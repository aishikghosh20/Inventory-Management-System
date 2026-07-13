-- Inventory Management System
-- reports.sql
-- SQL queries extracted from reports.py

-- Query 1
SELECT
                    Products.product_id,
                    Products.product_name,
                    Categories.category_name,
                    Suppliers.supplier_name,
                    Products.quantity,
                    Products.buying_price,
                    Products.selling_price,
                    (
                        Products.quantity *
                        Products.buying_price
                    ) AS inventory_value,
                    Products.reorder_level
                FROM Products

                LEFT JOIN Categories
                    ON Products.category_id = Categories.category_id

                LEFT JOIN Suppliers
                    ON Products.supplier_id = Suppliers.supplier_id

                ORDER BY Products.product_name ASC;

-- Query 2
SELECT
                    COUNT(*),
                    IFNULL(SUM(total_amount),0),
                    IFNULL(AVG(total_amount),0),
                    IFNULL(MAX(total_amount),0),
                    IFNULL(MIN(total_amount),0)
                FROM Sales
                WHERE status = 'Completed';

-- Query 3
SELECT
                    IFNULL(SUM(total_amount),0)
                FROM Sales
                WHERE
                    DATE(sale_date)=CURDATE()
                    AND status='Completed';

-- Query 4
SELECT
                    IFNULL(SUM(total_amount),0)
                FROM Sales
                WHERE
                    MONTH(sale_date)=MONTH(CURDATE())
                    AND YEAR(sale_date)=YEAR(CURDATE())
                    AND status='Completed';

-- Query 5
SELECT
                    COUNT(*),
                    IFNULL(SUM(total_amount),0),
                    IFNULL(AVG(total_amount),0),
                    IFNULL(MAX(total_amount),0),
                    IFNULL(MIN(total_amount),0)
                FROM Purchases
                WHERE status = 'Completed';

-- Query 6
SELECT
                    IFNULL(SUM(total_amount),0)
                FROM Purchases
                WHERE
                    DATE(purchase_date)=CURDATE()
                    AND status='Completed';

-- Query 7
SELECT
                    IFNULL(SUM(total_amount),0)
                FROM Purchases
                WHERE
                    MONTH(purchase_date)=MONTH(CURDATE())
                    AND YEAR(purchase_date)=YEAR(CURDATE())
                    AND status='Completed';

-- Query 8
SELECT
                    IFNULL(
                        SUM(
                            (Products.selling_price - Products.buying_price)
                            * Sale_items.quantity
                        ),
                        0
                    ) AS gross_profit,

                    IFNULL(
                        SUM(
                            Products.buying_price
                            * Sale_items.quantity
                        ),
                        0
                    ) AS cost_of_goods_sold,

                    IFNULL(
                        SUM(
                            Products.selling_price
                            * Sale_items.quantity
                        ),
                        0
                    ) AS revenue

                FROM Sale_items

                INNER JOIN Products
                    ON Sale_items.product_id = Products.product_id

                INNER JOIN Sales
                    ON Sale_items.sale_id = Sales.sale_id

                WHERE Sales.status = 'Completed';

-- Query 9
SELECT
                    Products.product_id,
                    Products.product_name,
                    Suppliers.supplier_name,
                    Products.quantity,
                    Products.reorder_level
                FROM Products

                LEFT JOIN Suppliers
                    ON Products.supplier_id = Suppliers.supplier_id

                WHERE Products.quantity <= Products.reorder_level

                ORDER BY
                    Products.quantity ASC,
                    Products.product_name ASC;

