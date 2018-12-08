--
-- File generated with SQLiteStudio v3.2.1 on Wed Dec 5 22:57:47 2018
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: food-entry
CREATE TABLE food_entry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  creator_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  food_code VARCHAR(6) NOT NULL,
  food_name TEXT NOT NULL,
  calories INT NOT NULL,
  FOREIGN KEY (creator_id) REFERENCES user (id)
);


-- Table: Profile
DROP TABLE IF EXISTS Profile;

CREATE TABLE Profile (
    Email    TEXT   PRIMARY KEY,
    Name     TEXT,
    Password TEXT,
    Height   DOUBLE,
    Weight   INT
);


-- Table: Vendors
DROP TABLE IF EXISTS Vendors;

CREATE TABLE Vendors (
    Name TEXT    PRIMARY KEY,
    Menu INTEGER
);

INSERT INTO Profile (
email, name, password, height, weight) 
values 
("Casey@mail.com", "Casey", "FatnDepressed", 1.70, 80) 

INSERT INTO Profile (
email, name, password, height, weight) 
values 
("jitminislife@mail.com", "jitmin", "BTSismylife", 1.59, 50)

INSERT INTO Profile (
    email, name, password, height, weight 
)
values 
("gracedwithlife@mail.com", "Grace", "Allisablessing", 1.60, 70)

INSERT INTO Profile ( 
    email, name, password, height, weight 
)
values 
("awakeatmidnight@mail.com", "Nightowl", "Iearnmorethandayworkers", 1.8, 77)

INSERT INTO Profile ( 
    email, name, password, height, weight
)

values 
("workfrom7to12@mail.com", "Albus", "CBBLimited", 1.78, 60)

INSERT INTO Vendors ( 
    Name, Menu
)

values (
    "MacDonalds", 3
)


Insert INTO Vendors ( 
    Name, Menu
)

values (
    "Subway", 4
) 
INSERT INTO Food (
    Name, Calories
)

VALUES (
    "Filet-O-Fish", 379
       )

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
