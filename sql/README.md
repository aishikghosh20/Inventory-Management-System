# SQL

This folder contains all SQL scripts required to initialize and manage the Inventory Management System database.

---

## Files

### schema.sql

Creates the complete relational database including:

- Users
- Categories
- Suppliers
- Products
- Customers
- Purchases
- Purchase Items
- Sales
- Sale Items

The schema includes:

- Primary Keys
- Foreign Keys
- UNIQUE Constraints
- ENUM fields
- CHECK Constraints
- Automatic timestamps
- Transaction support

---

## Foreign Key Design

The database is designed to preserve business data integrity.

### RESTRICT

Used for business entities.

Examples:

- Categories → Products
- Suppliers → Products
- Products → Sale Items
- Products → Purchase Items
- Users → Sales
- Users → Purchases

This prevents accidental deletion of important records.

### CASCADE

Used for transaction detail tables.

Examples:

- Purchases → Purchase_Items
- Sales → Sale_Items

Deleting a transaction automatically removes its corresponding line items.

---

## Transactions

The schema executes inside a transaction.

```sql
SET autocommit = 0;

START TRANSACTION;

...

COMMIT;
```

---

## Current Status

### Completed

- Database Schema
- Authentication
- User Roles
- Categories CRUD

### Planned

- Suppliers CRUD
- Customers CRUD
- Products CRUD
- Purchases
- Sales
- Reports