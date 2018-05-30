CREATE TABLE `animals`.`pets_sql` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(20) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `breed` char(20) DEFAULT NULL,
  `type` char(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO animals.pets_sql VALUES (Null, 'Violet', 6, 'dachshund', 'dog');
INSERT INTO animals.pets_sql VALUES (Null, 'JonJon', 15,'poodle', 'dog');
INSERT INTO animals.pets_sql VALUES (Null, 'Mister', 4,'siberian khatru', 'cat');
INSERT INTO animals.pets_sql VALUES (Null, 'Spot', 7,'koi', 'fish');
INSERT INTO animals.pets_sql VALUES (Null, 'Charlie', 6,'dachshund', 'dog');

CREATE VIEW `animals`.`num_pets` AS 
SELECT type as Type, COUNT(*) as Num 
FROM animals.pets_sql 
GROUP BY type;
