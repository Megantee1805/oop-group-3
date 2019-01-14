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
  weight INTEGER NOT NULL
);

CREATE TABLE food_entry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  creator_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
  food_code VARCHAR(6) NOT NULL,
  food_name TEXT NOT NULL,
  calories INT NOT NULL,
  FOREIGN KEY (creator_id) REFERENCES user (id)
);

CREATE TABLE question_and_answer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT,
  answer TEXT
);
