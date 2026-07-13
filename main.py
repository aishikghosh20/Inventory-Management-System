import os
from time import sleep
from database import connect_to_server, connect_using_env
from setup import setup_check, setup_wizard, save_config
from intializing_db import database_exists, create_database, connect_database, tables_exists, tables_create
from authentication import count_users, create_user, user_login
from crud import add_product, add_category, view_category, search_categories, update_category, delete_category
from crud import add_supplier, view_suppliers, search_supplier, update_supplier, delete_supplier, view_products, delete_product, search_products,  update_product
from crud import add_customer, view_customers, search_customers ,delete_customer, update_customer
from crud import add_purchase, purchase_history, search_purchase, add_sale, sales_history, search_sale
from reports import inventory_report, sales_report, purchase_report, low_stock_report, profit_report
from settings import change_password, manage_users, manage_roles, db_info

def clear(): # To clear the screen
    os.system("cls")
    sleep(0.2)
    
def title(text="INVENTORY MANAGEMENT SYSTEM", width=42):
    print(f"\033[36m┌{'─' * width}┐\033[0m")
    print(
        f"\033[36m│\033[0m"
        f"\033[1;97m{text.center(width)}\033[0m"
        f"\033[36m│\033[0m"
    )
    print(f"\033[36m└{'─' * width}┘\033[0m")

def exit_app(connection):
    print(f"\033[1;93mExiting the program...\033[0m")
    sleep(1)
    print("\n\033[1;95m!!😊Thank you for using!!\033[0m")
    sleep(0.5)
    print("\033[1;95mCoded by: \033[1;97mAishik Ghosh\033[0m")
    sleep(0.5)
    input("\nPress Enter to Exit...")
    if connection:
        connection.close()
    exit()
   
def breadcrumb(*paths):
    print("\033[1;96m📍 " + ">".join(paths) + "\033[0m")


def products_menu(connection):
    while True:
        clear()
        title("📦 PRODUCTS")
        sleep(0.2)
        breadcrumb("Home", "Products")
        sleep(0.5)
        print(f"{" ":<5}\033[1;97m[1] ➕  Add Product\n{" ":<5}[2] 📋 View Products\n{" ":<5}[3] 🔍 Search Product\n{" ":<5}[4] ✏️ Update Product\n{" ":<5}[5] 🗑️ Delete Product\n\n{" ":<5}[0] Back\033[0m\n")
        
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice >  5 or choice < 0:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

        if choice ==0:
            return
        elif choice == 1:
            print("\n\033[1;97mInitializing product creation...")
            sleep(0.5)
            add_product(connection)
            continue
        elif choice == 2:
            print("\n\033[1;97mLoading products...")
            sleep(0.5)
            view_products(connection)
            continue
        elif choice == 3:
            print("\n\033[1;97mLoading search bar...")
            sleep(0.5)
            search_products(connection)
            continue
        elif choice == 4:
            print("\n\033[1;97mUpdating product...")
            sleep(0.5)
            update_product(connection)
            continue
        elif choice == 5:
            print("\n\033[1;97mDeleting product...")
            sleep(0.5)
            delete_product(connection)
            continue
    
        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

def categories_menu(connection):
    while True:
        clear()
        title("🏷️ CATEGORIES")
        sleep(0.2)
        breadcrumb("Home", "Categories")
        sleep(0.5)
        print(f"{" ":<5}\033[1;97m[1] ➕  Add Category\n{" ":<5}[2] 📋 View Categories\n{" ":<5}[3] 🔍 Search Category\n{" ":<5}[4] ✏️ Update Category\n{" ":<5}[5] 🗑️ Delete Category\n\n{" ":<5}[0] Back\033[0m\n")
        
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice ==0:
            return
        elif choice == 1:
            print("\n\033[1;97mInitializing category creation...")
            sleep(0.5)
            add_category(connection)
            continue
        elif choice == 2:
            print("\n\033[1;97mLoading categories...")
            sleep(0.5)
            view_category(connection)
            continue
        elif choice == 3:
            print("\n\033[1;97mLoading search bar...")
            sleep(0.5)
            search_categories(connection)
            continue
        elif choice == 4:
            print("\n\033[1;97mUpdating category...")
            sleep(0.5)
            update_category(connection)
            continue
        elif choice == 5:
            print("\n\033[1;97mDeleting category...")
            sleep(0.5)
            delete_category(connection)
            continue
    
        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

