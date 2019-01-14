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
    "MacDonalds", 4
)


Insert INTO Vendors ( 
    Name, Menu 
)

values (
"Subway", 4
  )

Insert INTO Vendors ( 
    Name, Menu 
)

values (
"Manna", 4
  )


Insert INTO Vendors ( 
    Name, Menu 
)

values (
"Western Delight", 4
  )


Insert INTO Vendors ( 
    Name, Menu 
)

values (
"Fishball noodles", 4
  )


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;


