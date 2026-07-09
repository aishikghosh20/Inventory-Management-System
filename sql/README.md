# Smart Inventory Management System
## Database Structure

This folder contains all SQL files required to initialize the application's database.

## Files

### schema.sql
Contains the complete database schema including:

- Database tables
- Primary Keys
- Foreign Keys
- Constraints
- Default values
- Timestamp fields

### database_startup.sql

Responsible for creating the application database if it does not already exist.

---

## Database Tables

- Users
- Categories
- Suppliers
- Products
- Customers
- Purchases
- Purchase_Items
- Sales
- Sale_Items

---

## Features

- Fully normalized relational database
- Referential integrity
- Foreign key constraints
- Automatic timestamps
- CHECK constraints
- Safe initialization using `CREATE TABLE IF NOT EXISTS`

---

## Startup Process

The application automatically:

1. Connects to MySQL
2. Checks whether the database exists
3. Creates the database if necessary
4. Connects to the database
5. Verifies all required tables
6. Creates missing tables
7. Launches the application

No manual SQL execution is required by the user.