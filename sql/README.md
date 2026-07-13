# SQL Folder

This folder contains all the SQL queries used throughout the **Inventory Management System v1.0**. The queries have been separated by functionality to make the project easier to understand, maintain, and debug.

---

## 📂 Files

### 📄 schema.sql
**Purpose:**
Contains the complete database structure for the project.

**Includes:**
- Database creation
- All table definitions
- Primary Keys
- Foreign Keys
- Constraints
- Default values
- ENUM definitions
- CHECK constraints

**Used During**
- First-time project setup

---

### 📄 database_startup.sql
**Purpose:**
Contains all SQL queries executed when the application starts.

**Includes:**
- Database existence checks
- Database selection
- Table existence checks
- Initial setup queries

**Used During**
- Application startup
- Initial database initialization

---

### 📄 user_authentication.sql
**Purpose:**
Contains all SQL queries related to authentication and login.

**Includes:**
- User login
- Password verification
- Password hashing support
- Current user retrieval
- Administrator account creation
- User validation

**Related Python Module**
- authentication.py

---

### 📄 crud.sql
**Purpose:**
Contains every CRUD (Create, Read, Update, Delete) query used throughout the Inventory Management System.

**Includes**

#### Categories
- Add Category
- View Categories
- Search Category
- Update Category
- Delete Category

#### Products
- Add Product
- View Products
- Search Product
- Update Product
- Delete Product
- Stock Update

#### Suppliers
- Add Supplier
- View Suppliers
- Search Supplier
- Update Supplier
- Delete Supplier

#### Customers
- Add Customer
- View Customers
- Search Customer
- Update Customer
- Delete Customer

#### Purchases
- Add Purchase
- Purchase History
- Search Purchase
- Purchase Items
- Stock Increase

#### Sales
- Add Sale
- Sales History
- Search Sale
- Sale Items
- Stock Reduction

---

### 📄 reports.sql
**Purpose:**
Contains every SQL query used to generate reports.

**Includes**

- Inventory Report
- Sales Report
- Purchase Report
- Profit Report
- Low Stock Report

The queries calculate totals, averages, revenue, costs, profits, inventory values and low-stock information.

**Related Python Module**
- reports.py

---

### 📄 settings.sql
**Purpose:**
Contains all SQL queries related to system administration and settings.

**Includes**

### User Management
- Add User
- View Users
- Search User
- Update User
- Delete User

### Password Management
- Verify Current Password
- Change Password

### Role Management
- View Roles
- Users By Role
- Administrator Count

### Database Information
- Database Name
- MySQL Version
- Total Users
- Total Products
- Total Categories
- Total Suppliers
- Total Customers
- Total Purchases
- Total Sales
- Inventory Value

**Related Python Module**
- settings.py

---

# Folder Structure

```
SQL/
│
├── schema.sql
├── database_startup.sql
├── user_authentication.sql
├── crud.sql
├── reports.sql
├── settings.sql
└── README.md
```

---

# Purpose

Separating the SQL queries into dedicated files provides several advantages:

- Easier debugging
- Better project organization
- Improved readability
- Simplified maintenance
- Helpful reference for learning SQL
- Clear separation between Python logic and SQL statements

Although the application executes these queries directly through Python using MySQL Connector, keeping them in separate files makes the database layer easier to understand and serves as useful documentation for future development.

---

**Inventory Management System v1.0**

**Developed by:** Aishik Ghosh