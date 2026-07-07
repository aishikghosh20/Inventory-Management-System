Smart Inventory Management System

Overview

The Smart Inventory Management System is a Python and MySQL-based application designed to help businesses efficiently manage inventory, suppliers, customers, purchases, and sales through a modular command-line interface.

This project is being developed as part of my software engineering portfolio to demonstrate database design, SQL, Python programming, and clean software architecture.

---

Features

- User Authentication
- Product Management (CRUD)
- Category Management
- Supplier Management
- Customer Management
- Purchase Management
- Sales Management
- Inventory Tracking
- Low Stock Alerts
- Product Search & Filtering
- Reports & Analytics

---

Tech Stack

- Python
- MySQL
- MySQL Connector for Python
- Python Dotenv
- Git & GitHub
- Visual Studio Code

---

Project Structure

Smart-Inventory-Management-System/
│
├── .venv/
├── modules/
├── sql/
├── docs/
├── screenshots/
├── .env.example
├── config.py
├── database.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

Folder Description

Folder / File| Description
".venv/"| Virtual environment (not uploaded to GitHub)
"modules/"| Contains all Python modules (Products, Sales, Suppliers, etc.)
"sql/"| SQL scripts including schema, sample data, procedures, triggers and views
"docs/"| ER diagrams and project documentation
"screenshots/"| Images used in the README
".env.example"| Example environment configuration
"config.py"| Loads environment variables
"database.py"| Handles the MySQL database connection
"main.py"| Entry point of the application

---

Database Concepts

- Relational Database Design
- Primary Keys
- Foreign Keys
- Constraints
- CRUD Operations
- JOINs
- Aggregate Functions
- GROUP BY
- HAVING
- Subqueries
- Views
- Stored Procedures
- Triggers

---

Installation

1. Clone the Repository

git clone <repository-url>
cd Smart-Inventory-Management-System

---

2. Create a Virtual Environment

python -m venv .venv

Activate the Environment

Windows (Command Prompt)

.venv\Scripts\activate

Windows (PowerShell)

.\.venv\Scripts\Activate.ps1

---

3. Install Dependencies

pip install -r requirements.txt

---

4. Configure Environment Variables

Copy

.env.example

to

.env

Then edit the ".env" file with your own MySQL credentials.

Example:

DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=inventory_management

«Never commit your ".env" file to GitHub.»

---

5. Create the Database

Run the SQL scripts located inside the "sql/" folder.

1. "schema.sql" – Creates all database tables.
2. "sample_data.sql" – Inserts sample data (optional).

---

6. Run the Application

python main.py

---

Requirements

Install all required packages with:

pip install -r requirements.txt

Current dependencies:

- mysql-connector-python
- python-dotenv
- tabulate
- colorama

---

Future Improvements

- Password Hashing
- CSV Export
- Audit Logging
- Enhanced Terminal UI
- Desktop GUI using PySide6
- Flask Web Application

---

Project Status

🚧 Currently Under Development

This project is being developed in phases, beginning with database planning and SQL implementation before integrating Python modules.

---

License

This project is licensed under the Apache License 2.0.

---

Author

Aishik Ghosh