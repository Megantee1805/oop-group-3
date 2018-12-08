PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

CREATE TABLE Profile (
    Email    TEXT   PRIMARY KEY,
    Name     TEXT,
    Password TEXT,
    Height   DOUBLE,
    Weight   INT
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

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