def suppliers_menu(connection):
    while True:
        clear()
        title("🚚 SUPPLIERS")
        sleep(0.2)
        breadcrumb("Home", "Suppliers")
        sleep(0.5)
        print(f"{" ":<5}\033[1;97m[1] ➕  Add Supplier\n{" ":<5}[2] 📋 View Suppliers\n{" ":<5}[3] 🔍 Search Supplier\n{" ":<5}[4] ✏️ Update Supplier\n{" ":<5}[5] 🗑️ Delete Supplier\n\n{" ":<5}[0] Back\033[0m\n")
        
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue
        
        if choice ==0:
            return
        elif choice == 1:
            print("\n\033[1;97mInitializing supplier addition...")
            sleep(0.5)
            add_supplier(connection)
            continue
        elif choice == 2:
            print("\n\033[1;97mLoading Suppliers...")
            sleep(0.5)
            view_suppliers(connection)
            continue
        elif choice == 3:
            print("\n\033[1;97mLoading search bar...")
            sleep(0.5)
            search_supplier(connection)
            continue
        elif choice == 4:
            print("\n\033[1;97mUpdating supplier...")
            sleep(0.5)
            update_supplier(connection)
            continue
        elif choice == 5:
            print("\n\033[1;97mDeleting supplier...")
            sleep(0.5)
            delete_supplier(connection)
            continue
    
        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue
          
def customers_menu(connection):
    while True:
        clear()
        title("👥 CUSTOMERS")
        sleep(0.2)
        breadcrumb("Home", "Customers")
        sleep(0.5)
        print(f"{" ":<5}\033[1;97m[1] ➕  Add Customer\n{" ":<5}[2] 📋 View Customers\n{" ":<5}[3] 🔍 Search Customer\n{" ":<5}[4] ✏️ Update Customer\n{" ":<5}[5] 🗑️ Delete Customer\n\n{" ":<5}[0] Back\033[0m\n")
        
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice >  5 or choice < 0:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

        if choice ==0:
            return
        elif choice == 1:
            print("\n\033[1;97mInitializing customer addition...")
            sleep(0.5)
            add_customer(connection)
            continue
        elif choice == 2:
            print("\n\033[1;97mViewing customers...")
            sleep(0.5)
            view_customers(connection)
            continue
        elif choice == 3:
            print("\n\033[1;97mLoading search bar...")
            sleep(0.5)
            search_customers(connection)
            continue
        elif choice == 4:
            print("\n\033[1;97mUpdating customer...")
            sleep(0.5)
            update_customer(connection)
            continue
        elif choice == 5:
            print("\n\033[1;97mDeleting customer...")
            sleep(0.5)
            delete_customer(connection)
            continue
    
        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue
    
def purchases_menu(connection, user_id):
    while True:
        clear()
        title("🛒 PURCHASES")
        sleep(0.2)
        breadcrumb("Home", "Purchases")
        sleep(0.5)
        print(f"{" ":<5}\033[1;97m[1] ➕  New Purchase\n{" ":<5}[2] 📋 Purchase History\n{" ":<5}[3] 🔍 Search Purchase\n\n{" ":<5}[0] ← Back\033[0m\n")
        
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice >  3 or choice < 0:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

        if choice ==0:
                return
        elif choice == 1:
            print("\n\033[1;97mInitializing purchase addition...")
            sleep(0.5)
            add_purchase(connection, user_id)
            continue
        elif choice == 2:
            print("\n\033[1;97mViewing purchase history...")
            sleep(0.5)
            purchase_history(connection)
            continue
        elif choice == 3:
            print("\n\033[1;97mLoading search bar...")
            sleep(0.5)
            search_purchase(connection)
            continue    
        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

