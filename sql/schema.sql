Create Table IF NOT EXISTS Users(
  user_id int AUTO_INCREMENT Primary Key , 
  username varchar (50) UNIQUE NOT NULL,
  password_hash varchar (255) NOT NULL,
  first_name varchar (50),
  last_name varchar(50),
  email varchar(255) UNIQUE,
  phone_number varchar(20) UNIQUE,
  
  role  ENUM(
      "Administrator",
      "Manager",
      "Sales Staff",
      "Inventory Staff",
      "Viewer"
  ) NOT NULL DEFAULT "Administrator",

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE Table IF NOT EXISTS Categories(
  category_id int AUTO_INCREMENT PRIMARY KEY,
  category_name varchar(50) UNIQUE NOT NULL,
  description text NULL
);

CREATE Table IF NOT EXISTS Suppliers(
  supplier_id int AUTO_INCREMENT PRIMARY KEY,
  company_name varchar(100) NOT NULL,
  contact_person varchar(50),
  phone_number varchar(50) UNIQUE,
  email varchar(50) UNIQUE,
  address varchar(150) ,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE Table IF NOT EXISTS Customers(
  customer_id int AUTO_INCREMENT PRIMARY KEY,
  first_name varchar(50),
  last_name varchar(50),
  phone_number varchar(50) UNIQUE,
  email varchar(50) UNIQUE,
  address varchar(150),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE Table IF NOT EXISTS Products(
  product_id int AUTO_INCREMENT PRIMARY KEY,
  product_name varchar(50) NOT NULL,
  category_id int ,
  supplier_id int ,
  buying_price decimal(10,2) CHECK (buying_price >= 0),
  selling_price decimal(10,2)  CHECK (selling_price >= 0),
  quantity int NOT NULL DEFAULT 0 CHECK (quantity >= 0),
  reorder_level int NOT NULL DEFAULT 10,
  description text NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_products_category
  FOREIGN KEY (category_id)
  REFERENCES Categories(category_id) 
  ON DELETE SET NULL
  ON UPDATE CASCADE,

  CONSTRAINT fk_product_supplier
  FOREIGN KEY (supplier_id)
  REFERENCES Suppliers(supplier_id) 
  ON DELETE SET NULL
  ON UPDATE CASCADE
);

CREATE Table IF NOT EXISTS Purchases(
  purchase_id int AUTO_INCREMENT PRIMARY KEY,
  supplier_id int ,
  user_id int,
  purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_amount decimal(10,2),

  CONSTRAINT fk_purchase_supplier
  FOREIGN KEY (supplier_id)
  REFERENCES Suppliers(supplier_id) 
  ON DELETE SET NULL
  ON UPDATE CASCADE,

  CONSTRAINT fk_purchase_user
  FOREIGN KEY (user_id)
  REFERENCES Users(user_id)
  ON DELETE SET NULL
  ON UPDATE CASCADE
);

CREATE Table IF NOT EXISTS Purchase_items(
  purchase_item_id int AUTO_INCREMENT PRIMARY KEY,
  purchase_id int,
  product_id int,
  quantity int NOT NULL DEFAULT 0  CHECK (quantity >= 0),
  unit_price decimal(10,2) CHECK (unit_price >= 0),
  subtotal decimal(10,2),

  CONSTRAINT fk_item_productid
  FOREIGN KEY (product_id)
  REFERENCES Products(product_id)
  ON DELETE SET NULL
  ON UPDATE CASCADE,

  CONSTRAINT fk_item_purchaseid
  FOREIGN KEY (purchase_id)
  REFERENCES Purchases(purchase_id)
  ON DELETE SET NULL
  ON UPDATE CASCADE
);

CREATE Table IF NOT EXISTS Sales(
  sale_id int AUTO_INCREMENT PRIMARY KEY,
  customer_id int,
  user_id int,
  sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_amount decimal(10,2),

  CONSTRAINT fk_sales_customer
  FOREIGN KEY (customer_id)
  REFERENCES Customers(customer_id)
  ON DELETE SET NULL
  ON UPDATE CASCADE,

  CONSTRAINT fk_sales_userid
  FOREIGN KEY (user_id)
  REFERENCES Users(user_id)
  ON DELETE SET NULL
  ON UPDATE CASCADE
);

CREATE Table IF NOT EXISTS Sale_items(
  item_id int AUTO_INCREMENT PRIMARY KEY,
  sale_id int,
  product_id int,
  quantity int NOT NULL DEFAULT 0 CHECK (quantity >= 0),
  unit_price decimal(10,2) CHECK (unit_price >= 0),
  subtotal decimal(10,2),

  CONSTRAINT fk_saleitem_productid
  FOREIGN KEY (product_id)
  REFERENCES Products(product_id)
  ON DELETE SET NULL
  ON UPDATE CASCADE,

  CONSTRAINT fk_saleitem_saleid
  FOREIGN KEY (sale_id)
  REFERENCES Sales(sale_id)
  ON DELETE SET NULL
  ON UPDATE CASCADE
);

