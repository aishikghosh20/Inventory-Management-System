# 📦 Inventory Management System v1.0

<p align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange?logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-success)
![Version](https://img.shields.io/badge/Version-1.0-blue)

</p>

---

# Overview

Inventory Management System is a terminal-based desktop application developed in Python using MySQL as the backend database. It provides businesses with an efficient way to manage products, suppliers, customers, purchases, sales, inventory, reports, and user accounts through a secure authentication system.

The application has been designed with a modular architecture, emphasizing code organization, maintainability, and scalability. It supports role-based access control, complete CRUD operations, transaction-safe purchase and sales processing, and detailed business reports.

This project serves as both a practical inventory management solution and a demonstration of database design, Python programming, and software engineering principles.

---

# Features

## Authentication

- Secure login system
- Password hashing using bcrypt
- Password visibility toggle
- Administrator account creation
- Role-Based Access Control (RBAC)
- Secure password change
- Username validation

---

## Category Management

- Add Categories
- View Categories
- Search Categories
  - Search by ID
  - Search by Name
- Update Categories
- Delete Categories
- Duplicate validation

---

## Product Management

- Add Products
- View Products
- Search Products
- Update Products
- Delete Products

Validation includes

- Duplicate products
- Invalid prices
- Invalid stock quantities
- Category validation

---

## Supplier Management

- Add Suppliers
- View Suppliers
- Search Suppliers
- Update Suppliers
- Delete Suppliers

Validation

- Duplicate phone numbers
- Duplicate email addresses
- Email validation
- Phone validation

Optional

- Email
- Address

---

## Customer Management

- Add Customers
- View Customers
- Search Customers
- Update Customers
- Delete Customers

Validation

- Duplicate phone numbers
- Duplicate emails
- Email validation
- Phone validation

Optional

- Email
- Address

---

## Purchase Management

- Add Purchase
- Purchase History
- Search Purchase

Supports

- Multiple products per purchase
- Automatic stock increment
- Purchase totals
- Purchase item history
- Transaction support

---

## Sales Management

- Add Sale
- Sales History
- Search Sale

Supports

- Multiple products per sale
- Automatic stock deduction
- Sales totals
- Sales item history
- Transaction support

---

## Reports

Generate

- Inventory Report
- Sales Report
- Purchase Report
- Profit Report
- Low Stock Report

Reports include

- Inventory valuation
- Daily sales
- Monthly sales
- Daily purchases
- Monthly purchases
- Revenue
- Cost
- Profit
- Low stock products

---

## Settings

### Password Management

- Change Password
- Password verification

### User Management

- Add Users
- View Users
- Search Users
- Update Users
- Delete Users

### Role Management

- View roles
- Users by role
- Administrator management

### Database Information

Displays

- Database Name
- MySQL Version
- Total Users
- Total Categories
- Total Products
- Total Suppliers
- Total Customers
- Total Purchases
- Total Sales
- Inventory Value

---

# Technologies Used

- Python 3.14
- MySQL
- mysql-connector-python
- bcrypt
- python-dotenv
- pwinput
- PyInstaller

---

# Project Structure

```
Inventory Management System
│
├── assets/
│   └── inventory.ico
│
├── docs/
│   └── build_log/
│
├── sql/
│   ├── schema.sql
│   ├── crud.sql
│   ├── reports.sql
│   ├── settings.sql
│   ├── database_startup.sql
│   ├── user_authentication.sql
│   └── README.md
│
├── authentication.py
├── crud.py
├── reports.py
├── settings.py
├── database.py
├── initializing_db.py
├── setup.py
├── config.py
├── main.py
│
├── LICENSE
└── README.md
```

---

# Database Design

The project uses a relational MySQL database.

Tables

- Users
- Categories
- Products
- Suppliers
- Customers
- Purchases
- Purchase_Items
- Sales
- Sale_Items

Features

- Primary Keys
- Foreign Keys
- Constraints
- Transactions
- ENUM Fields
- Default Values

---

# Installation

## Method 1 — Using the Pre-built Executable (Recommended)

### Step 1

Download the latest release from the GitHub Releases page.

Extract the ZIP archive.

---

### Step 2

Ensure **MySQL Server 8.0 or later** is installed and running.

If you do not have MySQL installed:

Download MySQL Community Server

https://dev.mysql.com/downloads/mysql/

or install MySQL Installer for Windows

https://dev.mysql.com/downloads/installer/

During installation:

- Install MySQL Server
- Install MySQL Workbench (optional but recommended)
- Remember the root password
- Keep the default port (3306)

After installation, verify that the MySQL service is running.

---

### Step 3

Run

```
Inventory Management System.exe
```

On first launch the application automatically starts the setup wizard.

You will be asked for

- MySQL Host
- MySQL Port
- Username
- Password
- Database Name

Example

```
Host:
localhost

Port:
3306

Username:
root

Password:
********

Database:
inventory_management
```

The application automatically

- Creates the configuration file
- Connects to MySQL
- Creates the database
- Creates all required tables
- Starts the login system

No manual SQL execution is required.

---

# Method 2 — Run From Source Code

Clone the repository

```bash
git clone https://github.com/<your-username>/Inventory-Management-System.git
```

Open the project

```bash
cd Inventory-Management-System
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

The setup wizard will launch automatically on first startup.

---

# First Login

During the initial setup, the application will prompt you to create the first administrator account.

This administrator has full access to all features including:

- User Management
- Role Management
- Reports
- Settings

---

# Security

Implemented

- Password hashing using bcrypt
- Parameterized SQL queries
- SQL Injection protection
- Role-Based Access Control
- Duplicate validation
- Foreign Key Constraints
- Transaction support

---

# Reports

The application can generate

- Inventory Reports
- Sales Reports
- Purchase Reports
- Profit Reports
- Low Stock Reports

---

# SQL Documentation

All SQL queries used by the application have been documented.

```
sql/
│
├── schema.sql
├── database_startup.sql
├── user_authentication.sql
├── crud.sql
├── reports.sql
├── settings.sql
└── README.md
```

This makes it easy to study the database layer independently from the Python implementation.

---

# Future Improvements

Planned for Version 1.1

- PDF Export
- Excel Export
- Backup & Restore
- Dashboard Improvements
- Search Filters
- Graphical Charts
- Advanced Reports
- Performance Optimizations

---

# Screenshots

Screenshots will be added in future releases.

---

# License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

# Acknowledgements

- Python Software Foundation
- MySQL
- PyInstaller
- bcrypt
- python-dotenv

---

# Developer

**Aishik Ghosh**

GitHub:

https://github.com/aishikghosh20

---

# Icon Attribution

The application icon was created by **Freepik** and obtained from **Flaticon**.

Icon Page:
https://www.flaticon.com/free-icon/monitoring_12062370?term=inventory+management&related_id=12062370

Flaticon:
https://www.flaticon.com/

The icon is used under the applicable Flaticon license.


# Version

Current Release

**Inventory Management System v1.0**

Stable Release

July 2026