def sales_menu(connection, user_id):
    while True:
        clear()
        title("💰 SALES")
        sleep(0.2)
        breadcrumb("Home", "Sales")
        sleep(0.5)
        print(f"{" ":<5}\033[1;97m[1] ➕  New Sale\n{" ":<5}[2] 📋 Sales History\n{" ":<5}[3] 🔍 Search Sale\n\n{" ":<5}[0] Back\033[0m\n")
        
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice >  3 or choice < 0:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

        if choice ==0:
                return
        elif choice == 1:
            print("\n\033[1;97mInitializing sale addition...")
            sleep(0.5)
            add_sale(connection, user_id)
            continue
        elif choice == 2:
            print("\n\033[1;97mViewing sale history...")
            sleep(0.5)
            sales_history(connection)
            continue
        elif choice == 3:
            print("\n\033[1;97mLoading search bar...")
            sleep(0.5)
            search_sale(connection)
            continue    
        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

def settings_menu(connection, user_id, username):
    while True:
        clear()
        title("⚙️  SETTINGS")
        sleep(0.2)
        breadcrumb("Home", "Settings")
        sleep(0.5)
        print(f"{" ":<5}\033[1;97m[1] 🔑 Change Password\n{" ":<5}[2] 👤 User Management\n{" ":<5}[3] 🛡️ Role Management\n{" ":<5}[4] 🗄️ Database Information\n{" ":<5}\n\n{" ":<5}[0] ← Back\033[0m\n")
        
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice >  4 or choice < 0:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

        if choice ==0:
                return
        elif choice == 1:
            print("\n\033[1;97mInitializing password setup...")
            sleep(0.5)
            change_password(connection,user_id,username)
            continue
        elif choice == 2:
            print("\n\033[1;97mInitializing user management...")
            sleep(0.5)
            manage_users(connection, user_id)
            continue
        elif choice == 3:
            print("\n\033[1;97mInitializing roles management...")
            sleep(0.5)
            manage_roles(connection)
            continue    
        elif choice == 4:
            print("\n\033[1;97mViewing database information...")
            sleep(0.5)
            db_info(connection)
            continue    
        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue
    
def reports_menu():
     while True:
        clear()
        title("📊 Reports")
        sleep(0.2)
        breadcrumb("Home", "Reports")
        sleep(0.5)

        print(f"{" ":<5}\033[1;97m[1] 📈 Inventory Report\n{" ":<5}[2] 💹 Sales Report\n{" ":<5}[3] 🧾 Purchase Report\n{" ":<5}[4] 💵 Profit Report\n{" ":<5}[5] 📉 Low Stock Reports\n\n{" ":<5}[0] Back\033[0m\n")
    
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice >  5 or choice < 0:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

        if choice ==0:
                return
        elif choice == 1:
            print("\n\033[1;97mLoading inventory report...")
            sleep(0.5)
            inventory_report(connection)
            continue
        elif choice == 2:
            print("\n\033[1;97mLoading sales report...")
            sleep(0.5)
            sales_report(connection)
            continue
        elif choice == 3:
            print("\n\033[1;97mLoading purchase report...")
            sleep(0.5)
            purchase_report(connection)
            continue    
        elif choice == 4:
            print("\n\033[1;97mLoading profit report...")
            sleep(0.5)
            profit_report(connection)
            continue    
        elif choice == 5:
            print("\n\033[1;97mLoading low stock reports...")
            sleep(0.5)
            low_stock_report(connection)
            continue    
        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

