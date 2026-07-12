-- Query 1
INSERT INTO Categories
                    (
                        category_name, description
                    )
                    VALUES (%s, %s)

-- Query 2
SELECT category_id, category_name, description
                          FROM Categories
                          ORDER BY {order_by};

-- Query 3
SELECT
                    supplier_id,
                    supplier_name,
                    phone_number,
                    email,
                    address,
                    contact_person
                FROM Suppliers
                ORDER BY {order_by};

-- Query 4
SELECT
                            supplier_id,
                            supplier_name,
                            address,
                            phone_number,
                            email,
                            contact_person
                        FROM Suppliers
                        WHERE supplier_id = %s

-- Query 5
SELECT
                            supplier_id,
                            supplier_name,
                            address,
                            phone_number,
                            email,
                            contact_person
                        FROM Suppliers
                        WHERE LOWER(supplier_name) = LOWER(%s)

-- Query 6
SELECT
                            supplier_id,
                            supplier_name,
                            address,
                            phone_number,
                            email,
                            contact_person
                        FROM Suppliers
                        WHERE phone_number = %s

-- Query 7
SELECT
                            supplier_id,
                            supplier_name,
                            address,
                            phone_number,
                            email,
                            contact_person
                        FROM Suppliers
                        WHERE LOWER(email) = LOWER(%s)

-- Query 8
DELETE FROM Suppliers
                        WHERE supplier_id = %s

-- Query 9
INSERT INTO Products
                    (
                        product_name,
                        category_id,
                        supplier_id,
                        buying_price,
                        selling_price,
                        quantity,
                        reorder_level,
                        description
                    )
                    VALUES
                    (
                        %s,%s,%s,%s,%s,%s,%s,%s
                    )

-- Query 10
SELECT
                    p.product_id,
                    p.product_name,
                    c.category_name,
                    s.supplier_name,
                    p.buying_price,
                    p.selling_price,
                    p.quantity,
                    p.reorder_level,
                    p.description
                FROM Products p
                LEFT JOIN Categories c
                    ON p.category_id = c.category_id
                LEFT JOIN Suppliers s
                    ON p.supplier_id = s.supplier_id
                ORDER BY {order_by};

-- Query 11
SELECT
                            Products.product_id,
                            Products.product_name,
                            Categories.category_name,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE Products.product_id = %s

-- Query 12
SELECT
                            Products.product_id,
                            Products.product_name,
                            Categories.category_name,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE LOWER(Products.product_name)=LOWER(%s)

-- Query 13
DELETE FROM Products
                        WHERE product_id = %s

-- Query 14
SELECT
                            Products.product_id,
                            Products.product_name,
                            Products.category_id,
                            Categories.category_name,
                            Products.supplier_id,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE Products.product_id = %s

-- Query 15
SELECT
                            Products.product_id,
                            Products.product_name,
                            Products.category_id,
                            Categories.category_name,
                            Products.supplier_id,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE LOWER(Products.product_name)=LOWER(%s)

-- Query 16
SELECT category_name
                            FROM Categories
                            WHERE category_id = %s

-- Query 17
SELECT supplier_name
                            FROM Suppliers
                            WHERE supplier_id = %s

-- Query 18
SELECT category_name
                            FROM Categories
                            WHERE category_id=%s

-- Query 19
SELECT supplier_name
                            FROM Suppliers
                            WHERE supplier_id=%s

-- Query 20
INSERT INTO Customers
                    (
                        first_name,
                        last_name,
                        phone_number,
                        email,
                        address
                    )
                    VALUES
                    (
                        %s,%s,%s,%s,%s
                    )

-- Query 21
SELECT
                    customer_id,
                    first_name,
                    last_name,
                    phone_number,
                    email,
                    address
                FROM Customers
                ORDER BY {order_by};

-- Query 22
SELECT
                            customer_id,
                            first_name,
                            last_name,
                            phone_number,
                            email,
                            address
                        FROM Customers
                        WHERE customer_id = %s

-- Query 23
SELECT
                            customer_id,
                            first_name,
                            last_name,
                            phone_number,
                            email,
                            address
                        FROM Customers
                        WHERE LOWER(first_name) = LOWER(%s)

-- Query 24
DELETE FROM Customers
                        WHERE customer_id = %s

-- Query 25
SELECT supplier_name
                FROM Suppliers
                WHERE supplier_id = %s

-- Query 26
SELECT 1
            FROM Purchases
            WHERE purchase_id = %s

-- Query 27
SELECT
            Purchases.purchase_id,
            Suppliers.supplier_name,
            Users.username,
            Purchases.purchase_date,
            Purchases.total_amount,
            Purchases.status
        FROM Purchases
        LEFT JOIN Suppliers
            ON Purchases.supplier_id = Suppliers.supplier_id
        LEFT JOIN Users
            ON Purchases.user_id = Users.user_id
        WHERE Purchases.purchase_id = %s;

-- Query 28
SELECT
                    product_name,quantity
                FROM Products
                WHERE product_id = %s

-- Query 29
UPDATE Products
            SET quantity = quantity + %s
            WHERE product_id = %s

-- Query 30
SELECT
                    username
                FROM Users
                WHERE user_id = %s

-- Query 31
INSERT INTO Purchases
                (
                    supplier_id,
                    user_id,
                    total_amount
                )
                VALUES
                (
                    %s,%s,%s
                )

