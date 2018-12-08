--
-- File generated with SQLiteStudio v3.2.1 on Wed Dec 5 22:57:47 2018
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;


-- Table: Vendors
DROP TABLE IF EXISTS Vendors;

CREATE TABLE Vendors (
    Name TEXT    PRIMARY KEY,
    Menu INTEGER
);

INSERT INTO Vendors ( 
    Name, Menu
)

values (
    "MacDonalds", 3
)


Insert INTO Vendors ( 
    Name, Menu 
)

value (
"Subway", 3 
  )



COMMIT TRANSACTION;
PRAGMA foreign_keys = on;


