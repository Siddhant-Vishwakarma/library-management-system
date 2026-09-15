CREATE DATABASE IF NOT EXISTS library_management;
USE library_management;

-- Create table Admins
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table Books
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100),
    category VARCHAR(50),
    isbn VARCHAR(20) UNIQUE,
    total_quantity INT NOT NULL,
    available_quantity INT NOT NULL,
    shelf_no VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table Users
-- NOTE: added `password` -- user_repository.py inserts and reads this
-- column (bcrypt hash) for member login, but it was missing from the
-- original schema.
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    department VARCHAR(100),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table issued_books
CREATE TABLE issued_books (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,
    book_id INT NOT NULL,

    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,

    fine DECIMAL(10,2) DEFAULT 0,

    status ENUM('Issued','Returned') DEFAULT 'Issued',

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (book_id)
        REFERENCES books(book_id)
        ON DELETE CASCADE
);

-- insert default admin
-- NOTE: password is a real bcrypt hash of "admin123" (not plaintext --
-- admin_repository.py calls bcrypt.checkpw() against this column, which
-- errors out on a non-hash value like the original schema had).
INSERT INTO admins (username, password)
VALUES
('admin', '$2b$12$SyYWFsWNrkW8gG8cBlfgkOb1JpG92bmc0NGf17VzhPFofmQDnb2nW');
-- login as: admin / admin123

-- insert sample books
INSERT INTO books
(title, author, publisher, category, isbn, total_quantity, available_quantity, shelf_no)
VALUES
('Python Programming', 'John Smith', 'ABC Publication', 'Programming', '978000001', 10, 10, 'A1'),
('Data Structures', 'Mark Lee', 'XYZ Publication', 'Computer Science', '978000002', 8, 8, 'B2'),
('Database Management', 'Korth', 'McGraw Hill', 'Database', '978000003', 6, 6, 'C1');

-- insert sample users
-- NOTE: password is a real bcrypt hash of "password123" for both, so you
-- can actually log in and test the member menu.
INSERT INTO users
(full_name, email, phone, department, password)
VALUES
('Rahul Sharma', 'rahul@gmail.com', '9876543210', 'CSE', '$2b$12$kksNT896wjWNW2OXuUhZPOFoCUxsV3iDOzBIEtJIsxRDvqux4Q42u'),
('Ankit Gupta', 'ankit@gmail.com', '9123456789', 'ECE', '$2b$12$kksNT896wjWNW2OXuUhZPOFoCUxsV3iDOzBIEtJIsxRDvqux4Q42u');
-- login as: rahul@gmail.com / password123  (or ankit@gmail.com / password123)
