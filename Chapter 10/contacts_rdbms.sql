-- Dump created by MySQL pump utility, version: 8.0.3-rc, macos10.12 (x86_64)
-- Dump start time: Thu Jan 18 19:51:00 2018
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
DROP DATABASE `contact_list1`;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `contact_list1` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
CREATE TABLE `contact_list1`.`addresses` (
`addr_id` int(11) NOT NULL AUTO_INCREMENT,
`contact_id` int(11) NOT NULL,
`address_type` ENUM('work', 'home', 'other') DEFAULT 'home',
`street1` char(100) DEFAULT NULL,
`street2` char(100) DEFAULT NULL,
`city` char(30) DEFAULT NULL,
`state` char(30) DEFAULT NULL,
`zip` char(10) DEFAULT NULL,
PRIMARY KEY (`addr_id`,`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;
USE `contact_list1`;
ALTER TABLE `contact_list1`.`addresses` ADD KEY `contact_id` (`contact_id`);
ALTER TABLE `contact_list1`.`addresses` ADD CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`contact_id`);
CREATE TABLE `contact_list1`.`contacts` (
`contact_id` int(11) NOT NULL AUTO_INCREMENT,
`first` char(30) DEFAULT NULL,
`last` char(30) DEFAULT NULL,
PRIMARY KEY (`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;
CREATE TABLE `contact_list1`.`email_addresses` (
`email_id` int(11) NOT NULL AUTO_INCREMENT,
`contact_id` int(11) NOT NULL,
`email_address` char(64) DEFAULT NULL,
PRIMARY KEY (`email_id`,`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;
USE `contact_list1`;
ALTER TABLE `contact_list1`.`email_addresses` ADD KEY `contact_id` (`contact_id`);
ALTER TABLE `contact_list1`.`email_addresses` ADD CONSTRAINT `email_addresses_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`contact_id`);
CREATE TABLE `contact_list1`.`phones` (
`phone_id` int(11) NOT NULL AUTO_INCREMENT,
`contact_id` int(11) NOT NULL,
`phone` char(30) DEFAULT NULL,
PRIMARY KEY (`phone_id`,`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;
USE `contact_list1`;
ALTER TABLE `contact_list1`.`phones` ADD KEY `contact_id` (`contact_id`);
ALTER TABLE `contact_list1`.`phones` ADD CONSTRAINT `phones_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`contact_id`);
SET TIME_ZONE=@OLD_TIME_ZONE;
SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT;
SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS;
SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET SQL_MODE=@OLD_SQL_MODE;
-- Dump end time: Thu Jan 18 19:51:00 2018
INSERT INTO contact_list1.contacts VALUES (Null, 'Bill', 'Smith');
INSERT INTO contact_list1.addresses VALUES (Null, 1, 'home', '123 Main Street', Null, 'Anywhere', 'VT', 12388);
INSERT INTO contact_list1.phones VALUES (Null, 1, '(301) 555-1212');
INSERT INTO contact_list1.email_addresses VALUES (Null, 1, 'bill@smithmanufacturing.co');
INSERT INTO contact_list1.email_addresses VALUES (Null, 1, 'bill.smith@gomail.com');
SELECT * FROM contact_list1.contacts WHERE first = 'Bill' AND last = 'Smith';
SELECT * FROM contact_list1.addresses WHERE contact_id = 1;
SELECT * FROM contact_list1.email_addresses WHERE contact_id = 1;
SELECT * FROM contact_list1.phones WHERE contact_id = 1;


