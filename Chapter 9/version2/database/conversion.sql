mysql> ALTER TABLE library_v2.books ADD COLUMN Authors JSON NOT NULL;
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> EXPLAIN library_v2.books;
+-------------+----------+------+-----+---------+-------+
| Field       | Type     | Null | Key | Default | Extra |
+-------------+----------+------+-----+---------+-------+
| ISBN        | char(32) | NO   | PRI | NULL    |       |
| Title       | text     | NO   |     | NULL    |       |
| Year        | int(11)  | NO   |     | 2017    |       |
| Edition     | int(11)  | YES  |     | 1       |       |
| PublisherId | int(11)  | YES  | MUL | NULL    |       |
| Language    | char(24) | NO   |     | English |       |
| Authors     | json     | NO   |     | NULL    |       |
+-------------+----------+------+-----+---------+-------+
7 rows in set (0.01 sec)


DROP PROCEDURE convert_books_hybrid;
DELIMITER //
CREATE PROCEDURE convert_books_hybrid()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE isbn_val char(32);
    DECLARE author_id int;
    DECLARE json_obj JSON;
    DECLARE author_list varchar(255);
    DECLARE books_cursor CURSOR FOR SELECT ISBN FROM library_v2.books;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN books_cursor;
    
    books_loop: LOOP
        SET author_list = "[]";
        FETCH books_cursor INTO isbn_val;
        IF done THEN
          LEAVE books_loop;
        END IF;
        SET author_list = (SELECT GROUP_CONCAT(JSON_OBJECT('LastName', library_v2.authors.LastName,'FirstName',library_v2.authors.FirstName) SEPARATOR ', ') AS author_names
            FROM library_v2.books_authors JOIN library_v2.authors ON books_authors.AuthorId = authors.AuthorId
            WHERE ISBN = isbn_val GROUP BY library_v2.books_authors.ISBN);
        SET json_obj = CONCAT('{"authors":[',author_list,']}');
        UPDATE library_v2.books SET Authors = json_obj WHERE ISBN = isbn_val;
    END LOOP;
        
    CLOSE books_cursor;
END; //
DELIMITER ;

CALL convert_books_hybrid;

mysql> SELECT * from books;
+-------------------+----------------------------------------+------+---------+-------------+----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ISBN              | Title                                  | Year | Edition | PublisherId | Language | Authors                                                                                                                                                        |
+-------------------+----------------------------------------+------+---------+-------------+----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 978-1-4842-1174-8 | 3D Printing with Delta Printers        | 2015 |       1 |           1 | English  | {"authors": [{"LastName": "Bell", "FirstName": "Charles"}]}                                                                                                  |
| 978-1-4842-1294-3 | MySQL for the Internet of Things       | 2016 |       1 |           1 | English  | {"authors": [{"LastName": "Bell", "FirstName": "Charles"}]}                                                                                                  |
| 978-1-4842-2107-5 | Windows 10 for the Internet of Things  | 2017 |       1 |           1 | English  | {"authors": [{"LastName": "Bell", "FirstName": "Charles"}]}                                                                                                  |
| 978-1-4842-2724-4 | Introducing the MySQL 8 Document Store | 2018 |       1 |           1 | English  | {"authors": [{"LastName": "Bell", "FirstName": "Charles"}]}                                                                                                  |
| 978-1-4842-3122-7 | MicroPython for the Internet of Things | 2017 |       1 |           1 | English  | {"authors": [{"LastName": "Bell", "FirstName": "Charles"}]}                                                                                                  |
| 978-1449339586    | MySQL High Availability                | 2014 |       2 |           3 | English  | {"authors": [{"LastName": "Bell", "FirstName": "Charles"}, {"LastName": "Kindahl", "FirstName": "Mats"}, {"LastName": "Thalmann", "FirstName": "Lars"}]} |
+-------------------+----------------------------------------+------+---------+-------------+----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.00 sec)

drop table books_authors;
drop table authors;

