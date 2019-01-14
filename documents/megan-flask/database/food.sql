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



INSERT INTO food ( 
    Name, Calories, Shop 
)

Values ( 
    "Subway Club", 300, "Subway"
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
    "McSpicy", 522, "McDonalds"
)


INSERT INTO food ( 
    Name, Calories, Shop 
)

Values ( 
    "Spicy Chicken McWrap", 476, "McDonalds"
)


INSERT INTO food ( 
    Name, Calories, Shop 
)

Values ( 
    "Cheeseburger", 300, "McDonalds"
)


INSERT INTO food ( 
    Name, Calories, Shop 
)

Values ( 
    "Filet-O-Fish", 332, "McDonalds"
)







COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
