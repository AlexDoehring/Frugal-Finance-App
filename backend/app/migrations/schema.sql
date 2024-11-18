CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    description VARCHAR(255) --optional
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    threshold FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255) --optional
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    source_name VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    frequency VARCHAR(50) NOT NULL, -- e.g., "monthly", "weekly", "one-time"
    description VARCHAR(255), -- optional
    FOREIGN KEY (user_id) REFERENCES user(id)
);
