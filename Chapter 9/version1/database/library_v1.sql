-- Dump created by MySQL pump utility, version: 8.0.3-rc, macos10.12 (x86_64)
-- Dump start time: Sun Dec 31 15:21:54 2017
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
DROP DATABASE `library_v1`;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `library_v1` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
CREATE TABLE `library_v1`.`authors` (
`AuthorId` int(11) NOT NULL AUTO_INCREMENT,
`FirstName` varchar(64) DEFAULT NULL,
`LastName` varchar(64) DEFAULT NULL,
PRIMARY KEY (`AuthorId`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4
;
INSERT INTO `library_v1`.`authors` VALUES (1,"Charles","Bell"),(2,"Mats","Kindahl"),(3,"Lars","Thalmann");
CREATE TABLE `library_v1`.`books` (
`ISBN` char(32) NOT NULL,
`Title` text NOT NULL,
`Year` int(11) NOT NULL DEFAULT '2017',
`Edition` int(11) DEFAULT '1',
`PublisherId` int(11) DEFAULT NULL,
`Language` char(24) NOT NULL DEFAULT 'English',
PRIMARY KEY (`ISBN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;
INSERT INTO `library_v1`.`books` VALUES ("978-1-4842-1174-8","3D Printing with Delta Printers",2015,1,1,"English"),("978-1-4842-1294-3","MySQL for the Internet of Things",2016,1,1,"English"),("978-1-4842-2107-5","Windows 10 for the Internet of Things",2017,1,1,"English"),("978-1-4842-2724-4","Introducing the MySQL 8 Document Store",2018,1,1,"English"),("978-1-4842-3122-7","MicroPython for the Internet of Things",2017,1,1,"English"),("978-1449339586","MySQL High Availability",2014,2,3,"English");
CREATE TABLE `library_v1`.`books_authors` (
`ISBN` char(32) NOT NULL,
`AuthorId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;
USE `library_v1`;
ALTER TABLE `library_v1`.`books` ADD KEY `pub_id` (`PublisherId`);
ALTER TABLE `library_v1`.`books` ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`PublisherId`) REFERENCES `publishers` (`publisherid`);
CREATE TABLE `library_v1`.`notes` (
`NoteId` int(11) NOT NULL AUTO_INCREMENT,
`ISBN` char(32) NOT NULL,
`Note` text,
PRIMARY KEY (`NoteId`,`ISBN`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4
;
INSERT INTO `library_v1`.`books_authors` VALUES ("978-1-4842-2724-4",1),("978-1-4842-3122-7",1),("978-1-4842-2107-5",1),("978-1-4842-1294-3",1),("978-1-4842-1174-8",1),("978-1449339586",1),("978-1449339586",2),("978-1449339586",3);
USE `library_v1`;
ALTER TABLE `library_v1`.`books_authors` ADD KEY `auth_id` (`AuthorId`);
ALTER TABLE `library_v1`.`books_authors` ADD KEY `isbn_id` (`ISBN`);
ALTER TABLE `library_v1`.`books_authors` ADD CONSTRAINT `books_authors_fk_1` FOREIGN KEY (`ISBN`) REFERENCES `books` (`isbn`);
ALTER TABLE `library_v1`.`books_authors` ADD CONSTRAINT `books_authors_fk_2` FOREIGN KEY (`AuthorId`) REFERENCES `authors` (`authorid`);
USE `library_v1`;
ALTER TABLE `library_v1`.`notes` ADD KEY `ISBN` (`ISBN`);
ALTER TABLE `library_v1`.`notes` ADD CONSTRAINT `notes_fk_1` FOREIGN KEY (`ISBN`) REFERENCES `books` (`isbn`);
CREATE TABLE `library_v1`.`publishers` (
`PublisherId` int(11) NOT NULL AUTO_INCREMENT,
`Name` varchar(128) NOT NULL,
`City` varchar(32) DEFAULT NULL,
`URL` text,
PRIMARY KEY (`PublisherId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `library_v1`.`get_author_ids`(isbn_lookup char(32)) RETURNS varchar(128) CHARSET utf8mb4
    DETERMINISTIC
RETURN (
        SELECT GROUP_CONCAT(library_v1.authors.AuthorId SEPARATOR ', ') AS author_ids
            FROM library_v1.books_authors JOIN library_v1.authors ON books_authors.AuthorId = authors.AuthorId
        WHERE ISBN = isbn_lookup GROUP BY library_v1.books_authors.ISBN
)//
DELIMITER ;
;
INSERT INTO `library_v1`.`publishers` VALUES (1,"Apress","New York NY","http://apress.com"),(2,"Rocky Mountain Press","Colorado, CO",''),(3,"OReilly","Boston, MA","http://www.oreilly.com");
DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `library_v1`.`get_author_names`(isbn_lookup char(32)) RETURNS varchar(128) CHARSET utf8mb4
    DETERMINISTIC
RETURN (
        SELECT GROUP_CONCAT(library_v1.authors.LastName SEPARATOR ', ') AS author_names
            FROM library_v1.books_authors JOIN library_v1.authors ON books_authors.AuthorId = authors.AuthorId
        WHERE ISBN = isbn_lookup GROUP BY library_v1.books_authors.ISBN
)//
DELIMITER ;
;
SET TIME_ZONE=@OLD_TIME_ZONE;
SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT;
SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS;
SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET SQL_MODE=@OLD_SQL_MODE;
-- Dump end time: Sun Dec 31 15:21:55 2017