def administrator_main_menu(connection, first_name, last_name, role):
    while True:
        clear()
        title()
        sleep(0.1) 
        breadcrumb("Home")
        print(f"\033[1;97m👤 {first_name} {last_name}\033[0m")
        print(f"\033[1;97m🛡️  {role}\033[0m")
        title("MAIN MENU")
        
        print(f"\033[1;97m📦 INVENTORY\033[0m")
        print(f"{" ":<5}\033[1;97m[1] Products\n{" ":<5}[2] Categories\n{" ":<5}[3] Suppliers\n{" ":<5}[4] Customers\033[0m\n")

        print(f"\033[1;97m💼 TRANSACTIONS\033[0m")
        print(f"{" ":<5}\033[1;97m[5] Purchases\n{" ":<5}[6] Sales\033[0m\n")

        print(f"\033[1;97m📊  ANALYTICS\033[0m")
        print(f"{" ":<5}\033[1;97m[7] Reports\033[0m\n")

        print(f"\033[1;97m⚙️  SYSTEM\033[0m")
        print(f"{" ":<5}\033[1;97m[8] Settings\n{" ":<5}[0] Exit\033[0m\n")
        print(f"\033[36m└{'─' * 54}┘\033[0m")
        
        sleep(0.5)
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 1:
            products_menu(connection)
            continue

        elif choice == 2:
            categories_menu(connection)
            continue

        elif choice == 3:
            suppliers_menu(connection)
            continue

        elif choice == 4:
            customers_menu(connection)
            continue
        
        elif choice == 5:
            purchases_menu(connection, user_id)
            continue
            
        elif choice == 6:
            sales_menu(connection, user_id)
            continue

        elif choice == 7:
            reports_menu()
            continue

        elif choice == 8:
            settings_menu(connection, user_id, username)
            continue

        elif choice == 0:
            exit_app(connection)

        else:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

def manager_menu(connection, first_name, last_name, role):
    while True:
        clear()
        title()
        sleep(0.1) 
        breadcrumb("Home")
        print(f"\033[1;97m👤 {first_name} {last_name}\033[0m")
        print(f"\033[1;97m🛡️  {role}\033[0m")
        title("MAIN MENU")
        
        print(f"\033[1;97m📦 INVENTORY\033[0m")
        print(f"{" ":<5}\033[1;97m[1] Products\n{" ":<5}[2] Categories\n{" ":<5}[3] Suppliers\n{" ":<5}[4] Customers\033[0m\n")

        print(f"\033[1;97m💼 TRANSACTIONS\033[0m")
        print(f"{" ":<5}\033[1;97m[5] Purchases\n{" ":<5}[6] Sales\033[0m\n")

        print(f"\033[1;97m📊  ANALYTICS\033[0m")
        print(f"{" ":<5}\033[1;97m[7] Reports\033[0m\n")

        print(f"\033[1;97m⚙️  SYSTEM\033[0m")
        print(f"{" ":<5}\033[1;97m[8] Change Password\n{" ":<5}[0] Exit\033[0m\n")
        print("\033[36m==========================================\033[0m")
        
        sleep(0.5)
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 1:
            products_menu(connection)
            continue

        elif choice == 2:
            categories_menu(connection)
            continue
            
        elif choice == 3:
            suppliers_menu(connection)
            continue
            
        elif choice == 4:
            customers_menu(connection)
            continue
        
        elif choice == 5:
            purchases_menu(connection, user_id)
            continue
            
        elif choice == 6:
            sales_menu(connection, user_id)
            continue

        elif choice == 7:
            reports_menu()
            continue

        elif choice == 8:
            print("\n\033[1;97mInitializing password setup...")
            sleep(0.5)
            change_password(connection,user_id,username)
            continue

        elif choice == 0:
            exit_app(connection)

        else:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

def inventory_staff_menu(connection, first_name, last_name, role):
    while True:
        clear()
        title()
        sleep(0.1) 
        breadcrumb("Home")
        print(f"\033[1;97m👤 {first_name} {last_name}\033[0m")
        print(f"\033[1;97m🛡️  {role}\033[0m")
        title("MAIN MENU")
        
        print(f"\033[1;97m📦 INVENTORY\033[0m")
        print(f"{" ":<5}\033[1;97m[1] Products\n{" ":<5}[2] Categories\n{" ":<5}[3] Suppliers\033[0m\n")

        print(f"\033[1;97m💼 TRANSACTIONS\033[0m")
        print(f"{" ":<5}\033[1;97m[4] Purchases\033[0m\n")

        print(f"\033[1;97m📊  ANALYTICS\033[0m")
        print(f"{" ":<5}\033[1;97m[5] Inventory Report\n{" ":<5}\033[1;97m[6] Low Stock Report\033[0m\n")

        print(f"\033[1;97m⚙️  SYSTEM\033[0m")
        print(f"{" ":<5}\033[1;97m[7] Change password\n{" ":<5}[0] Exit\033[0m\n")
        print("\033[36m==========================================\033[0m")
        
        sleep(0.5)
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 1:
            products_menu(connection)
            continue

        elif choice == 2:
            categories_menu(connection)
            continue

        elif choice == 3:
            suppliers_menu(connection)
            continue
        
        elif choice == 4:
            purchases_menu(connection, user_id)
            continue
            
        elif choice == 5:
            print("\n\033[1;97mLoading inventory report...")
            sleep(0.5)
            inventory_report(connection)
            continue

        elif choice == 6:
            print("\n\033[1;97mLoading low stock reports...")
            sleep(0.5)
            low_stock_report(connection)
            continue 

        elif choice == 7:
            print("\n\033[1;97mInitializing password setup...")
            sleep(0.5)
            change_password(connection,user_id,username)
            continue

        elif choice == 0:
            exit_app(connection)

        else:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

