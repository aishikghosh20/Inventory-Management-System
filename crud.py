import mysql.connector
from pathlib import Path
import sys
from time import sleep
from intializing_db import exit_app
import re, bcrypt, os

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

def breadcrumb(*paths):
    print("\033[1;96m📍 " + ">".join(paths) + "\033[0m")

def add_category(connection):
    clear()
    title("ADD CATEGORY")
    sleep(0.1) 
    breadcrumb("Home", "Products", "Add Category")
    sleep(0.5)
    print("\n\033[1;93mPlease enter the details as prompted:\033[0m\n")
    sleep(0.5)
    while True:
        try:
            category_name = input("\033[1;93mCATEGORY NAME: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return

        if not category_name:
            print("\033[1;91m❌ Category name cannot be empty\033[0m\n")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z0-9  _.,'()&/+-]+", category_name):
            print("\033[1;91m❌ Category name contains invalid characters\033[0m\n")
            sleep(1)
            continue

        if len(category_name) > 50:
            print("\033[1;91m❌ Category name can have a max of 50 characters\033[0m\n")
            sleep(1)
            continue

        cursor = connection.cursor(buffered = True)
        try:
            cursor.execute("SELECT 1 FROM Categories WHERE LOWER(category_name) = LOWER(%s)", (category_name,))
            if cursor.fetchone():  # returns 1 if the emails is present in the table
                print("\033[1;91m✕ Category already exists")
                sleep(1)
                continue
            else:
                break

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with adding the category\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return

        finally:
            cursor.close()

    print("\033[1;93mInitializing category...")
    sleep(0.5)

    cursor = connection.cursor(buffered = True)
    try:
        cursor.execute(
        """
        INSERT INTO Categories
        (
            category_name
        )
        VALUES (%s)
        """,
        (
            category_name,
        )
        )
        connection.commit()

        print("\033[1;92m✓ Category added successfully\033[0m")
        sleep(1)

    except  Exception as e:
        connection.rollback()
        print(f"\033[1;91mFailed to initialize\n\033[1;93mReason: {e}\033[0m")
        sleep(0.5)
        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
        sleep(1)
        return

    finally:
        cursor.close()

    input("\033[1;97mPress Enter to continue...\033[0m")
    return
    
def view_category(connection):
    clear()
    title("VIEW CATEGORIES")
    sleep(0.1) 
    breadcrumb("Home", "Products", "View Categories")
    sleep(0.5)
    print("\n\033[1;93mSort Categories:\n\033[1;97m[1] Category ID (Ascending)\n[2] Category ID (Descending)\n[3] Category Name (A-Z)\n[4] Category Name (Z-A)\n\n[0] Back\033[0m")
    while True:
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 0 :
            return
        elif choice == 1:
            order_by = "category_id ASC"
            break
        elif choice == 2:
            order_by = "category_id DESC"
            break
        elif choice == 3:
            order_by = "category_name ASC"
            break
        elif choice == 4:
            order_by = "category_name DESC"
            break
        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue


    cursor = connection.cursor(buffered = True)
    try:
        cursor.execute(f"""SELECT category_id, category_name
                          FROM Categories
                          ORDER BY {order_by};
                        """)
        categories = cursor.fetchall()

    except  Exception as e:
            print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return
    
    if not categories:
        print(f"\033[1;91m✕ No Categories Found\033[0m\n")
        sleep(1)
        return
    
    print("\033[36m┌────┬──────────────────────────────┐\033[0m")
    print(f"\033[1;97m│ {'ID':<2} │ {'Category Name':<28} │\033[0m")
    print("\033[36m├────┼──────────────────────────────┤\033[0m")

    for category_id, category_name in categories:
        print(f"│ {category_id:<2} │ {category_name:<28} │")

    print("\033[36m└────┴──────────────────────────────┘\033[0m")
    sleep(0.5)
    print("\n\033[36m─────────────────────────────────────\033[0m")
    print(f"\033[1;97mTotal Categories : {len(categories)}\033[0m")
    sleep(0.5)
    input("\n\033[1;97mPress Enter to continue...\033[0m")
    return    

def search_categories(connection):
    clear()
    title("SEARCH CATEGORIES")
    sleep(0.1) 
    breadcrumb("Home", "Products", "Search Categories")
    sleep(0.5)
    print("\n\033[1;93mSearch Type:\n\033[1;97m[1] Search by ID\n[2] Search by Name\n\n[0] Back\033[0m")
    while True:
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 0:
            return
        
        elif choice == 1:
            print("\n\033[1;93mPlease enter the id below....\n")
            sleep(0.5)
            while True:
                try:
                    new_id = int(input("\033[1;93mID: \033[0m"))
                    
                except ValueError:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if not new_id:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if new_id < 0:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                break

            cursor = connection.cursor(buffered = True)
            try:
                cursor.execute(f"SELECT * FROM Categories WHERE category_id = %s", (new_id,))
                categories = cursor.fetchone()

            except  Exception as e:
                    print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            
            if not categories:
                print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                sleep(1)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                return
            
            category_id, category_name, description = categories
            
            print("\033[36m┌────┬──────────────────────────────┐\033[0m")
            print(f"\033[1;97m│ {'ID':<2} │ {'Category Name':<28} │\033[0m")
            print("\033[36m├────┼──────────────────────────────┤\033[0m")
            print(f"│ {category_id:<2} │ {category_name:<28} │")
            print("\033[36m└────┴──────────────────────────────┘\033[0m")

            print()
            print("\033[36m──────────────────────────────────────────────\033[0m")
            print("\033[1;97mDescription:\033[0m")

            if description:
                print(description)
            else:
                print("No description available.")

            print("\033[36m──────────────────────────────────────────────\033[0m")
            sleep(0.5)
            input("\n\033[1;97mPress Enter to continue...\033[0m")
            return    
        elif choice == 2:
            print("\n\033[1;93mPlease enter the name below....\n")
            sleep(0.5)
            while True:
                try:
                    name = (input("\033[1;93mNAME: \033[0m")).strip()
                    
                except ValueError:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if not name:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", name):
                    print("\033[1;91m❌ Category name contains invalid characters\033[0m\n")
                    sleep(1)
                    continue

                if len(name) > 50:
                    print("\033[1;91m❌ Category name can have a max of 50 characters\033[0m\n")
                    sleep(1)
                    continue

                break

            cursor = connection.cursor(buffered = True)
            try:
                cursor.execute(f"SELECT * FROM Categories WHERE LOWER(category_name)=LOWER(%s)",(name,))
                categories = cursor.fetchone()

            except  Exception as e:
                    print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            
            if not categories:
                print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                sleep(1)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                return
            
            category_id, category_name, description = categories
            
            print("\033[36m┌────┬──────────────────────────────┐\033[0m")
            print(f"\033[1;97m│ {'ID':<2} │ {'Category Name':<28} │\033[0m")
            print("\033[36m├────┼──────────────────────────────┤\033[0m")
            print(f"│ {category_id:<2} │ {category_name:<28} │")
            print("\033[36m└────┴──────────────────────────────┘\033[0m")

            print()
            print("\033[36m──────────────────────────────────────────────\033[0m")
            print("\033[1;97mDescription:\033[0m")

            if description:
                print(description)
            else:
                print("No description available.")

            print("\033[36m──────────────────────────────────────────────\033[0m")
            sleep(0.5)
            input("\n\033[1;97mPress Enter to continue...\033[0m")
            return  

        else:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

def update_category(connection):
    clear()
    title("UPDATE CATEGORy")
    sleep(0.1) 
    breadcrumb("Home", "Products", "Update Category")
    sleep(0.5)
    print("\n\033[1;93mSearch Category:\n\033[1;97m[1] Search by ID\n[2] Search by Name\n\n[0] Back\033[0m")
    while True:
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 0:
            return
        
        elif choice == 1:
            print("\n\033[1;93mPlease enter the id below....\n")
            sleep(0.5)
            while True:
                try:
                    new_id = int(input("\033[1;93mID: \033[0m"))
                    
                except ValueError:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if not new_id:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if new_id < 0:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                break

            cursor = connection.cursor(buffered = True)
            try:
                cursor.execute(f"SELECT * FROM Categories WHERE category_id = %s;", (new_id,))
                categories = cursor.fetchone()

            except  Exception as e:
                    print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            
            if not categories:
                print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                sleep(1)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                return
            
            category_id, category_name, description = categories
            
            print("\033[36m┌────┬──────────────────────────────┐\033[0m")
            print(f"\033[1;97m│ {'ID':<2} │ {'Category Name':<28} │\033[0m")
            print("\033[36m├────┼──────────────────────────────┤\033[0m")
            print(f"│ {category_id:<2} │ {category_name:<28} │")
            print("\033[36m└────┴──────────────────────────────┘\033[0m")

            print()
            print("\033[36m──────────────────────────────────────────────\033[0m")
            print("\033[1;97mDescription:\033[0m")

            if description:
                print(description)
            else:
                print("No description available.")

            print("\033[36m──────────────────────────────────────────────\033[0m")
            sleep(0.5)
            break


        elif choice == 2:
            print("\n\033[1;93mPlease enter the name below....\n")
            sleep(0.5)
            while True:
                try:
                    name = (input("\033[1;93mNAME: \033[0m")).strip()
                    
                except ValueError:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if not name:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", name):
                    print("\033[1;91m❌ Category name contains invalid characters\033[0m\n")
                    sleep(1)
                    continue

                if len(name) > 50:
                    print("\033[1;91m❌ Category name can have a max of 50 characters\033[0m\n")
                    sleep(1)
                    continue

                break

            cursor = connection.cursor(buffered = True)
            try:
                cursor.execute(f"SELECT * FROM Categories WHERE LOWER(category_name)=LOWER(%s)",(name,))

                categories = cursor.fetchone()

            except  Exception as e:
                    print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            
            if not categories:
                print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                sleep(1)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                return
            
            category_id, category_name, description = categories
            
            print("\033[36m┌────┬──────────────────────────────┐\033[0m")
            print(f"\033[1;97m│ {'ID':<2} │ {'Category Name':<28} │\033[0m")
            print("\033[36m├────┼──────────────────────────────┤\033[0m")
            print(f"│ {category_id:<2} │ {category_name:<28} │")
            print("\033[36m└────┴──────────────────────────────┘\033[0m")

            print()
            print("\033[36m──────────────────────────────────────────────\033[0m")
            print("\033[1;97mDescription:\033[0m")

            if description:
                print(description)
            else:
                print("No description available.")

            print("\033[36m──────────────────────────────────────────────\033[0m")
            sleep(0.5)
            break

        else:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

    while True:
        print("\n\033[1;93mUpdate Category:\033[0m\n")
        print("\033[1;97m[1] Category Name")
        print("[2] Description")
        print("[3] Both")
        print("[0] ← Back\033[0m\n")

        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))
        except ValueError:
            print("\033[1;91mEnter a valid input.\033[0m")
            sleep(1)
            continue

        if choice not in (0, 1, 2, 3):
            print("\033[1;91mEnter a valid choice.\033[0m")
            sleep(1)
            continue
            
        if choice == 3:
            print("\033[1;93mPlease enter the New Name:\033[0m\n")
            sleep(0.5)
            while True:
                try:
                    new_category_name = input("\033[1;93mCATEGORY NAME: \033[0m").strip()

                except  Exception as e:
                    print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return

                if not new_category_name:
                    print("\033[1;91m❌ Category name cannot be empty\033[0m\n")
                    sleep(1)
                    continue

                if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", new_category_name):
                    print("\033[1;91m❌ Category name contains invalid characters\033[0m\n")
                    sleep(1)
                    continue

                if len(new_category_name) > 50:
                    print("\033[1;91m❌ Category name can have a max of 50 characters\033[0m\n")
                    sleep(1)
                    continue

                if new_category_name == category_name:
                    break
                

                cursor = connection.cursor(buffered = True)
                try:
                    cursor.execute("SELECT 1 FROM Categories WHERE LOWER(category_name) = LOWER(%s)", (new_category_name,))
                    if cursor.fetchone():  # returns 1 if the emails is present in the table
                        print("\033[1;91m✕ Category already exists")
                        sleep(1)
                        continue
                    else:
                        break

                except  Exception as e:
                    print(f"\033[1;91mFailed to continue with adding the category name\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return

                finally:
                    cursor.close()

            
            print("\033[1;93mPlease enter the New Description: <Press Enter to keep current description>\033[0m\n")
            sleep(0.5)
            try:
                desc = input("\033[1;93mTEXT: \033[0m\n")
            except  Exception as e:
                    print(f"\033[1;91mFailed to continue with adding the category description\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            
            if not desc:
                desc = description
            
            sleep(0.5)
            print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
            print("\033[1;97m│                 REVIEW CATEGORY UPDATE                     │\033[0m")
            print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

            print(f"\n\033[1;97mCategory ID : \033[1;93m{category_id}\033[0m\n")

            print("\033[1;97mName\033[0m")
            print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
            print(f"\033[1;93mCurrent :\033[0m {category_name}")
            print(f"\033[1;92mUpdated :\033[0m {new_category_name}\n")

            print("\033[1;97mDescription\033[0m")
            print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
            print(f"\033[1;93mCurrent :\033[0m {description}")
            print(f"\033[1;92mUpdated :\033[0m {desc}")

            print("\n\033[36m──────────────────────────────────────────────────────────────\033[0m")
            sleep(0.5)
            print("\n\033[1;97mSave these changes?\033[0m\n")
            print("\033[1;92m[1] ✔ Yes\033[0m")
            print("\033[1;91m[2] ✖ No\033[0m")
            sleep(0.5)
            while True:
                try:
                    choice = int(input("\033[1;93mChoice: \033[0m"))

                except ValueError:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if choice == 1:
                    print("\033[1;97mSaving changes...")
                    sleep(0.5)

                    cursor = connection.cursor(buffered = True)
                    try:
                        cursor.execute("UPDATE Categories SET category_name =%s, description =%s WHERE category_id = %s;", (new_category_name, desc, category_id))
                        connection.commit()
                        print("\033[1;92m✓ Category updated successfully\033[0m")
                        sleep(1)
                        input("\033[1;97mPress Enter to continue...")
                        break

                    except  Exception as e:
                        print(f"\033[1;91mFailed to continue with update the category\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    finally:
                        cursor.close()

                elif choice == 2:
                    print("\033[1;97mCancelling...")
                    sleep(1)
                    break
                
                else:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

            continue
            
        elif choice == 1:
            print("\033[1;93mPlease enter the New Name:\033[0m\n")
            sleep(0.5)
            while True:
                try:
                    new_category_name = input("\033[1;93mCATEGORY NAME: \033[0m").strip()

                except  Exception as e:
                    print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return

                if not new_category_name:
                    print("\033[1;91m❌ Category name cannot be empty\033[0m\n")
                    sleep(1)
                    continue

                if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", new_category_name):
                    print("\033[1;91m❌ Category name contains invalid characters\033[0m\n")
                    sleep(1)
                    continue

                if len(new_category_name) > 50:
                    print("\033[1;91m❌ Category name can have a max of 50 characters\033[0m\n")
                    sleep(1)
                    continue

                if new_category_name == category_name:
                    break
                

                cursor = connection.cursor(buffered = True)
                try:
                    cursor.execute("SELECT 1 FROM Categories WHERE LOWER(category_name) = LOWER(%s)", (new_category_name,))
                    if cursor.fetchone():  # returns 1 if the emails is present in the table
                        print("\033[1;91m✕ Category already exists")
                        sleep(1)
                        continue
                    else:
                        break

                except  Exception as e:
                    print(f"\033[1;91mFailed to continue with adding the category name\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return

                finally:
                    cursor.close()

            sleep(0.5)
            print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
            print("\033[1;97m│                 REVIEW CATEGORY UPDATE                     │\033[0m")
            print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

            print(f"\n\033[1;97mCategory ID : \033[1;93m{category_id}\033[0m\n")

            print("\033[1;97mName\033[0m")
            print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
            print(f"\033[1;93mCurrent :\033[0m {category_name}\n")
            print(f"\033[1;92mUpdated :\033[0m {new_category_name}\n")

            print("\033[1;97mDescription\033[0m")
            print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
            print(f"\033[1;93mCurrent :\033[0m {description}")

            print("\n\033[36m──────────────────────────────────────────────────────────────\033[0m")
            sleep(0.5)
            print("\n\033[1;97mSave these changes?\033[0m\n")
            print("\033[1;92m[1] ✔ Yes\033[0m")
            print("\033[1;91m[2] ✖ No\033[0m")
            sleep(0.5)
            while True:
                try:
                    choice = int(input("\033[1;93mChoice: \033[0m"))

                except ValueError:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if choice == 1:
                    print("\033[1;97mSaving changes...")
                    sleep(0.5)

                    cursor = connection.cursor(buffered = True)
                    try:
                        cursor.execute("UPDATE Categories SET category_name =%s WHERE category_id = %s;", (new_category_name, category_id))
                        connection.commit()
                        print("\033[1;92m✓ Category updated successfully\033[0m")
                        sleep(1)
                        input("\033[1;97mPress Enter to continue...")
                        break

                    except  Exception as e:
                        print(f"\033[1;91mFailed to continue with update the category\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    finally:
                        cursor.close()

                elif choice == 2:
                    print("\033[1;97mCancelling...")
                    sleep(1)
                    break
                
                else:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

            continue
              
        elif choice == 2:
            print("\033[1;93mPlease enter the New Description: <Press Enter to keep current description>\033[0m\n")
            sleep(0.5)
            try:
                desc = input("\033[1;93mTEXT: \033[0m\n")
            except  Exception as e:
                    print(f"\033[1;91mFailed to continue with adding the category description\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            if not desc:
                desc = description
            
            sleep(0.5)
            print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
            print("\033[1;97m│                 REVIEW CATEGORY UPDATE                     │\033[0m")
            print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

            print(f"\n\033[1;97mCategory ID : \033[1;93m{category_id}\033[0m\n")

            print("\033[1;97mName\033[0m")
            print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
            print(f"\033[1;93mCurrent :\033[0m {category_name}\n")

            print("\033[1;97mDescription\033[0m")
            print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
            print(f"\033[1;93mCurrent :\033[0m {description}")
            print(f"\033[1;92mUpdated :\033[0m {desc}")

            print("\n\033[36m──────────────────────────────────────────────────────────────\033[0m")
            sleep(0.5)
            print("\n\033[1;97mSave these changes?\033[0m\n")
            print("\033[1;92m[1] ✔ Yes\033[0m")
            print("\033[1;91m[2] ✖ No\033[0m")
            sleep(0.5)
            while True:
                try:
                    choice = int(input("\033[1;93mChoice: \033[0m"))

                except ValueError:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if choice == 1:
                    print("\033[1;97mSaving changes...")
                    sleep(0.5)

                    cursor = connection.cursor(buffered = True)
                    try:
                        cursor.execute("UPDATE Categories SET description =%s WHERE category_id = %s;", (desc, category_id))
                        connection.commit()
                        print("\033[1;92m✓ Category updated successfully\033[0m")
                        sleep(1)
                        input("\033[1;97mPress Enter to continue...")
                        break

                    except  Exception as e:
                        print(f"\033[1;91mFailed to continue with update the category\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    finally:
                        cursor.close()

                elif choice == 2:
                    print("\033[1;97mCancelling...")
                    sleep(1)
                    break
                
                else:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

            continue

        else:
            input("\033[1;97mPress Enter to go back...\033[0m")
            return

def delete_category(connection):
    clear()
    title("DELETE CATEGORY")
    sleep(0.1) 
    breadcrumb("Home", "Products", "Delete Category")
    sleep(0.5)
    print("\n\033[1;93mPlease enter the details as prompted:\033[0m\n")
    sleep(0.5)
    print("\n\033[1;93mSearch Category:\n\033[1;97m[1] Search by ID\n[2] Search by Name\n\n[0] Back\033[0m")
    while True:
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 0:
            return
        
        elif choice == 1:
            print("\n\033[1;93mPlease enter the id below....\n")
            sleep(0.5)
            while True:
                try:
                    new_id = int(input("\033[1;93mID: \033[0m"))
                    
                except ValueError:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if not new_id:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if new_id < 0:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                break

            cursor = connection.cursor(buffered = True)
            try:
                cursor.execute(f"SELECT * FROM Categories WHERE category_id = %s", (new_id,))
                categories = cursor.fetchone()

            except  Exception as e:
                    print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            
            if not categories:
                print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                sleep(1)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                return
            
            category_id, category_name, description = categories
            
            print("\033[36m┌────┬──────────────────────────────┐\033[0m")
            print(f"\033[1;97m│ {'ID':<2} │ {'Category Name':<28} │\033[0m")
            print("\033[36m├────┼──────────────────────────────┤\033[0m")
            print(f"│ {category_id:<2} │ {category_name:<28} │")
            print("\033[36m└────┴──────────────────────────────┘\033[0m")

            print()
            print("\033[36m──────────────────────────────────────────────\033[0m")
            print("\033[1;97mDescription:\033[0m")

            if description:
                print(description)
            else:
                print("No description available.")

            print("\033[36m──────────────────────────────────────────────\033[0m")
            sleep(0.5)
            break


        elif choice == 2:
            print("\n\033[1;93mPlease enter the name below....\n")
            sleep(0.5)
            while True:
                try:
                    name = (input("\033[1;93mNAME: \033[0m")).strip()
                    
                except ValueError:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if not name:
                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", name):
                    print("\033[1;91m❌ Category name contains invalid characters\033[0m\n")
                    sleep(1)
                    continue

                if len(name) > 50:
                    print("\033[1;91m❌ Category name can have a max of 50 characters\033[0m\n")
                    sleep(1)
                    continue

                break

            cursor = connection.cursor(buffered = True)
            try:
                cursor.execute(f"SELECT * FROM Categories WHERE LOWER(category_name)=LOWER(%s)",(name,))

                categories = cursor.fetchone()

            except  Exception as e:
                    print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            
            if not categories:
                print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                sleep(1)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                return
            
            category_id, category_name, description = categories
            
            print("\033[36m┌────┬──────────────────────────────┐\033[0m")
            print(f"\033[1;97m│ {'ID':<2} │ {'Category Name':<28} │\033[0m")
            print("\033[36m├────┼──────────────────────────────┤\033[0m")
            print(f"│ {category_id:<2} │ {category_name:<28} │")
            print("\033[36m└────┴──────────────────────────────┘\033[0m")

            print()
            print("\033[36m──────────────────────────────────────────────\033[0m")
            print("\033[1;97mDescription:\033[0m")

            if description:
                print(description)
            else:
                print("No description available.")

            print("\033[36m──────────────────────────────────────────────\033[0m")
            sleep(0.5)
            break

        else:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

    print("\033[1;93m┌───────────────────────────────────┐\033[0m") 
    print("\033[1;93m│           \033[1;91mARE YOU SURE?          \033[1;93m │\033[0m")
    print("\033[1;93m├───────────────────────────────────┤\033[0m")
    print("\033[1;93m│  \033[1;93m⚠️  THIS ACTION CANNOT BE UNDONE \033[1;93m │\033[0m")
    print("\033[1;93m├─────────────────┬─────────────────┤\033[0m")
    print(f"\033[1;93m│ \033[1;97m{"   [1] \033[1;92mYES     ":<10} \033[1;93m│ \033[1;97m{"    [2] \033[1;91mNO ":<22} \033[1;93m│")
    print("\033[1;93m└─────────────────┴─────────────────┘\033[0m")
    while True:
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 2:
            print("\033[1;93mCancelling...")
            sleep(0.5)
            input("\033[1;97mPress Enter to go back...\033[0m")
            return
        
        elif choice == 1:
            cursor = connection.cursor(buffered = True)
            try:
                cursor.execute(f"DELETE FROM Categories WHERE category_id =%s;",(category_id,))
                connection.commit()
                print("\033[1;92m✓ Category deleted successfully\033[0m")
                sleep(1)
                break

            except mysql.connector.Error as e:
                connection.rollback()

                if e.errno == 1451:
                    print("\033[1;91m❌ This category cannot be deleted because products are assigned to it.\033[0m")
                    sleep(0.1)
                    print("\033[1;93mPlease update or remove those products first before trying again\033[0m")
                    sleep(1)
                    break
                else:
                    print(f"\033[1;91mFailed to delete category.\nReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    return
                
            except  Exception as e:
                    print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            

            
            finally:
                cursor.close()

        else:
            print("\033[1;91mEnter a valid choice\033[0m")
            sleep(1)
            continue

    input("\033[1;97mPress Enter to go back...\033[0m")
    return

         





def add_product(connection):
    clear()
    title("ADD PRODUCT")
    sleep(0.1) 
    breadcrumb("Home", "Products", "Add Product")
    sleep(0.5)
    print("\n\033[1;93mPlease enter the details as prompted:\033[0m\n")
    sleep(0.5)

    while True:
        try:
            product_name = input("\033[1;93mPRODUCT NAME: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            return

        if not product_name:
            print("\033[1;91m❌ Username cannot be empty\033[0m\n")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z0-9_.,'()&/+-]+", product_name):
            print("\033[1;91m❌ Product name contains invalid characters\033[0m\n")
            sleep(1)
            continue

        if len(product_name) > 150:
            print("\033[1;91m❌ Product name can have a max of 150 characters\033[0m\n")
            sleep(1)
            continue

        break

    

    

