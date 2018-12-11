-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS food_entry;


CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email VARCHAR(512) UNIQUE NOT NULL,
  password TEXT NOT NULL,
  height INTEGER NOT NULL,
  weight INTEGER NOT NULL
);

CREATE TABLE food_entry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  creator_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  food_code VARCHAR(6) NOT NULL,
  food_name TEXT NOT NULL,
  calories INT NOT NULL,
  FOREIGN KEY (creator_id) REFERENCES user (id)
);
