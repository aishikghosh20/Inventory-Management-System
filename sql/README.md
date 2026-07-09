

https://github.com/user-attachments/assets/37fce9b1-0c19-44e0-84c3-92c699179d23

# SQL Folder

This folder contains the SQL scripts required to initialize and maintain the Inventory Management System database.

---

## Contents

### schema.sql

Creates the complete database schema.

Includes:

- Categories
- Suppliers
- Products
- Customers
- Purchases
- Purchase Items
- Sales
- Sale Items
- Users

---

### database_startup.sql

Contains database initialization scripts.

Responsibilities:

- Create the Inventory Management database
- Verify database existence

---

### user_authentication.sql

Contains all SQL queries related to administrator authentication.

Includes:

- Administrator existence check
- Username availability check
- Email availability check
- Phone number availability check
- User login query
- Administrator account creation

---

## Authentication

Passwords are **never stored in plain text**.

The application uses:

- bcrypt password hashing
- Parameterized SQL queries
- Secure password verification using `bcrypt.checkpw()`

---

## Database Structure

```
Inventory Management
│
├── Categories
├── Suppliers
├── Products
├── Customers
├── Purchases
├── Purchase_Items
├── Sales
├── Sale_Items
└── Users
```

---

## Demonstration

This folder includes a demonstration video showing:

- Automatic database creation
- Automatic table creation
- Administrator account creation
- Secure login
- Authentication workflow

```

---

## Current Version

**v0.4**

Implemented:

- Automatic database initialization
- Automatic schema creation
- Authentication system
- Secure password hashing
- Administrator setup
- Administrator login

Next Version:

**v0.5 — Inventory Management Dashboard & CRUD Operations**