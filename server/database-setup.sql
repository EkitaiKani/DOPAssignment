CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    points INT NOT NULL DEFAULT 0
);

CREATE TABLE redeemable_items (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    value INT NOT NULL DEFAULT 0
);

CREATE TABLE admin_users (
    admin_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

INSERT INTO students (name, points) VALUES
    ('John Doe', 100),
    ('Jane Smith', 150),
    ('Alice Johnson', 200),
    ('Bob Brown', 50);

INSERT INTO redeemable_items (name, quantity, value) VALUES
    ('Gift Card', 10, 50),
    ('Headphones', 5, 100),
    ('Laptop', 2, 500),
    ('Voucher', 20, 10);

INSERT INTO admin_users (username, password) VALUES
    ('admin', 'admin_password');