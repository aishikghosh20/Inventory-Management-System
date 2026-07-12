# 🗄️ SQL

This folder contains all SQL scripts used by the **Inventory Management System**. The scripts are organized according to their purpose, making it easier to understand the database structure, initialization process, authentication workflow, and CRUD operations.

---

## 📂 Folder Structure

```
SQL/
│
├── schema.sql
├── database_startup.sql
├── user_authentication.sql
├── crud.sql
└── README.md
```

---

## 📄 Files

### schema.sql

Contains the complete database schema for the project.

This file creates:

- Database
- Categories
- Suppliers
- Products
- Customers
- Users
- Purchases
- Purchase_Items
- Sales
- Sale_Items

It also defines:

- Primary Keys
- Foreign Keys
- Constraints
- Default Values
- ENUM fields
- CHECK Constraints
- Cascading Rules

---

### database_startup.sql

Contains the SQL queries executed during application startup.

Responsibilities include:

- Checking database existence
- Creating the database (if required)
- Creating missing tables
- Initializing default settings
- Preparing the application for first-time use

---

### user_authentication.sql

Contains every SQL query related to authentication.

Includes:

- User Registration
- User Login
- Password Verification
- Password Updates
- User Validation
- User Management

Passwords are securely stored using **bcrypt hashing** in the Python application before being saved to the database.

---

### crud.sql

Contains the SQL queries used throughout the application for CRUD (Create, Read, Update and Delete) operations.

Covered modules include:

- Categories
- Suppliers
- Products
- Customers
- Purchases
- Purchase_Items
- Sales
- Sale_Items
- Users

Operations include:

- INSERT
- SELECT
- UPDATE
- DELETE
- JOIN Queries
- Search Queries
- Sorting Queries
- Aggregate Queries
- Stock Updates

---

## 🗃 Database Design

The project follows a **relational database design**.

Relationships include:

```
Categories
     │
     ▼
 Products ◄──────────────┐
     ▲                   │
     │                   │
Suppliers                │
     │                   │
     ▼                   │
 Purchases               │
     │                   │
     ▼                   │
Purchase_Items───────────┘


Customers
     │
     ▼
   Sales
     │
     ▼
 Sale_Items
     ▲
     │
 Products


Users
 ├────────► Purchases
 └────────► Sales
```

---

## 🔒 Database Features

The database uses several mechanisms to maintain integrity:

- Primary Keys
- Foreign Keys
- UNIQUE Constraints
- CHECK Constraints
- ENUM Columns
- Default Values
- Timestamp Tracking
- ON UPDATE CASCADE
- ON DELETE RESTRICT
- ON DELETE CASCADE (where appropriate)

---

## ⚙ Transaction Management

Database write operations are performed using transactions.

Typical workflow:

1. Execute SQL statements
2. Commit on success
3. Rollback on failure
4. Display appropriate error messages

This ensures database consistency even if an operation fails midway.

---

## 📦 Inventory Logic

The application automatically synchronizes stock levels.

### Purchases

```
Product Quantity += Purchased Quantity
```

### Sales

```
Product Quantity -= Sold Quantity
```

Sales are validated to ensure sufficient stock exists before completing the transaction.

---

## 🛠 Technologies

- MySQL
- MySQL Connector/Python
- SQL (DDL & DML)

---

## 📌 Current Status

**Version:** v0.6

Completed modules:

- ✅ Users
- ✅ Categories
- ✅ Suppliers
- ✅ Products
- ✅ Customers
- ✅ Purchases
- ✅ Sales

The SQL layer now fully supports the core functionality of the Inventory Management System and provides the foundation for future modules such as Reports, Dashboard, and Analytics.