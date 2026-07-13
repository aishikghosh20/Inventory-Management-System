-- Inventory Management System
-- settings.sql
-- SQL queries extracted from settings.py

-- Query 1
SELECT 1
            FROM Users
            WHERE user_id = %s;

-- Query 2
SELECT
                user_id,
                username,
                first_name,
                last_name,
                role,
                created_at
            FROM Users
            WHERE user_id=%s;

-- Query 3
SELECT 1 FROM USERS WHERE username= %s;

-- Query 4
SELECT 1 FROM USERS WHERE email= %s;

-- Query 5
SELECT 1 FROM USERS WHERE phone_number= %s;

-- Query 6
INSERT INTO Users
                (
                    username,
                    password_hash,
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    role
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s,%s
                );

-- Query 7
SELECT
                    user_id,
                    username,
                    first_name,
                    last_name,
                    role,
                    created_at
                FROM Users
                ORDER BY
                    first_name ASC,
                    last_name ASC;

-- Query 8
SELECT
                            user_id,
                            username,
                            first_name,
                            last_name,
                            role,
                            created_at
                        FROM Users
                        WHERE LOWER(username)=LOWER(%s);

-- Query 9
SELECT COUNT(*)
                    FROM Users
                    WHERE role='Administrator';

-- Query 10
UPDATE Users
                SET
                    username = %s,
                    first_name = %s,
                    last_name = %s,
                    role = %s
                WHERE user_id = %s;

-- Query 11
DELETE FROM Users
                WHERE user_id = %s;

-- Query 12
SELECT
                    password_hash
                FROM Users
                WHERE user_id = %s;

-- Query 13
UPDATE Users
                SET password_hash = %s
                WHERE user_id = %s;

-- Query 14
SELECT COUNT(*)
            FROM Users
            WHERE role = %s;

-- Query 15
SELECT
                    role,
                    COUNT(*)
                FROM Users
                GROUP BY role
                ORDER BY role;

-- Query 16
SELECT
                    user_id,
                    username,
                    first_name,
                    last_name,
                    created_at
                FROM Users
                WHERE role = %s
                ORDER BY
                    first_name ASC,
                    last_name ASC;

-- Query 17
SELECT DATABASE();

-- Query 18
SELECT VERSION();

-- Query 19
SELECT COUNT(*) FROM Users;

-- Query 20
SELECT COUNT(*) FROM Products;

-- Query 21
SELECT COUNT(*) FROM Categories;

-- Query 22
SELECT COUNT(*) FROM Suppliers;

-- Query 23
SELECT COUNT(*) FROM Customers;

-- Query 24
SELECT COUNT(*) FROM Purchases;

-- Query 25
SELECT COUNT(*) FROM Sales;

-- Query 26
SELECT
                    IFNULL(
                        SUM(stock_quantity * selling_price),
                        0
                    )
                FROM Products;

