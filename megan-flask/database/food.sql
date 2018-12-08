-- Table: Food 

PRAGMA foreign_keys = off;
BEGIN TRANSACTION;


Create Table food ( 
    Name    TEXT    Primary KEY,
    Calories    INT,
    Shop    Text
)

INSERT INTO food ( 
    Name, Calories, Shop 
)

Values ( 
    "Egg Mayo Sub", 435, "Subway"
)

INSERT INTO food ( 
    Name, Calories, Shop 
)

Values ( 
    "Subway Melt", 352, "Subway"
)


INSERT INTO food ( 
    Name, Calories, Shop 
)

Values ( 
    "Veggie Delite", 206, "Subway"
)




COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