def sales_staff_menu(connection, first_name, last_name, role):
    while True:
        clear()
        title()
        sleep(0.1) 
        breadcrumb("Home")
        print(f"\033[1;97m👤 {first_name} {last_name}\033[0m")
        print(f"\033[1;97m🛡️  {role}\033[0m")
        title("MAIN MENU")
        
        print(f"\033[1;97m💰 Sales\033[0m")
        print(f"{" ":<5}\033[1;97m[1] ➕ New Sale\n{" ":<5}[2] 📋 Sale History\n{" ":<5}[3] 🔍 Search Sale\n{" ":<5}[4] 👥 Customers\033[0m\n")

        print(f"\033[1;97m💼 TRANSACTIONS\033[0m")
        print(f"{" ":<5}\033[1;97m[5] View Products\033[0m\n")

        print(f"\033[1;97m📊  ANALYTICS\033[0m")
        print(f"{" ":<5}\033[1;97m[6] Sales Report\033[0m\n")

        print(f"\033[1;97m⚙️  SYSTEM\033[0m")
        print(f"{" ":<5}\033[1;97m[7] Change password\n{" ":<5}[0] Exit\033[0m\n")
        print("\033[36m==========================================\033[0m")
        
        sleep(0.5)
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 1:
            print("\n\033[1;97mInitializing sale addition...")
            sleep(0.5)
            add_sale(connection, user_id)
            continue

        elif choice == 2:
            print("\n\033[1;97mViewing sale history...")
            sleep(0.5)
            sales_history(connection)
            continue

        elif choice == 3:
            print("\n\033[1;97mLoading search bar...")
            sleep(0.5)
            search_sale(connection)
            continue  
        
        elif choice == 4:
            customers_menu(connection)
            continue
            
        elif choice == 5:
            print("\n\033[1;97mLoading products...")
            sleep(0.5)
            view_products(connection)
            continue

        elif choice == 6:
            print("\n\033[1;97mLoading sales report...")
            sleep(0.5)
            sales_report(connection)
            continue

        elif choice == 7:
            print("\n\033[1;97mInitializing password setup...")
            sleep(0.5)
            change_password(connection,user_id,username)
            continue

        elif choice == 0:
            exit_app(connection)

        else:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

def viewer_menu(connection, first_name, last_name, role):
    while True:
        clear()
        title()
        sleep(0.1) 
        breadcrumb("Home")
        print(f"\033[1;97m👤 {first_name} {last_name}\033[0m")
        print(f"\033[1;97m🛡️  {role}\033[0m")
        title("MAIN MENU")
        
        print(f"\033[1;97m📦 INVENTORY\033[0m")
        print(f"{" ":<5}\033[1;97m[1] View Products\n{" ":<5}[2] View Categories\n{" ":<5}[3] View Suppliers\033[0m\n")

        print(f"\033[1;97m📊  ANALYTICS\033[0m")
        print(f"{" ":<5}\033[1;97m[4] Reports\033[0m\n")

        print(f"\033[1;97m⚙️  SYSTEM\033[0m")
        print(f"{" ":<5}\033[1;97m[5] Change password\n{" ":<5}[0] Exit\033[0m\n")
        print("\033[36m==========================================\033[0m")
        
        sleep(0.5)
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 1:
            print("\n\033[1;97mLoading products...")
            sleep(0.5)
            view_products(connection)
            continue

        elif choice == 2:
            print("\n\033[1;97mLoading categories...")
            sleep(0.5)
            view_category(connection)
            continue

        elif choice == 3:
            print("\n\033[1;97mLoading Suppliers...")
            sleep(0.5)
            view_suppliers(connection)
            continue
        
        elif choice == 4:
            reports_menu()
            continue
            
        elif choice == 5:
            print("\n\033[1;97mInitializing password setup...")
            sleep(0.5)
            change_password(connection,user_id,username)
            continue


        elif choice == 0:
            exit_app(connection)

        else:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue


