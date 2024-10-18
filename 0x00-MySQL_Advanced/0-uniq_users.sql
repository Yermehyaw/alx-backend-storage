-- Creates a table with all the attributes of the email column unique
CREATE TABLE IF NOT EXISTS users (
       id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(255) NOT NULL UNIQUE,
       nane VARCHAR(255) NOT NULL UNIQUE
);
