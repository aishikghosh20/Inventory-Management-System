-- To count all the users in the table
SELECT COUNT(*) FROM USERS;

-- Returns 1 if the username exists
SELECT 1 FROM USERS WHERE username= %s;

-- Returns 1 if the email exists
SELECT 1 FROM USERS WHERE email= %s;

-- Returns 1 if the phone numnber exists
SELECT 1 FROM USERS WHERE phone_number= %s;

-- To initialize the user
INSERT INTO Users
(
    username,
    password_hash,
    first_name,
    last_name,
    email,
    phone_number
)
VALUES (%s, %s, %s, %s, %s, %s);

SELECT user_id, first_name, password_hash
FROM USERS 
WHERE username= %s;