-- Query 32
INSERT INTO Purchase_Items
                    (
                        purchase_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES
                    (
                        %s,%s,%s,%s,%s
                    )

-- Query 33
SELECT
                    Purchases.purchase_id,
                    Suppliers.supplier_name,
                    Users.username,
                    Purchases.purchase_date,
                    Purchases.total_amount,
                    Purchases.status
                FROM Purchases
                LEFT JOIN Suppliers
                    ON Purchases.supplier_id = Suppliers.supplier_id
                LEFT JOIN Users
                    ON Purchases.user_id = Users.user_id
                ORDER BY {order_by};

-- Query 34
SELECT
                            Purchases.purchase_id,
                            Suppliers.supplier_name,
                            Users.username,
                            Purchases.purchase_date,
                            Purchases.total_amount,
                            Purchases.status
                        FROM Purchases
                        LEFT JOIN Suppliers
                            ON Purchases.supplier_id = Suppliers.supplier_id
                        LEFT JOIN Users
                            ON Purchases.user_id = Users.user_id
                        WHERE LOWER(Suppliers.supplier_name)=LOWER(%s)

-- Query 35
UPDATE Products
            SET quantity = quantity - %s
            WHERE product_id = %s

-- Query 36
SELECT 1
            FROM Sales
            WHERE sale_id = %s

-- Query 37
SELECT
                Sales.sale_id,
                Customers.first_name,
                Customers.last_name,
                Users.username,
                Sales.sale_date,
                Sales.total_amount,
                Sales.status
            FROM Sales
            LEFT JOIN Customers
                ON Sales.customer_id = Customers.customer_id
            LEFT JOIN Users
                ON Sales.user_id = Users.user_id
            WHERE Sales.sale_id = %s

-- Query 38
SELECT
                    customer_id,
                    first_name,
                    last_name
                FROM Customers
                WHERE customer_id = %s

-- Query 39
SELECT
                        customer_id
                    FROM Customers
                    WHERE LOWER(
                        CONCAT(
                            first_name,
                            ' ',
                            last_name
                        )
                    ) = LOWER(%s)

-- Query 40
SELECT
                        customer_id
                    FROM Customers
                    WHERE LOWER(
                        CONCAT(
                            first_name,
                            ' ',
                            last_name
                        )
                    ) = LOWER(%s)
                    AND customer_id != %s

-- Query 41
SELECT
                        quantity,
                        selling_price
                    FROM Products
                    WHERE product_id = %s

-- Query 42
INSERT INTO Sales
                (
                    customer_id,
                    user_id,
                    total_amount
                )
                VALUES
                (
                    %s,%s,%s
                )

-- Query 43
INSERT INTO Sale_Items
                    (
                        sale_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES
                    (
                        %s,%s,%s,%s,%s
                    )

-- Query 44
SELECT
                            Sales.sale_id,
                            Customers.first_name,
                            Customers.last_name,
                            Users.username,
                            Sales.sale_date,
                            Sales.total_amount,
                            Sales.status
                        FROM Sales
                        LEFT JOIN Customers
                            ON Sales.customer_id = Customers.customer_id
                        LEFT JOIN Users
                            ON Sales.user_id = Users.user_id
                        WHERE LOWER(
                            CONCAT(
                                Customers.first_name,
                                ' ',
                                Customers.last_name
                            )
                        ) = LOWER(%s)

-- Query 45
SELECT
                    Sales.sale_id,
                    Customers.first_name,
                    Customers.last_name,
                    Users.username,
                    Sales.sale_date,
                    Sales.total_amount,
                    Sales.status
                FROM Sales
                LEFT JOIN Customers
                    ON Sales.customer_id = Customers.customer_id
                LEFT JOIN Users
                    ON Sales.user_id = Users.user_id
                ORDER BY {order_by};

-- Query 46
SELECT 1 FROM Categories WHERE LOWER(category_name)=LOWER(%s)

-- Query 47
SELECT * FROM Categories WHERE category_id = %s

-- Query 48
SELECT * FROM Categories WHERE LOWER(category_name)=LOWER(%s)

-- Query 49
SELECT * FROM Categories WHERE category_id = %s;

-- Query 50
DELETE FROM Categories WHERE category_id =%s;

-- Query 51
SELECT 1 FROM Suppliers WHERE LOWER(supplier_name)=LOWER(%s)

-- Query 52
SELECT 1 FROM {table_name} WHERE phone_number = %s

-- Query 53
SELECT 1 FROM {table} WHERE LOWER(email)=LOWER(%s)

-- Query 54
INSERT INTO Suppliers (supplier_name, address, phone_number, email, contact_person) VALUES (%s, %s, %s, %s, %s)

-- Query 55
SELECT * FROM Suppliers WHERE supplier_id = %s;

-- Query 56
SELECT * FROM Suppliers WHERE LOWER(supplier_name)=LOWER(%s)

-- Query 57
SELECT * FROM Suppliers WHERE supplier_id = %s

-- Query 58
SELECT 1 FROM Products WHERE LOWER(product_name)=LOWER(%s)

-- Query 59
SELECT category_name FROM Categories WHERE category_id = %s

-- Query 60
SELECT supplier_name FROM Suppliers WHERE supplier_id = %s

