CREATE TABLE students (
    studentid VARCHAR(10) PRIMARY KEY,
	password VARCHAR(255) NOT NULL,
    username VARCHAR(100) NOT NULL,
    diplomaofstudy VARCHAR(100) NOT NULL,
    yearofentry INT NOT NULL,
    emailaddress VARCHAR(100) NOT NULL,
    points INT NOT NULL DEFAULT 0
);

CREATE TABLE redeemable_items (
    itemid SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    value INT NOT NULL DEFAULT 0
);

CREATE TABLE admins (
    adminid VARCHAR(10) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

TRUNCATE TABLE redeemable_items;
TRUNCATE TABLE students;
TRUNCATE TABLE admins;

INSERT INTO students (studentid, password, username, diplomaofstudy, yearofentry, emailaddress, points) VALUES
    ('A1234567X', 'scrypt:32768:8:1$ZiUQqpsICuLqh5NS$8a6f2803d1986af8d539fb3a7e662bb66b2fdef774889e8cf327abaecbf46194b9f0fbac3dbb05eaee47b50286d9d6b2518089e5e7b02f0efa7cbdd89ea5e3e1', 'John Tan', 'Diploma in IT', 2024, 'john.tan.2024@example.edu', 50),
    ('A1234568Y', 'scrypt:32768:8:1$5dQddlxx4ydcFYec$e77847efc6ea5f0717f98af177ff31f25993aa3f9840c692313af547d1760c526331611011600ad2fadb8c321d0a47de54945cfe4da9b5d97e9be8c403ffe459', 'Sarah Lim', 'Diploma in Business', 2023, 'sarah.lim.2024@example.edu', 80);

INSERT INTO redeemable_items (name, quantity, value) VALUES
    ('Gift Card', 10, 50),
    ('Headphones', 5, 100),
    ('Laptop', 2, 500),
    ('Voucher', 20, 10);

INSERT INTO admins (adminid, username, password) VALUES
    ('A0000000A', 'Admin', 'scrypt:32768:8:1$OhTURrIyRok8nRj7$55b1e99e1a881e2e98e6a8e3dbb5f7fd4d4e2f74dc6825a2d1fe1941c288af9730774e05b22205431133cef5be13a2e9aef68e7a5f30f736fa39143b95d500a9');
