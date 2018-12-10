BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `Shops` (
	`Name`	TEXT UNIQUE,
	`Menu`	INTEGER,
	`Location`	TEXT,
	PRIMARY KEY(`Name`)
);
INSERT INTO `Shops` VALUES ('Subway',4,'Nanyang Poly');
INSERT INTO `Shops` VALUES ('Manna',4,'Nanyang Poly');
CREATE TABLE IF NOT EXISTS `Food` (
	`Name`	TEXT,
	`Code`	TEXT UNIQUE,
	`Shop`	TEXT,
	`Calories`	INTEGER,
	PRIMARY KEY(`Name`)
);

INSERT INTO `Food` VALUES ('Subway Melt','b00001','Subway',352);
INSERT INTO `Food` VALUES ('Subway Club','b00004','Subway',300);
INSERT INTO `Food` VALUES ('Egg Mayo','b00003','Subway',435);
INSERT INTO `Food` VALUES ('McSpicy','a00006','McDonald''s',522);
INSERT INTO `Food` VALUES ('Spicy Chicken McWrap','a0004','McDonald''s',476);
COMMIT;