DROP FUNCTION library_v2.get_author_names;
DELIMITER //
CREATE FUNCTION library_v2.get_author_names(isbn_lookup char(32)) RETURNS TEXT DETERMINISTIC
BEGIN
    DECLARE j_array varchar(255);
    DECLARE num_items int;
    DECLARE i int;
    DECLARE last char(20);
    DECLARE first char(20);
    DECLARE csv varchar(255);
    SET j_array = (SELECT JSON_EXTRACT(Authors,'$.authors') FROM library_v2.books WHERE ISBN = isbn_lookup);
    SET num_items = JSON_LENGTH(j_array);
    SET csv = "";
    SET i = 0;
    author_loop: LOOP
        IF i < num_items THEN
			SET last = CONCAT('$[',i,'].LastName');
			SET first = CONCAT('$[',i,'].FirstName');
            IF i > 0 THEN
                SET csv = CONCAT(csv,", ",JSON_UNQUOTE(JSON_EXTRACT(j_array,last)),' ', JSON_UNQUOTE(JSON_EXTRACT(j_array,first)));
            ELSE
                SET csv = CONCAT(JSON_UNQUOTE(JSON_EXTRACT(j_array,last)),' ', JSON_UNQUOTE(JSON_EXTRACT(j_array,first)));
            END IF;
            SET i = i + 1;
        ELSE
           LEAVE author_loop;
        END IF;
    END LOOP;
    RETURN csv;
END;//
DELIMITER ;

SIDEBAR on existing MySQL servers that have not been configured for the XDevAPI:

Must enable the X Protocol:

INSTALL PLUGIN mysqlx SONAME 'mysqlx.so';

Must use 33060 port

Must enable SSL

$ sudo mysql_ssl_rsa_setup --datadir=/usr/local/mysql/data/ --uuid=_mysql
Generating a 2048 bit RSA private key
.........................................+++
.............+++
writing new private key to 'ca-key.pem'
-----
Generating a 2048 bit RSA private key
......................................................................................+++
...........................................................................................+++
writing new private key to 'server-key.pem'
-----
Generating a 2048 bit RSA private key
......................+++
.+++
writing new private key to 'client-key.pem'
-----


Add to the configuration file:
[mysqld]
...
ssl-ca=/usr/local/mysql/data/ca.pem
ssl-cert=/usr/local/mysql/data/server-cert.pem
ssl-key=/usr/local/mysql/data/server-key.pem


You may need to change the owner:

bash-3.2# cd /usr/local/mysql/data
bash-3.2# chown _mysql *.pem
bash-3.2# ls -lsa *.pem
8 -rw-------  1 _mysql  _mysql  1679 Jan  1 10:54 ca-key.pem
8 -rw-r--r--  1 _mysql  _mysql  1078 Jan  1 10:54 ca.pem
8 -rw-r--r--  1 _mysql  _mysql  1086 Jan  1 10:54 client-cert.pem
8 -rw-------  1 _mysql  _mysql  1675 Jan  1 10:54 client-key.pem
8 -rw-------  1 _mysql  _mysql  1675 Jan  1 10:55 private_key.pem
8 -rw-r--r--  1 _mysql  _mysql   451 Jan  1 10:55 public_key.pem
8 -rw-r--r--  1 _mysql  _mysql  1086 Jan  1 10:54 server-cert.pem
8 -rw-------  1 _mysql  _mysql  1675 Jan  1 10:54 server-key.pem


"SELECT DISTINCT book.ISBN, book.ISBN, Title, publisher.Name as Publisher, Year, library_v2.get_author_names(book.ISBN)  FROM library_v2.books As book INNER JOIN library_v2.publishers as publisher on book.PublisherId=publisher.PublisherId ORDER BY book.ISBN DESC"

{"authors":[{"LastName":"Bell","FirstName":"Charles"},{"LastName":"Kindahl","FirstName":"Mats"},{"LastName":"Thalmann","FirstName":"Lars"}]}
{"authors":[{"LastName":"Bell","FirstName":"Charles"},{"LastName":"Kindahl","FirstName":"Mats"},{"LastName":"Thalmann","FirstName":"Lars"}]}

{"authors":[{"LastName":"Bell","FirstName":"Charles"},{"LastName":"Kindahl","FirstName":"Mats"},{"LastName":"Thalmann","FirstName":"Lars"}]}
{"authors":[{"LastName":"Bell","FirstName":"Charles"},{"LastName":"Kindahl","FirstName":"Mats"},{"LastName":"Thalmann","FirstName":"Lars"}]}
