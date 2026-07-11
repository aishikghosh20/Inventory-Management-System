SELECT 1 FROM Categories WHERE LOWER(category_name) = LOWER(%s);

SELECT category_id, category_name
FROM Categories
ORDER BY {order_by};

SELECT *
FROM Categories
WHERE category_id = %s;

SELECT * 
FROM Categories 
WHERE LOWER(category_name)=LOWER(%s);

UPDATE Categories 
SET category_name =%s, 
    description =%s 
WHERE category_id = %s;

UPDATE Categories 
SET category_name =%s
WHERE category_id = %s;


UPDATE Categories 
SET description =%s 
WHERE category_id = %s;

DELETE FROM Categories
WHERE category_id = %s;


