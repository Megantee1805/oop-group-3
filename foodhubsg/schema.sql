-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS food_entry;
DROP TABLE IF EXISTS question_and_answer;


CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email VARCHAR(512) UNIQUE NOT NULL,
  password TEXT NOT NULL,
  height INTEGER NOT NULL,
  weight INTEGER NOT NULL,
  location TEXT NOT NULL,
  status BOOLEAN NOT NULL
);

-- CREATE TABLE vendors (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   vendor_name TEXT NOT NULL,
--   average_calories INT NOT NULL,
--   area TEXT NOT NULL,
--   location TEXT NOT NULL,
--   description TEXT NOT NULL,
--   rating INT NOT NULL,
--   image_location TEXT NOT NULL
-- );
--
-- CREATE TABLE food (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   code VARCHAR(6) UNIQUE NOT NULL,
--   name TEXT NOT NULL,
--   calories INT NOT NULL,
--   vendor TEXT NOT NULL
-- );

CREATE TABLE food_entry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  creator_id INTEGER NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  food_code VARCHAR(6) NOT NULL,
  food_name TEXT NOT NULL,
  calories INT NOT NULL,
  FOREIGN KEY (creator_id) REFERENCES user (id)
);

CREATE TABLE question_and_answer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT,
  answer TEXT,
  user TEXT
);