if __name__ == "__main__":

    clear()
    title()
    sleep(0.1)
    print("\033[1;73mWelcome !!\033[0m\n")
    sleep(0.5)
    if setup_check():
        print("\033[1;92m✅ Configuration Found\033[0m\n")
        sleep(0.5)
        print(f"\033[1;93mConnecting to MySQL server...\033[0m\n")
        sleep(0.1)
        print(f"\033[1;93mPlease wait...\033[0m\n")
        sleep(0.5)

        connection = connect_using_env()

        if connection:
            print(f"{" ":<12}{"\033[1;92m✅ Successfully connected to the MySQL server\033[0m"}")
            sleep(1)
        else : 
            print("\033[1;91m❌ Failed to connect to the server\033[0m\n")
            sleep(0.5)
            print("\033[1;93mPlease ensure:\n• MySQL Server is installed\n• MySQL Server is running\n• User Credentials in the .env file are correct\033[0m\n")
            sleep(1)
            input("Press Enter to exit program...")
            exit_app(connection)

    else:
        print("\033[1;91mNo configuration found\033[0m\n")
        sleep(0.5)
        while True:
            print("\033[1;93mLaunching setup wizard...\033[0m\n")
            sleep(0.5)
            clear()
            title()
            sleep(0.1)
            host, port, user, password = setup_wizard()

            connection = connect_to_server(host, port, user, password)

            if connection:
                print(f"{" ":<12}{"\033[1;92m✅ Successfully connected\033[0m"}")
                sleep(0.5)
                print("\033[1;73mSaving configuration...\033[0m\n")
                success, message = (save_config(host, port, user, password))
                if success:
                    print(f"\033[1;92m✅ {message}\033[0m")
                    sleep(1)
                else:
                    print("\033[1;91m❌ Failed to save the configuration\033[0m\n")
                    sleep(0.2)
                    print(f"{"\033[1;93mReason:":<10}{f"\033[1;97m{message}"}\033[0m")
                    sleep(0.2)
                    print(f"\n{" ":<10}\033[1;97mPlease make sure that this issue has been fixed.\033[0m")
                    sleep(0.5)
                    input("Press Enter to return to the setup wizard and try again...")
                    continue

                # sleep(0.5)
                # input("Press Enter to continue...")
                break

            else : 
                print("\033[1;91m❌ Failed to connect to the server.\033[0m\n")
                sleep(1)
                print("\033[1;93mPlease ensure:\n• MySQL Server is installed\n• MySQL Server is running\n• All credentials are correct\033[0m\n")
                sleep(1)
                print("\033[1;96m1. Try Again\n2. Exit\033[0m\n")
                while True:
                    try:
                        choice = int(input("\033[1;93mChoice: \033[0m"))
                    
                    except ValueError:
                        print("\033[1;91mEnter a valid choice\033[0m")
                        sleep(1)
                        continue
                    
                    if choice == 1:
                        break

                    elif choice == 2:
                        exit_app(connection)

                    else:
                        print("\033[1;91mPlease enter 1 or 2...\033[0m")
                        sleep(1)
                        continue

    clear()
    title()
    print("\033[1;97mChecking for database...\033[0m")
    sleep(1)
    check = database_exists(connection)
    if check:
        print("\033[1;92m✅ Database exists\033[0m\n")
        sleep(0.5)
    else:
        print("\033[1;91m❌ Database not found\033[0m\n")
        sleep(1)
        print("\033[1;93mCreating database...\033[0m")
        sleep(0.5)
        success, message = create_database(connection)
        if success:
            print(f"\033[1;92m✅ {message}\033[0m\n")
            sleep(0.5)
            # input("Press Enter to continue...")
        else:
            print("\033[1;91m❌ Failed to create the database\033[0m\n")
            print("\033[1;91m❌ Failed to save the configuration\033[0m\n")
            sleep(0.2)
            print(f"{"\033[1;93mReason:":<10}{f"\033[1;97m{message}"}\033[0m")
            sleep(0.2)
            print(f"\n{" ":<10}\033[1;97mPlease make sure that this issue has been fixed.\033[0m")
            sleep(1)
            input("Press Enter to exit program...")
            exit_app(connection)

    print("\033[1;93mConnecting to the database...\033[0m")
    sleep(0.5)
    connect_database(connection)
    print(f"\033[1;92m✅ Successfully connected the database\033[0m\n")
    sleep(1)
    # input("Press Enter to continue...")

    clear()
    title()
    print("\n\033[1;93mChecking for tables...\033[0m\n")
    sleep(0.5)    
    tables_check = tables_exists(connection)
    if tables_check:
        print(f"\n\033[1;92m✅ Database structure verified\033[0m\n")
        sleep(0.1)
        print(f"\033[1;92m✅ All required tables exist\033[0m\n")
        sleep(1)
        # input("Press Enter to continue...")

    else:
        print("\033[1;91m⚠️ Database structure is not fully initialized\033[0m\n")
        sleep(0.5)
        print("\033[1;93mSetting up the database structure...\033[0m\n")
        sleep(0.5)
        tables_create(connection)
        print(f"\033[1;92m✅ Database structure was set up successfully\033[0m\n")
        sleep(0.5)
        input("Press Enter to continue...")
           

    clear()
    title()
    print("\n\033[1;93mChecking for administrators...\033[0m\n")

    count = count_users(connection)
    if count == 0:
        print("\n\033[1;91m✕ No administrator account found\033[0m\n")
        sleep(0.5)
        print("\n\033[1;93mLaunching administrator setup wizard...\033[0m\n")
        sleep(1)
        clear()
        create_user(connection, count)
        print(f"\033[1;92m✅ Administrator account created successfully\033[0m\n")
        sleep(0.1)
        input("Press Enter to continue with login...")
        while True:
            clear()
            current_user = user_login(connection)
            if not current_user:
                print(f"\033[1;91m✕ Invalid credentials\033[0m")
                sleep(1)
                continue
            else:
                break

        print(f"\033[1;92m✅ Login successful\033[0m\n")
        sleep(1)
    else:
        print(f"\n\033[1;93m{count} user accounts found\033[0m\n")
        sleep(0.5)
        while True:
            print(f"\n\033[1;97m1. Login\n2. Create new account\033[0m\n")
            sleep(0.5)
            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 1:
                sleep(0.5)
                clear()
                current_user = user_login(connection)
                if not current_user:
                    print(f"\033[1;91m✕ Invalid credentials\033[0m")
                    sleep(1)
                    continue
                else:
                    break

            if choice == 2:
                print("\n\033[1;93mLaunching administrator setup wizard...\033[0m\n")
                sleep(0.5)
                clear()
                create_user(connection, count)
                print(f"\033[1;92m✅ Administrator account created successfully\033[0m\n")
                sleep(0.1)
                print(f"\033[1;92m✅ Login successful\033[0m\n")
                sleep(1)
                break

    username = current_user["username"]
    user_id = current_user["user_id"]
    first_name = current_user["first_name"]
    last_name = current_user["last_name"]
    role = current_user["role"]

    if role == "Administrator":
        administrator_main_menu(connection, first_name, last_name, role)
    elif role == "Manager":
        manager_menu(connection, first_name, last_name, role) 
    elif role == "Inventory Staff":
        inventory_staff_menu(connection, first_name, last_name, role)
    elif role == "Sales Staff":
        sales_staff_menu(connection, first_name, last_name, role)
    elif role == "Viewer":
        viewer_menu(connection, first_name, last_name, role)
    


    
        

            


