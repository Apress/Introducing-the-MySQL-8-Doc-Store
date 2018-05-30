-- Dump created by MySQL pump utility, version: 8.0.3-rc, macos10.12 (x86_64)
-- Dump start time: Wed Jan  3 11:08:16 2018
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
DROP DATABASE `library_v3`;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `library_v3` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
CREATE TABLE `library_v3`.`books` (
`doc` json DEFAULT NULL,
`_id` varchar(32) GENERATED ALWAYS AS (json_unquote(json_extract(`doc`,_utf8mb4'$._id'))) STORED NOT NULL,
PRIMARY KEY (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;
INSERT INTO `library_v3`.`books` (`doc`) VALUES ("{\"_id\": \"9801A79DE093A10A11E7EF5EBC5E9900\", \"ISBN\": \"978-1-4842-2107-5\", \"Title\": \"Windows 10 for the Internet of Things\", \"Authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}], \"Language\": \"English\", \"Pub_Year\": 2017, \"Publisher\": {\"URL\": \"http://apress.com\", \"City\": \"New York, NY\", \"Name\": \"Apress\"},\"Edition\":1}"),("{\"_id\": \"9801A79DE093A17211E7EF5EBC603C0F\", \"ISBN\": \"978-1-4842-3122-7\", \"Title\": \"MicroPython for the Internet of Things\", \"Authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}], \"Language\": \"English\", \"Pub_Year\": 2017, \"Publisher\": {\"URL\": \"http://apress.com\", \"City\": \"New York, NY\", \"Name\": \"Apress\"},\"Edition\":1}"),("{\"_id\": \"9801A79DE093A1D311E7EF5EBC5F7617\", \"ISBN\": \"978-1-4842-2724-4\", \"Title\": \"Introducing the MySQL 8 Document Store\", \"Authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}], \"Language\": \"English\", \"Pub_Year\": 2018, \"Publisher\": {\"URL\": \"http://apress.com\", \"City\": \"New York, NY\", \"Name\": \"Apress\"},\"Edition\":1}"),("{\"_id\": \"9801A79DE093AD6811E7EF5EBC614C05\", \"ISBN\": \"978-1449339586\", \"Title\": \"MySQL High Availability\", \"Authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}, {\"LastName\": \"Kindahl\", \"FirstName\": \"Mats\"}, {\"LastName\": \"Thalmann\", \"FirstName\": \"Lars\"}], \"Language\": \"English\", \"Pub_Year\": 2014, \"Publisher\": {\"URL\": \"http://oreilly.com\", \"City\": \"Boston, MA\", \"Name\": \"OReilly\"},\"Edition\":2}"),("{\"_id\": \"9801A79DE093BB2511E7EF5EBC58FAC2\", \"ISBN\": \"978-1-4842-1294-3\", \"Title\": \"MySQL for the Internet of Things\", \"Authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}], \"Language\": \"English\", \"Pub_Year\": 2016, \"Publisher\": {\"URL\": \"http://apress.com\", \"City\": \"New York, NY\", \"Name\": \"Apress\"},\"Edition\":1}"),("{\"_id\": \"9801A79DE093BBD311E7EF5EBC56E123\", \"ISBN\": \"978-1-4842-1174-8\", \"Title\": \"3D Printing with Delta Printers\", \"Authors\": [{\"LastName\": \"Bell\", \"FirstName\": \"Charles\"}], \"Language\": \"English\", \"Pub_Year\": 2015, \"Publisher\": {\"URL\": \"http://apress.com\", \"City\": \"New York, NY\", \"Name\": \"Apress\"},\"Edition\":1}");
SET TIME_ZONE=@OLD_TIME_ZONE;
SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT;
SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS;
SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET SQL_MODE=@OLD_SQL_MODE;
-- Dump end time: Wed Jan  3 11:08:17 2018
