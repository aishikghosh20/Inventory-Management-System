import mysql.connector
from pathlib import Path
import sys
from time import sleep
from config import RESOURCE_DIR

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

def database_exists(connection):
    from config import DB_NAME
    cursor = connection.cursor(buffered = True)
    try:
        cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
        exists= cursor.fetchone() is not None
        databases = [db[0] for db in cursor.fetchall()]
        print("\n\033[1;97mDB_NAME =", DB_NAME)
        print("DATABASES =\033[0m", databases)
        print()
        sleep(1)
        cursor.close()
    except Exception as e:
        print(f"\033[1;91mFailed: {e}\033[0m")
        sleep(1)
        cursor.close()
        exit_app(connection)

    return exists

def create_database(connection):
    from config import DB_NAME
    try:
        cursor = connection.cursor(buffered = True)
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
        cursor.close()
        return True, f"Database \033[1;96m{DB_NAME}\033[1;92m created successfully"
    except Exception as e:
        return False, f"{e}"
    
def connect_database(connection):
    from config import  DB_NAME
    cursor = connection.cursor(buffered = True)
    try:
        cursor.execute(f"USE {DB_NAME}")
        cursor.close()
    except Exception as e:
        print(f"\033[1;91mFailed: {e}\033[0m")
        sleep(1)
        cursor.close()
        exit_app(connection)
    

def tables_exists(connection):
    required_tables = [
        "users",
        "categories",
        "suppliers",
        "products",
        "customers",
        "purchases",
        "purchase_items",
        "sales",
        "sale_items"
    ]
    cursor = connection.cursor(buffered = True)
    try:
        cursor.execute("SHOW TABLES")
        tables  = cursor.fetchall() # returns a list of tuples with the table names
        cursor.close()
    except  Exception as e:
        print(f"\033[1;91mFailed: {e}\033[0m")
        sleep(1)
        cursor.close()
        exit_app(connection)

    table_names = [table[0] for table in tables] # makes a list of the table names from the list of the tuples in 'tables'

    exists = True
    for table in required_tables:
        if table in table_names:
            print(f"\033[1;92m✓ {table}\033[0m")
            sleep(0.1)

        else:
            print(f"\033[1;91m✕ {table}\033[0m")
            exists = False
            sleep(0.1)

    sleep(0.5)
    return exists

def tables_create(connection):

    schema_file = RESOURCE_DIR/"sql"/"schema.sql" # To get the schema file

    # To read all the queries from the schema file
    with open(schema_file, "r", encoding= "utf-8") as file:
        scripts = file.read() 

    queries = scripts.split(";") # creates a list of strings of the queries

    cursor = connection.cursor(buffered = True)
    for query in queries:
        query = query.strip()

        if query:
            try:
                cursor.execute(query)
            except Exception as e:
                print(f"\033[1;91mFailed: {e}\033[0m")
                sleep(1)
                cursor.close()
                exit_app(connection)

            if query.upper().startswith("CREATE TABLE"):
                words =query.split()
                if "EXISTS" in words:
                    table_name = words[words.index("EXISTS") + 1].rstrip("(")
                else:
                    table_name = words[words.index("TABLE") + 1].rstrip("(")

                print(f"\033[1;92mCreated table: \033[1;96m{table_name}\033[0m\n")
                sleep(0.1)
        else:
            continue

    connection.commit()
    cursor.close()
    sleep(0.5)
    print(f"\033[1;92m✅ All required tables created\033[0m\n")
    sleep(0.5)
    return



