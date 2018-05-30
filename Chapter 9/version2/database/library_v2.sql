-- Dump created by MySQL pump utility, version: 8.0.3-rc, macos10.12 (x86_64)
-- Dump start time: Mon Jan  1 13:50:48 2018
-- Server version: 8.0.3

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE;
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET @@SESSION.SQL_LOG_BIN= 0;
SET @OLD_TIME_ZONE=@@TIME_ZONE;
SET TIME_ZONE='+00:00';
SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT;
SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS;
SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION;
SET NAMES utf8mb4;
DROP DATABASE `library_v2`;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `library_v2` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
CREATE TABLE `library_v2`.`books` (
`ISBN` char(32) NOT NULL,
`Title` text NOT NULL,
`Year` int(11) NOT NULL DEFAULT '2017',
`Edition` int(11) DEFAULT '1',
`PublisherId` int(11) DEFAULT NULL,
`Language` char(24) NOT NULL DEFAULT 'English',
`Authors` json NOT NULL,
PRIMARY KEY (`ISBN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;
CREATE TABLE `library_v2`.`notes` (
`NoteId` int(11) NOT NULL AUTO_INCREMENT,
`ISBN` char(32) NOT NULL,
`Note` text,
PRIMARY KEY (`NoteId`,`ISBN`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4
;
INSERT INTO `library_v2`.`books` VALUES ("978-1-4842-1174-8","3D Printing with Delta Printers",2015,2015,1,"English","{\"authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}]}"),("978-1-4842-1294-3","MySQL for the Internet of Things",2016,1,1,"English","{\"authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}]}"),("978-1-4842-2107-5","Windows 10 for the Internet of Things",2017,1,1,"English","{\"authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}]}"),("978-1-4842-2724-4","Introducing the MySQL 8 Document Store",2018,1,1,"English","{\"authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}]}"),("978-1-4842-3122-7","MicroPython for the Internet of Things",2017,1,1,"English","{\"authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}]}"),("978-1449339586","MySQL High Availability",2014,2,3,"English","{\"authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}, {\"LastName\": \"Kindahl\", \"FirstName\": \"Mats\"}, {\"LastName\": \"Thalmann\", \"FirstName\": \"Lars\"}]}");
USE `library_v2`;
ALTER TABLE `library_v2`.`books` ADD KEY `pub_id` (`PublisherId`);
ALTER TABLE `library_v2`.`books` ADD CONSTRAINT `books_fk_1` FOREIGN KEY (`PublisherId`) REFERENCES `publishers` (`publisherid`);
CREATE TABLE `library_v2`.`publishers` (
`PublisherId` int(11) NOT NULL AUTO_INCREMENT,
`Name` varchar(128) NOT NULL,
`City` varchar(32) DEFAULT NULL,
`URL` text,
PRIMARY KEY (`PublisherId`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4
;
USE `library_v2`;
ALTER TABLE `library_v2`.`notes` ADD KEY `ISBN` (`ISBN`);
ALTER TABLE `library_v2`.`notes` ADD CONSTRAINT `notes_fk_1` FOREIGN KEY (`ISBN`) REFERENCES `books` (`isbn`);
INSERT INTO `library_v2`.`publishers` VALUES (1,"Apress","New York NY","http://apress.com"),(2,"Rocky Mountain Press","Colorado, CO",''),(3,"OReilly","Boston, MA","http://www.oreilly.com");
DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `library_v2`.`get_author_names`(isbn_lookup char(32)) RETURNS text CHARSET utf8mb4
    DETERMINISTIC
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
END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `library_v2`.`convert_books_hybrid`()
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
END//
DELIMITER ;
;
SET TIME_ZONE=@OLD_TIME_ZONE;
SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT;
SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS;
SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET SQL_MODE=@OLD_SQL_MODE;
-- Dump end time: Mon Jan  1 13:50:49 2018
