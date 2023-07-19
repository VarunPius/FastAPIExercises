-- DDL: Create table :
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    address VARCHAR(255)
);

-- DML: Insert data
INSERT INTO USERS (name, email, address)
VALUES ('test_user1', 'user1@me.io', 'Boston, MA');
INSERT INTO USERS (name, email, address)
VALUES ('test_user2', 'user2@you.io', 'Seattle, WA');
INSERT INTO USERS (name, email, address)
VALUES ('test_user3', 'user3@us.gov', 'Vancouver, BC');

-- DQL: Select
SELECT * FROM users;
