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

def print_category(category_id, category_name, description, pause=True):

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

    if pause:
        sleep(0.5)
        input("\n\033[1;97mPress Enter to continue...\033[0m")
def repeat_operation(operation, entity, location="main menu"):
    
    # Returns:
    #     True  -> Repeat the operation
    #     False -> Return to previous menu

    print(f"\n\033[1;93mWould you like to {operation} another {entity}?\033[0m\n")
    print("\033[1;97m[1] YES")
    print("\033[1;91m[2] NO\033[0m")

    while True:
        try:
            choice = int(input("\033[1;93mChoice: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        if choice == 1:
            return True

        elif choice == 2:
            input(f"\n\033[1;97mPress Enter to return to {location}...\033[0m")
            return False

        print("\033[1;91mEnter a valid input\033[0m")
        sleep(1)
def confirm_changes():

    print("\n\033[1;97mSave these changes?\033[0m\n")
    print("\033[1;92m[1] ✔ Yes")
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
            return True

        elif choice == 2:
            return False

        print("\033[1;91mEnter a valid input\033[0m")
        sleep(1)
def review_category_update(category_id,old_name,new_name,old_description,new_description):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;97m│                 REVIEW CATEGORY UPDATE                     │\033[0m")
    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print(f"\n\033[1;97mCategory ID : \033[1;93m{category_id}\033[0m\n")

    print("\033[1;97mName\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {old_name}")

    if new_name is not None:
        print(f"\033[1;92mUpdated :\033[0m {new_name}")

    print()

    print("\033[1;97mDescription\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {old_description}")

    if new_description is not None:
        print(f"\033[1;92mUpdated :\033[0m {new_description}")

    print("\n\033[36m──────────────────────────────────────────────────────────────\033[0m")
def execute_update(connection, query, values, entity="Category"):

    print(f"\033[1;93mUpdating {entity}...")
    sleep(0.5)

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(query, values)

        connection.commit()

        print(f"\033[1;92m✓ {entity.capitalize()} updated successfully\033[0m")
        sleep(1)

        return True

    except Exception as e:

        connection.rollback()

        print(
            f"\033[1;91mFailed to continue with updating the {entity}\n"
            f"\033[1;93mReason: {e}\033[0m"
        )

        sleep(0.5)

        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

        sleep(1)

        return False

    finally:

        cursor.close()
def review_new_category(category_name, description):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;97m│                   REVIEW NEW CATEGORY                      │\033[0m")
    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print("\033[1;97mName\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(category_name)

    print("\033[1;97mDescription\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")

    if description:
        print(description)
    else:
        print("No description")

    print("\n\033[36m──────────────────────────────────────────────────────────────\033[0m")
def get_category_name(connection, current_name=None):

    print("\033[1;93mPlease enter the New Name:\033[0m\n")
    sleep(0.5)

    while True:
        try:
            new_name = input("\033[1;93mCATEGORY NAME: \033[0m").strip()

        except Exception as e:
            print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return None

        if not new_name:
            print("\033[1;91m❌ Category name cannot be empty\033[0m\n")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", new_name):
            print("\033[1;91m❌ Category name contains invalid characters\033[0m\n")
            sleep(1)
            continue

        if len(new_name) > 50:
            print("\033[1;91m❌ Category name can have a max of 50 characters\033[0m\n")
            sleep(1)
            continue

        if current_name and new_name == current_name:
            return new_name

        try:
            if category_exists(connection, new_name):
                print("\033[1;91m✕ Category already exists")
                sleep(1)
                continue

            return new_name

        except Exception as e:
            print(f"\033[1;91mFailed to continue with adding the category name\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return None
def category_exists(connection, category_name):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            "SELECT 1 FROM Categories WHERE LOWER(category_name)=LOWER(%s)",
            (category_name,)
        )

        return cursor.fetchone() is not None

    finally:

        cursor.close()
def get_description(current_description=None):

    if current_description is None:
        print("\033[1;93mPlease enter the Description: <Press Enter to leave it blank>\033[0m\n")
    else:
        print("\033[1;93mPlease enter the New Description: <Press Enter to keep current description>\033[0m\n")

    sleep(0.5)

    try:
        desc = input("\033[1;93mTEXT: \033[0m\n")

    except Exception as e:
        raise e

    if current_description is not None and not desc:
        return current_description

    return desc
def save_category_update(connection, query, values):

    if not confirm_changes():
        print("\033[1;97mCancelling...\033[0m")
        sleep(1)
        return False

    return execute_update(connection, query, values)

def add_category(connection):
    while True:
        clear()
        title("ADD CATEGORY")
        sleep(0.1) 
        breadcrumb("Home", "Categories", "Add Category")
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

            try:
                if category_exists(connection, category_name):  # returns 1 if the emails is present in the table
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

        print("\033[1;93mPlease enter the Description: <Press Enter to leave it blank>\033[0m\n")
        sleep(0.5)
        try:
            description = input("\033[1;93mTEXT: \033[0m\n")
        except  Exception as e:
                print(f"\033[1;91mFailed to continue with adding the category description\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return
        
        sleep(0.5)
        review_new_category(category_name, description)
        sleep(0.5)
        if confirm_changes():
            print("\033[1;93mInitializing category...")
            sleep(0.5)

            cursor = connection.cursor(buffered=True)

            try:
                cursor.execute(
                    """
                    INSERT INTO Categories
                    (
                        category_name, description
                    )
                    VALUES (%s, %s)
                    """,
                    (
                        category_name,
                        description
                    )
                )

                connection.commit()

                print("\033[1;92m✓ Category added successfully\033[0m")
                sleep(1)

                if repeat_operation("add", "category"):
                    continue
                return

            except Exception as e:
                print(f"\033[1;91mFailed to add the category\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            finally:
                cursor.close()

        else:

            print("\033[1;97mCancelling...\033[0m")
            sleep(1)

            if repeat_operation("add", "category"):
                continue

            return

def view_category(connection):
    clear()
    title("VIEW CATEGORIES")
    sleep(0.1) 
    breadcrumb("Home", "Categories", "View Categories")
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
        cursor.execute(f"""SELECT category_id, category_name, description
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
    
    finally:
        cursor.close()

    if not categories:
        print(f"\033[1;91m✕ No Categories Found\033[0m\n")
        sleep(1)
        return
    
    for category in categories:
        category_id, category_name, description = category
        print_category(category_id,category_name,description,pause= False)
    print()
    sleep(0.5)
    input("\n\033[1;97mPress Enter to continue...\033[0m")
    return    

def search_categories(connection):
    while True:
        clear()
        title("SEARCH CATEGORIES")
        sleep(0.1) 
        breadcrumb("Home", "Categories", "Search Categories")
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
                    cursor.execute("SELECT * FROM Categories WHERE category_id = %s", (new_id,))
                    categories = cursor.fetchone()

                except  Exception as e:
                        print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return
                
                finally:
                    cursor.close()
                
                if not categories:
                    print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                    sleep(1)
                    if repeat_operation("search", "category", "main menu"):
                        break
                    return

                category_id, category_name, description = categories
                print_category(
                    category_id,
                    category_name,
                    description, pause= False
                )
                sleep(0.5)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                if repeat_operation("search", "category", "main menu"):
                    break
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
                    cursor.execute("SELECT * FROM Categories WHERE LOWER(category_name)=LOWER(%s)",(name,))
                    categories = cursor.fetchone()

                except  Exception as e:
                        print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return
                
                finally:
                    cursor.close()
                
                if not categories:
                    print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                    sleep(1)
                    if repeat_operation("search", "category", "main menu"):
                        break
                    return
                
                category_id, category_name, description = categories
                print_category(
                    category_id,
                    category_name,
                    description
                )
                sleep(0.5)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                if repeat_operation("search", "category", "main menu"):
                    break
                return
            else:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

def update_category(connection):
    while True:
        clear()
        title("UPDATE CATEGORY")
        sleep(0.1) 
        breadcrumb("Home", "Categories", "Update Category")
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
                    cursor.execute("SELECT * FROM Categories WHERE category_id = %s;", (new_id,))
                    categories = cursor.fetchone()

                except  Exception as e:
                        print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return
                
                finally:
                    cursor.close()
                
                if not categories:
                    print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                    sleep(1)
                    if repeat_operation("search", "category", "main menu"):
                        break
                    return
                category_id, category_name, description = categories

                print_category(
                    category_id,
                    category_name,
                    description
                )
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
                    cursor.execute("SELECT * FROM Categories WHERE LOWER(category_name)=LOWER(%s)",(name,))

                    categories = cursor.fetchone()

                except  Exception as e:
                        print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return
                
                finally:
                    cursor.close()
                
                if not categories:
                    print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                    sleep(1)
                    if repeat_operation("search", "category", "main menu"):
                        break
                    return
                
                category_id, category_name, description = categories

                print_category(
                    category_id,
                    category_name,
                    description
                )
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
                new_category_name = get_category_name(
                    connection,
                    category_name
                )

                if new_category_name is None:
                    return
                
                desc = get_description(description)
                
                sleep(0.5)
                review_category_update(category_id,category_name,new_category_name,description,desc)
                sleep(0.5)
                success = save_category_update(connection, "UPDATE Categories SET category_name =%s, description =%s WHERE category_id = %s;", (new_category_name,desc,category_id) )
                if success:
                    if repeat_operation("update", "category", "main menu"):
                        break
                    return

                continue
            elif choice == 1:
                new_category_name = get_category_name(
                    connection,
                    category_name
                )

                if new_category_name is None:
                    return
                
                sleep(0.5)
                review_category_update(category_id,category_name,new_category_name,description, None)
                sleep(0.5)
                success = save_category_update(connection, "UPDATE Categories SET category_name =%s WHERE category_id = %s;", (new_category_name, category_id) )
                if success:
                    if repeat_operation("update", "category", "main menu"):
                        break
                    return

                continue
                
            elif choice == 2:
                desc = get_description(description)

                sleep(0.5)
                review_category_update(category_id,category_name,None,description,desc)
                sleep(0.5)
                success = save_category_update(connection, "UPDATE Categories SET description =%s WHERE category_id = %s;", (desc, category_id) )
                if success:
                    if repeat_operation("update", "category", "main menu"):
                        break
                    return

                continue

            else:
                input("\033[1;97mPress Enter to go back...\033[0m")
                return
        continue

def delete_category(connection):
    clear()
    title("DELETE CATEGORY")
    sleep(0.1) 
    breadcrumb("Home", "Categories", "Delete Category")
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
                cursor.execute("SELECT * FROM Categories WHERE category_id = %s", (new_id,))
                categories = cursor.fetchone()

            except  Exception as e:
                    print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            
            finally:
                    cursor.close()
            
            if not categories:
                print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                sleep(1)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                return
            
            category_id, category_name, description = categories

            print_category(
                category_id,
                category_name,
                description
            )
            sleep(0.5)
            break


        elif choice == 2:
            print("\n\033[1;93mPlease enter the Category Name below....\n")
            sleep(0.5)

            while True:

                try:
                    category_name = input("\033[1;93mCATEGORY NAME: \033[0m").strip()

                except Exception as e:

                    print(f"\033[1;91mFailed to continue with searching the supplier\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return

                if not category_name:
                    print("\033[1;91m❌ Category name cannot be empty\033[0m\n")
                    sleep(1)
                    continue

                if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", category_name):
                    print("\033[1;91m❌ Category name contains invalid characters\033[0m\n")
                    sleep(1)
                    continue

                if len(category_name) > 50:
                            print("\033[1;91m❌ Category name can have a max of 50 characters\033[0m\n")
                            sleep(1)
                            continue
                break

            cursor = connection.cursor(buffered=True)

            try:

                cursor.execute(
                    "SELECT * FROM Categories WHERE LOWER(category_name)=LOWER(%s)",
                    (category_name,)
                )

                category_check = cursor.fetchone()

            except Exception as e:

                print(f"\033[1;91mFailed to load the category\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            finally:
                cursor.close()

            if not category_check:

                print("\033[1;91m✕ No Category Found\033[0m\n")
                sleep(1)

                if repeat_operation("search", "categories", "Delete Category"):
                    break

                return


            cursor = connection.cursor(buffered = True)
            try:
                cursor.execute(
                                """
                                SELECT
                                    category_id,
                                    category_name,
                                    description
                                FROM Categories
                                WHERE LOWER(category_name)=LOWER(%s)
                                """,
                                (category_name,)
                            )
                categories = cursor.fetchone()

            except  Exception as e:
                    print(f"\033[1;91mFailed to load the categories\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return
            
            finally:
                cursor.close()
            
            if not categories:
                print(f"\033[1;91m✕ No Categories Found\033[0m\n")
                sleep(1)
                input("\n\033[1;97mPress Enter to continue...\033[0m")
                return
            
            category_id, category_name, description = categories

            print_category(
                category_id,
                category_name,
                description
            )
            sleep(0.5)
            break

        else:
            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

    print("\033[1;93m┌───────────────────────────────────┐\033[0m") 
    print("\033[1;93m│           \033[1;91mARE YOU SURE?          \033[1;93m │\033[0m")
    print("\033[1;93m├───────────────────────────────────┤\033[0m")
    print("\033[1;93m│  \033[1;93m⚠️ THIS ACTION CANNOT BE UNDONE \033[1;93m │\033[0m")
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
                cursor.execute("DELETE FROM Categories WHERE category_id =%s;",(category_id,))
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


def supplier_exists(connection, supplier_name):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            "SELECT 1 FROM Suppliers WHERE LOWER(supplier_name)=LOWER(%s)",
            (supplier_name,)
        )

        return cursor.fetchone() is not None

    finally:

        cursor.close()
def phone_exists(connection, phone_number, table_name):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(
            f"SELECT 1 FROM {table_name} WHERE phone_number = %s",
            (phone_number,)
        )
        return cursor.fetchone() is not None

    finally:
        cursor.close()
def email_exists(connection, email, table):
    cursor = connection.cursor(buffered=True)

    try:
        cursor.execute(
            f"SELECT 1 FROM {table} WHERE LOWER(email)=LOWER(%s)",
            (email,)
        )
        return cursor.fetchone() is not None

    finally:
        cursor.close()
def get_address(prompt="ADDRESS", max_length = 300):
    while True:
        address = input(f"\033[1;93m{prompt}: \033[0m").strip()

        if len(address) > max_length:
            print(f"\033[1;91m✕ Address can have a maximum of {max_length} characters\033[0m")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z0-9\s,.'#()/:&-]*", address):
            print("\033[1;91m✕ Address contains invalid characters\033[0m")
            sleep(1)
            continue

        return address
def review_new_supplier(supplier_name, address, phone_number, email, contact_person):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;97m│                   REVIEW NEW SUPPLIER                      │\033[0m")
    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print("\033[1;97mName\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(supplier_name)

    print("\033[1;97mAddress\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")

    if address:
        print(address)
    else:
        print("No address")

    print("\033[1;97mEmail\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")

    if email:
        print(email)
    else:
        print("No email")

    print("\033[1;97mPhone Number\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")

    print(phone_number)

    print("\033[1;97mContact Person\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")

    if contact_person:
        print(contact_person)
    else:
        print("No contact person")
    

    print("\n\033[36m──────────────────────────────────────────────────────────────\033[0m")
def print_supplier(supplier_id,supplier_name,phone_number,supplier_email,address,contact_person,pause=True):

    print("\033[36m┌────┬──────────────────────────────┐\033[0m")
    print(f"\033[1;97m│ {'ID':<2} │ {'Supplier Name':<28} │\033[0m")
    print("\033[36m├────┼──────────────────────────────┤\033[0m")
    print(f"│ {supplier_id:<2} │ {supplier_name:<28} │")
    print("\033[36m└────┴──────────────────────────────┘\033[0m")

    print()

    print("\033[1;97mPhone Number\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(phone_number if phone_number else "Not provided")

    print("\n\033[1;97mEmail\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(supplier_email if supplier_email else "Not provided")

    print("\n\033[1;97mAddress\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(address if address else "Not provided")

    print("\n\033[1;97mContact Person\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(contact_person if contact_person else "Not provided")

    print("\n\033[36m──────────────────────────────────────────────\033[0m")

    if pause:
        sleep(0.5)
        input("\n\033[1;97mPress Enter to continue...\033[0m")
def get_supplier_name(connection, current_name=None):

    print("\033[1;93mPlease enter the New Name:\033[0m\n")
    sleep(0.5)

    while True:
        try:
            new_name = input("\033[1;93mSupplier NAME: \033[0m").strip()

        except Exception as e:
            print(f"\033[1;91mFailed to continue with adding the name\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return None

        if not new_name:
            print("\033[1;91m❌ Supplier name cannot be empty\033[0m\n")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", new_name):
            print("\033[1;91m❌ Supplier name contains invalid characters\033[0m\n")
            sleep(1)
            continue

        if len(new_name) > 100:
            print("\033[1;91m❌ Supplier name can have a max of 100 characters\033[0m\n")
            sleep(1)
            continue

        if new_name.lower() == current_name.lower():
            return new_name

        try:
            if supplier_exists(connection, new_name):
                print("\033[1;91m✕ Supplier already exists")
                sleep(1)
                continue

            return new_name

        except Exception as e:
            print(f"\033[1;91mFailed to continue with adding the name\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return None
def review_supplier_update(
    supplier_id,
    old_name, new_name,
    old_phone, new_phone,
    old_email, new_email,
    old_address, new_address,
    old_contact, new_contact
):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;97m│                 REVIEW SUPPLIER UPDATE                     │\033[0m")
    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print(f"\n\033[1;97mSupplier ID : \033[1;93m{supplier_id}\033[0m\n")

    print("\033[1;97mSupplier Name\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {old_name}")
    if new_name != old_name:
        print(f"\033[1;92mUpdated :\033[0m {new_name}")
    print()

    print("\033[1;97mPhone Number\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {old_phone}")
    if new_phone != old_phone:
        print(f"\033[1;92mUpdated :\033[0m {new_phone}")
    print()

    print("\033[1;97mEmail\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {old_email if old_email else 'Not provided'}")
    if new_email != old_email:
        print(f"\033[1;92mUpdated :\033[0m {new_email if new_email else 'Not provided'}")
    print()

    print("\033[1;97mAddress\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {old_address if old_address else 'Not provided'}")
    if new_address != old_address:
        print(f"\033[1;92mUpdated :\033[0m {new_address if new_address else 'Not provided'}")
    print()

    print("\033[1;97mContact Person\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {old_contact if old_contact else 'Not provided'}")
    if new_contact != old_contact:
        print(f"\033[1;92mUpdated :\033[0m {new_contact if new_contact else 'Not provided'}")

    print("\n\033[36m──────────────────────────────────────────────────────────────\033[0m")

def get_phone(connection,table_name, current_phone= None):

    while True:

        try:
            new_phone = input("\033[1;93mSUPPLIER PHONE NUMBER: \033[0m").strip()

        except Exception as e:
            print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return None

        if not new_phone:
            print("\033[1;91m❌ Supplier phone number cannot be empty\033[0m\n")
            sleep(1)
            continue

        if not re.fullmatch(r"^\+?[0-9]{7,15}$", new_phone):
            print("\033[1;91m✕ Enter a valid phone number (7-15 digits, optional '+' prefix)\033[0m")
            sleep(1)
            continue

        if new_phone == current_phone:
            print("\033[1;91m❌ New phone number must be different from the current phone number\033[0m")
            sleep(1)
            continue

        try:

            if phone_exists(connection, new_phone, table_name):
                print("\033[1;91m✕ Supplier phone number already exists\033[0m")
                sleep(1)
                continue

        except Exception as e:

            print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return None

        return new_phone
def get_email(connection, current_email, table, max_length = 255):

    while True:

        try:
            new_email = input("\033[1;93mSUPPLIER EMAIL: \033[0m").strip()

        except Exception as e:
            print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return None

        if new_email:

            if len(new_email) > max_length:
                print(f"\033[1;91m✕ Email can have a maximum of {max_length} characters\033[0m")
                sleep(1)
                continue

            if not re.fullmatch(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                new_email
            ):
                print("\033[1;91m✕ Please enter a valid email address\033[0m")
                sleep(1)
                continue

            try:

                if (
                    new_email.lower() != (current_email or "").lower()
                    and email_exists(connection, new_email, table)
                ):
                    print("\033[1;91m✕ Email already exists\033[0m")
                    sleep(1)
                    continue

            except Exception as e:

                print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return None

        if new_email.lower() == (current_email or "").lower():
            print("\033[1;91m❌ New email must be different from the current email\033[0m")
            sleep(1)
            continue

        return new_email
def get_new_address(connection, current_address, max_length =300):

    while True:

        try:
            new_address = input("\033[1;93mADDRESS: \033[0m").strip()

        except Exception as e:
            print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return None

        if len(new_address) > max_length:
            print(f"\033[1;91m✕ Address can have a maximum of {max_length} characters\033[0m")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z0-9\s,.'#()/:&-]*", new_address):
            print("\033[1;91m✕ Address contains invalid characters\033[0m")
            sleep(1)
            continue

        if new_address == current_address:
            print("\033[1;91m❌ New address must be different from the current address\033[0m")
            sleep(1)
            continue

        return new_address
def get_contact_person(connection, current_contact):

    while True:

        try:
            new_contact = input("\033[1;93mCONTACT PERSON: \033[0m").strip()

        except Exception as e:
            print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            connection.rollback()
            return None

        if new_contact:

            if len(new_contact) > 100:
                print("\033[1;91m✕ Contact person can have a maximum of 100 characters\033[0m")
                sleep(1)
                continue

            if not re.fullmatch(r"[A-Za-z .'-]+", new_contact):
                print("\033[1;91m✕ Contact person contains invalid characters\033[0m")
                sleep(1)
                continue

        if new_contact == current_contact:
            print("\033[1;91m❌ New contact person must be different from the current contact person\033[0m")
            sleep(1)
            continue

        return new_contact


def add_supplier(connection):
    while True:
        clear()
        title("ADD SUPPLIER")
        sleep(0.1) 
        breadcrumb("Home", "Suppliers", "Add Supplier")
        sleep(0.5)
        print("\n\033[1;93mPlease enter the details as prompted:\033[0m\n")
        sleep(0.5)
        while True:
            try:
                supplier_name = input("\033[1;93mSUPPLIER NAME: \033[0m").strip()

            except  Exception as e:
                print(f"\033[1;91mFailed to continue with adding the supplier\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            if not supplier_name:
                print("\033[1;91m❌ Supplier name cannot be empty\033[0m\n")
                sleep(1)
                continue

            if not re.fullmatch(r"[A-Za-z0-9  _.,'()&/+-]+", supplier_name):
                print("\033[1;91m❌ Supplier name contains invalid characters\033[0m\n")
                sleep(1)
                continue

            if len(supplier_name) > 100:
                print("\033[1;91m❌ Suppplier name can have a max of 100 characters\033[0m\n")
                sleep(1)
                continue

            break
            
        while True:
            try:
                phone_number = (input("\033[1;93mSUPPLIER PHONE NUMBER: \033[0m"))

            except  Exception as e:
                print(f"\033[1;91mFailed to continue with adding the supplier\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            if not phone_number:
                print("\033[1;91m❌ Supplier phone number cannot be empty\033[0m\n")
                sleep(1)
                continue

            if not re.fullmatch(r"^\+?[0-9]{7,15}$", phone_number):
                print("\033[1;91m✕ Enter a valid phone number (7-15 digits, optional '+' prefix)\033[0m")
                sleep(1)
                continue

            if not (7 <= len(phone_number) <= 15):
                print("\033[1;91m✕ Phone number must contain between 7 and 15 digits\033[0m")
                sleep(1)
                continue

            try:
                if phone_exists(connection, phone_number, "Suppliers"):  
                    print("\033[1;91m✕ Supplier phone number already exists")
                    sleep(1)
                    continue
                else:
                    break

            except  Exception as e:
                print(f"\033[1;91mFailed to continue with adding the supplier\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return
        
        print("\033[1;93mPlease enter the supplier email: <Press Enter to leave it blank>\033[0m\n")
        sleep(0.5)
        while True:
            try:
                supplier_email = (input("\033[1;93mSUPPLIER EMAIL: \033[0m")).strip()

            except  Exception as e:
                print(f"\033[1;91mFailed to continue with adding the supplier\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            moveon = True
            if not supplier_email:
                print("\033[1;93mContinue with blank email address?\n[1] YES\n[2] NO\033[0m\n")
                while True:
                    try:
                        choice = int(input("\033[1;93mChoice: \033[0m"))

                    except ValueError:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if choice == 1:
                        moveon = True
                    elif choice == 2:
                        moveon = False
                    else:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue  

                    break
            if not(moveon):
                continue

            # Blank email is allowed
            if supplier_email == "":
                break

            if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", supplier_email):
                print("\033[1;91m✕ Please enter a valid email address\033[0m")
                sleep(1)
                continue

            if len(supplier_email) > 255:
                print("\033[1;91m✕ Email can have a maximum of 255 characters\033[0m")
                sleep(1)
                continue

            try:
                if email_exists(connection, supplier_email, "Suppliers"):  
                    print("\033[1;91m✕ Supplier email already exists")
                    sleep(1)
                    continue
                else:
                    break

            except  Exception as e:
                print(f"\033[1;91mFailed to continue with adding the supplier\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

        print("\033[1;93mPlease enter the supplier address: <Press Enter to leave it blank>\033[0m\n")
        sleep(0.5)
        while True: 
            try:
                address = get_address()

            except  Exception as e:
                print(f"\033[1;91mFailed to continue with adding the supplier\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return
            
            moveon = True
            if not address:
                print("\033[1;93mContinue with blank address?\n[1] YES\n[2] NO\033[0m\n")
                while True:
                    try:
                        choice = int(input("\033[1;93mChoice: \033[0m"))

                    except ValueError:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if choice == 1:
                        moveon = True
                    elif choice == 2:
                        moveon = False
                    else:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue  

                    break
                if not(moveon):
                    continue

            break

        print("\033[1;93mPlease enter the Contact Person: <Press Enter to leave it blank>\033[0m\n")
        sleep(0.5)

        while True:
            try:
                contact_person = input("\033[1;93mCONTACT PERSON: \033[0m").strip()

            except Exception as e:
                print(f"\033[1;91mFailed to continue with adding the contact person\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            # Blank is allowed
            if not contact_person:
                break

            if len(contact_person) > 100:
                print("\033[1;91m✕ Contact person can have a maximum of 100 characters\033[0m")
                sleep(1)
                continue

            if not re.fullmatch(r"[A-Za-z .'-]+", contact_person):
                print("\033[1;91m✕ Contact person contains invalid characters\033[0m")
                sleep(1)
                continue

            break

        sleep(0.5)
        review_new_supplier(supplier_name,address, phone_number, supplier_email,  contact_person)
        sleep(0.5)
        if confirm_changes():
            print("\033[1;93mInitializing supplier...")
            sleep(0.5)

            cursor = connection.cursor(buffered=True)

            try:
                cursor.execute("INSERT INTO Suppliers (supplier_name, address, phone_number, email, contact_person) VALUES (%s, %s, %s, %s, %s)", ( supplier_name,address, phone_number, supplier_email,  contact_person ))

                connection.commit()

                print("\033[1;92m✓ Supplier added successfully\033[0m")
                sleep(1)

                if repeat_operation("add", "supplier"):
                    continue
                return

            except Exception as e:
                print(f"\033[1;91mFailed to add the supplier\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            finally:
                cursor.close()

        else:

            print("\033[1;97mCancelling...\033[0m")
            sleep(1)

            if repeat_operation("add", "supplier"):
                continue

            return
  
def view_suppliers(connection):
    while True:
        clear()
        title("VIEW SUPPLIERS")
        sleep(0.1)
        breadcrumb("Home", "Suppliers", "View Suppliers")
        sleep(0.5)

        print(
            "\n\033[1;93mSort By:\n"
            "\033[1;97m"
            "[1] Supplier ID (Ascending)\n"
            "[2] Supplier ID (Descending)\n"
            "[3] Supplier Name (A-Z)\n"
            "[4] Supplier Name (Z-A)\n\n"
            "[0] Back\033[0m"
        )

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
                order_by = "supplier_id ASC"
                break

            elif choice == 2:
                order_by = "supplier_id DESC"
                break

            elif choice == 3:
                order_by = "supplier_name ASC"
                break

            elif choice == 4:
                order_by = "supplier_name DESC"
                break

            else:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                f"""
                SELECT
                    supplier_id,
                    supplier_name,
                    phone_number,
                    email,
                    address,
                    contact_person
                FROM Suppliers
                ORDER BY {order_by};
                """
            )

            suppliers = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the suppliers\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

            sleep(1)

            connection.rollback()

            return

        finally:
            cursor.close()

        if not suppliers:

            print("\n\033[1;91m❌ No suppliers found.\033[0m")
            sleep(1)
            input("\n\033[1;97mPress Enter to continue...\033[0m")
            return

        clear()
        title("VIEW SUPPLIERS")
        breadcrumb("Home", "Suppliers", "View Suppliers")

        print()

        for supplier in suppliers:

            (
                supplier_id,
                supplier_name,
                phone_number,
                supplier_email,
                address,
                contact_person
            ) = supplier

            print_supplier(
                supplier_id,
                supplier_name,
                phone_number,
                supplier_email,
                address,
                contact_person,
                pause=False
            )

            print()

        input("\n\033[1;97mPress Enter to continue...\033[0m")

        return

def search_supplier(connection):
    while True:
        clear()
        title("SEARCH SUPPLIER")
        sleep(0.1)
        breadcrumb("Home", "Suppliers", "Search Supplier")
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Type:\n"
            "\033[1;97m"
            "[1] Search by ID\n"
            "[2] Search by Supplier Name\n"
            "[3] Search by Phone Number\n"
            "[4] Search by Email\n\n"
            "[0] Back\033[0m"
        )

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

                print("\n\033[1;93mPlease enter the Supplier ID below....\n")
                sleep(0.5)

                while True:
                    try:
                        supplier_id = int(input("\033[1;93mSUPPLIER ID: \033[0m"))

                    except ValueError:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if supplier_id <= 0:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            supplier_id,
                            supplier_name,
                            address,
                            phone_number,
                            email,
                            contact_person
                        FROM Suppliers
                        WHERE supplier_id = %s
                        """,
                        (supplier_id,)
                    )

                    supplier = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the supplier\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    connection.rollback()

                    return

                finally:
                    cursor.close()

                if not supplier:

                    print("\033[1;91m✕ No Supplier Found\033[0m")
                    sleep(1)

                    if repeat_operation("search", "supplier"):
                        break

                    return

                (
                    supplier_id,
                    supplier_name,
                    address,
                    phone_number,
                    supplier_email,
                    contact_person
                ) = supplier

                print_supplier(
                    supplier_id,
                    supplier_name,
                    phone_number,
                    supplier_email,
                    address,
                    contact_person
                )

                if repeat_operation("search", "supplier"):
                    break

                return

            elif choice == 2:

                print("\n\033[1;93mPlease enter the Supplier Name below....\n")
                sleep(0.5)

                while True:
                    try:
                        supplier_name = input("\033[1;93mSUPPLIER NAME: \033[0m").strip()

                    except Exception as e:
                        print(f"\033[1;91mFailed to continue with searching the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    if not supplier_name:
                        print("\033[1;91m❌ Supplier name cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", supplier_name):
                        print("\033[1;91m❌ Supplier name contains invalid characters\033[0m\n")
                        sleep(1)
                        continue

                    if len(supplier_name) > 100:
                        print("\033[1;91m❌ Supplier name can have a max of 100 characters\033[0m\n")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            supplier_id,
                            supplier_name,
                            address,
                            phone_number,
                            email,
                            contact_person
                        FROM Suppliers
                        WHERE LOWER(supplier_name) = LOWER(%s)
                        """,
                        (supplier_name,)
                    )

                    supplier = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the supplier\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    connection.rollback()

                    return

                finally:
                    cursor.close()

                if not supplier:

                    print("\033[1;91m✕ No Supplier Found\033[0m")
                    sleep(1)

                    if repeat_operation("search", "supplier"):
                        break

                    return

                (
                    supplier_id,
                    supplier_name,
                    address,
                    phone_number,
                    supplier_email,
                    contact_person
                ) = supplier

                print_supplier(
                    supplier_id,
                    supplier_name,
                    phone_number,
                    supplier_email,
                    address,
                    contact_person
                )

                if repeat_operation("search", "supplier"):
                    break

                return

            elif choice == 3:

                print("\n\033[1;93mPlease enter the Supplier Phone Number below....\n")
                sleep(0.5)

                while True:
                    try:
                        phone_number = input("\033[1;93mSUPPLIER PHONE NUMBER: \033[0m").strip()

                    except Exception as e:
                        print(f"\033[1;91mFailed to continue with searching the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    if not phone_number:
                        print("\033[1;91m❌ Supplier phone number cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if not re.fullmatch(r"^\+?[0-9]{7,15}$", phone_number):
                        print("\033[1;91m✕ Enter a valid phone number (7-15 digits, optional '+' prefix)\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            supplier_id,
                            supplier_name,
                            address,
                            phone_number,
                            email,
                            contact_person
                        FROM Suppliers
                        WHERE phone_number = %s
                        """,
                        (phone_number,)
                    )

                    supplier = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the supplier\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    connection.rollback()

                    return

                finally:
                    cursor.close()

                if not supplier:

                    print("\033[1;91m✕ No Supplier Found\033[0m")
                    sleep(1)

                    if repeat_operation("search", "supplier"):
                        break

                    return

                (
                    supplier_id,
                    supplier_name,
                    address,
                    phone_number,
                    supplier_email,
                    contact_person
                ) = supplier

                print_supplier(
                    supplier_id,
                    supplier_name,
                    phone_number,
                    supplier_email,
                    address,
                    contact_person
                )

                if repeat_operation("search", "supplier"):
                    break

                return

            elif choice == 4:

                print("\n\033[1;93mPlease enter the Supplier Email below....\n")
                sleep(0.5)

                while True:
                    try:
                        supplier_email = input("\033[1;93mSUPPLIER EMAIL: \033[0m").strip()

                    except Exception as e:
                        print(f"\033[1;91mFailed to continue with searching the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    if not supplier_email:
                        print("\033[1;91m❌ Supplier email cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if len(supplier_email) > 255:
                        print("\033[1;91m✕ Email can have a maximum of 255 characters\033[0m")
                        sleep(1)
                        continue

                    if not re.fullmatch(
                        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                        supplier_email
                    ):
                        print("\033[1;91m✕ Please enter a valid email address\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            supplier_id,
                            supplier_name,
                            address,
                            phone_number,
                            email,
                            contact_person
                        FROM Suppliers
                        WHERE LOWER(email) = LOWER(%s)
                        """,
                        (supplier_email,)
                    )

                    supplier = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the supplier\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    connection.rollback()

                    return

                finally:
                    cursor.close()

                if not supplier:

                    print("\033[1;91m✕ No Supplier Found\033[0m")
                    sleep(1)

                    if repeat_operation("search", "supplier"):
                        break

                    return

                (
                    supplier_id,
                    supplier_name,
                    address,
                    phone_number,
                    supplier_email,
                    contact_person
                ) = supplier

                print_supplier(
                    supplier_id,
                    supplier_name,
                    phone_number,
                    supplier_email,
                    address,
                    contact_person
                )

                if repeat_operation("search", "supplier"):
                    break

                return

            else:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

def update_supplier(connection):
    while True:
        clear()
        title("UPDATE SUPPLIER")
        sleep(0.1) 
        breadcrumb("Home", "Suppliers", "Update Supplier")
        sleep(0.5)
        print("\n\033[1;93mSearch Supplier:\n\033[1;97m[1] Search by ID\n[2] Search by Name\n\n[0] Back\033[0m")
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
                    cursor.execute("SELECT (supplier_id, supplier_name, contact_person, phone_number, supplier_email, address) FROM Suppliers WHERE supplier_id = %s;", (new_id,))
                    suppliers = cursor.fetchone()

                except  Exception as e:
                        print(f"\033[1;91mFailed to load the suppliers\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return
                
                finally:
                    cursor.close()
                
                if not suppliers:
                    print(f"\033[1;91m✕ No Supplier Found\033[0m\n")
                    sleep(1)
                    if repeat_operation("search", "supplier", "menu"):
                        break
                    return
                supplier_id, supplier_name, contact_person, phone_number, supplier_email, address = suppliers

                print_supplier(
                    supplier_id,supplier_name,phone_number,supplier_email,address,contact_person,pause=True
                )
                sleep(0.5)
                break

            elif choice == 2:
                print("\n\033[1;93mPlease enter the name below....\n")
                sleep(0.5)
                while True:
                    try:
                        supplier_name = input("\033[1;93mSUPPLIER NAME: \033[0m").strip()

                    except  Exception as e:
                        print(f"\033[1;91mFailed to continue with searching the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    if not supplier_name:
                        print("\033[1;91m❌ Supplier name cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if not re.fullmatch(r"[A-Za-z0-9  _.,'()&/+-]+", supplier_name):
                        print("\033[1;91m❌ Supplier name contains invalid characters\033[0m\n")
                        sleep(1)
                        continue

                    if len(supplier_name) > 100:
                        print("\033[1;91m❌ Suppplier name can have a max of 100 characters\033[0m\n")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered = True)
                try:
                    cursor.execute("SELECT (supplier_id, supplier_name, contact_person, phone_number, supplier_email, address) FROM Suppliers WHERE LOWER(supplier_name)=LOWER(%s)",(supplier_name,))

                    suppliers = cursor.fetchone()

                except  Exception as e:
                        print(f"\033[1;91mFailed to load the suppliers\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return
                
                finally:
                    cursor.close()
                
                if not suppliers:
                    print(f"\033[1;91m✕ No Supplier Found\033[0m\n")
                    sleep(1)
                    if repeat_operation("search", "supplier", "menu"):
                        break
                    return
                
                supplier_id, supplier_name, contact_person, phone_number, supplier_email, address = suppliers

                print_supplier(
                    supplier_id,supplier_name,phone_number,supplier_email,address,contact_person,pause=True
                )
                sleep(0.5)
                break

            else:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

        while True:
            print("\n\033[1;93mUpdate Supplier:\033[0m\n")
            print("\033[1;97m[1] Name")
            print("[2] Phone number")
            print("[3] Email")
            print("[4] Address")
            print("[5] Contact Person")
            print("[6] Update All")
            print("[0] ← Back\033[0m\n")

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))
            except ValueError:
                print("\033[1;91mEnter a valid input.\033[0m")
                sleep(1)
                continue

            if choice not in range(0, 7):
                print("\033[1;91mEnter a valid choice.\033[0m")
                sleep(1)
                continue
                
            if choice == 1:
                new_supplier_name = get_supplier_name(
                    connection,
                    supplier_name
                )

                if new_supplier_name is None:
                    continue
                
                
                sleep(0.5)
                review_supplier_update(
                    supplier_id,
                    supplier_name,
                    new_supplier_name,
                    phone_number,
                    phone_number,
                    supplier_email,
                    supplier_email,
                    address,
                    address,
                    contact_person,
                    contact_person
                )

                sleep(0.5)
                if not confirm_changes():
                    print("\033[1;97mCancelling...\033[0m")
                    sleep(1)

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return
                
                success = execute_update(
                    connection,
                    """
                    UPDATE Suppliers
                    SET supplier_name = %s
                    WHERE supplier_id = %s
                    """,
                    (
                        new_supplier_name,
                        supplier_id
                    ),
                    "supplier"
                )

                if success:
                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break
                    return

                continue

            elif choice == 2:

                print("\n\033[1;93mPlease enter the updated Supplier Phone Number below....\n")
                sleep(0.5)

                while True:
                    try:
                        new_phone_number = input("\033[1;93mSUPPLIER PHONE NUMBER: \033[0m").strip()

                    except Exception as e:
                        print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    if not new_phone_number:
                        print("\033[1;91m❌ Supplier phone number cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if not re.fullmatch(r"^\+?[0-9]{7,15}$", new_phone_number):
                        print("\033[1;91m✕ Enter a valid phone number (7-15 digits, optional '+' prefix)\033[0m")
                        sleep(1)
                        continue

                    if new_phone_number == phone_number:
                        print("\033[1;91m❌ New phone number must be different from the current phone number\033[0m\n")
                        sleep(1)
                        continue

                    try:
                        if phone_exists(connection, new_phone_number, "Suppliers"):
                            print("\033[1;91m✕ Supplier phone number already exists\033[0m")
                            sleep(1)
                            continue

                    except Exception as e:
                        print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    break

                review_supplier_update(
                    supplier_id,
                    supplier_name, supplier_name,
                    phone_number, new_phone_number,
                    supplier_email, supplier_email,
                    address, address,
                    contact_person, contact_person
                )

                sleep(0.5)

                if not confirm_changes():

                    print("\033[1;97mCancelling...\033[0m")
                    sleep(1)

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return

                success = execute_update(
                    connection,
                    """
                    UPDATE Suppliers
                    SET phone_number = %s
                    WHERE supplier_id = %s
                    """,
                    (
                        new_phone_number,
                        supplier_id
                    ),
                    "supplier"
                )

                if success:

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return
                
            elif choice == 3:

                print("\n\033[1;93mPlease enter the updated Supplier Email: <Press Enter to leave it blank>\033[0m\n")
                sleep(0.5)

                while True:
                    try:
                        new_supplier_email = input("\033[1;93mSUPPLIER EMAIL: \033[0m").strip()

                    except Exception as e:
                        print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    if new_supplier_email:

                        if len(new_supplier_email) > 255:
                            print("\033[1;91m✕ Email can have a maximum of 255 characters\033[0m")
                            sleep(1)
                            continue

                        if not re.fullmatch(
                            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                            new_supplier_email
                        ):
                            print("\033[1;91m✕ Please enter a valid email address\033[0m")
                            sleep(1)
                            continue

                        try:
                            if email_exists(connection, new_supplier_email, "Suppliers"):
                                print("\033[1;91m✕ Supplier email already exists\033[0m")
                                sleep(1)
                                continue

                        except Exception as e:
                            print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
                            sleep(0.5)
                            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                            sleep(1)
                            connection.rollback()
                            return

                    if new_supplier_email.lower() == (supplier_email or "").lower():
                        print("\033[1;91m❌ New email must be different from the current email\033[0m\n")
                        sleep(1)
                        continue

                    break

                review_supplier_update(
                    supplier_id,
                    supplier_name, supplier_name,
                    phone_number, phone_number,
                    supplier_email, new_supplier_email,
                    address, address,
                    contact_person, contact_person
                )

                sleep(0.5)

                if not confirm_changes():

                    print("\033[1;97mCancelling...\033[0m")
                    sleep(1)

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return

                success = execute_update(
                    connection,
                    """
                    UPDATE Suppliers
                    SET email = %s
                    WHERE supplier_id = %s
                    """,
                    (
                        new_supplier_email,
                        supplier_id
                    ),
                    "supplier"
                )

                if success:

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return

            elif choice == 4:

                print("\n\033[1;93mPlease enter the updated Supplier Address: <Press Enter to leave it blank>\033[0m\n")
                sleep(0.5)

                while True:
                    try:
                        new_address = get_new_address(connection, address)

                    except Exception as e:
                        print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    if new_address == address:
                        print("\033[1;91m❌ New address must be different from the current address\033[0m\n")
                        sleep(1)
                        continue

                    break

                review_supplier_update(
                    supplier_id,
                    supplier_name, supplier_name,
                    phone_number, phone_number,
                    supplier_email, supplier_email,
                    address, new_address,
                    contact_person, contact_person
                )

                sleep(0.5)

                if not confirm_changes():

                    print("\033[1;97mCancelling...\033[0m")
                    sleep(1)

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return

                success = execute_update(
                    connection,
                    """
                    UPDATE Suppliers
                    SET address = %s
                    WHERE supplier_id = %s
                    """,
                    (
                        new_address,
                        supplier_id
                    ),
                    "supplier"
                )

                if success:

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return
            
            elif choice == 5:

                print("\n\033[1;93mPlease enter the updated Contact Person: <Press Enter to leave it blank>\033[0m\n")
                sleep(0.5)

                while True:
                    try:
                        new_contact_person = input("\033[1;93mCONTACT PERSON: \033[0m").strip()

                    except Exception as e:
                        print(f"\033[1;91mFailed to continue with updating the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    if new_contact_person:

                        if len(new_contact_person) > 100:
                            print("\033[1;91m✕ Contact person can have a maximum of 100 characters\033[0m")
                            sleep(1)
                            continue

                        if not re.fullmatch(r"[A-Za-z .'-]+", new_contact_person):
                            print("\033[1;91m✕ Contact person contains invalid characters\033[0m")
                            sleep(1)
                            continue

                    if new_contact_person == contact_person:
                        print("\033[1;91m❌ New contact person must be different from the current contact person\033[0m\n")
                        sleep(1)
                        continue

                    break

                review_supplier_update(
                    supplier_id,
                    supplier_name, supplier_name,
                    phone_number, phone_number,
                    supplier_email, supplier_email,
                    address, address,
                    contact_person, new_contact_person
                )

                sleep(0.5)

                if not confirm_changes():

                    print("\033[1;97mCancelling...\033[0m")
                    sleep(1)

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return

                success = execute_update(
                    connection,
                    """
                    UPDATE Suppliers
                    SET contact_person = %s
                    WHERE supplier_id = %s
                    """,
                    (
                        new_contact_person,
                        supplier_id
                    ),
                    "supplier"
                )

                if success:

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return
                
            elif choice == 6:

                print("\n\033[1;93mPlease enter the updated supplier details.\033[0m\n")
                sleep(0.5)

                new_supplier_name = get_supplier_name(
                    connection,
                    supplier_name
                )

                if new_supplier_name is None:
                    continue

                new_phone_number = get_phone(
                    connection,
                    "Suppliers",
                    phone_number
                )

                if new_phone_number is None:
                    continue

                new_supplier_email = get_email(
                    connection,
                    supplier_email,
                    "Suppliers"
                )

                if new_supplier_email is None:
                    continue

                new_address = get_new_address(
                    connection,
                    address
                )

                if new_address is None:
                    continue

                new_contact_person = get_contact_person(
                    connection,
                    contact_person
                )

                if new_contact_person is None:
                    continue

                review_supplier_update(
                    supplier_id,
                    supplier_name, new_supplier_name,
                    phone_number, new_phone_number,
                    supplier_email, new_supplier_email,
                    address, new_address,
                    contact_person, new_contact_person
                )

                sleep(0.5)

                if not confirm_changes():

                    print("\033[1;97mCancelling...\033[0m")
                    sleep(1)

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return

                success = execute_update(
                    connection,
                    """
                    UPDATE Suppliers
                    SET
                        supplier_name = %s,
                        phone_number = %s,
                        email = %s,
                        address = %s,
                        contact_person = %s
                    WHERE supplier_id = %s
                    """,
                    (
                        new_supplier_name,
                        new_phone_number,
                        new_supplier_email,
                        new_address,
                        new_contact_person,
                        supplier_id
                    ),
                    "supplier"
                )

                if success:

                    if repeat_operation("update", "supplier", "Update Supplier"):
                        break

                    return
            
        continue

def delete_supplier(connection):
    while True:
        clear()
        title("DELETE SUPPLIER")
        sleep(0.1)
        breadcrumb("Home", "Suppliers", "Delete Supplier")
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Supplier:\033[0m\n"
            "\033[1;97m"
            "[1] Search by ID\n"
            "[2] Search by Name\n\n"
            "[0] Back\033[0m"
        )

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

                print("\n\033[1;93mPlease enter the ID below....\n")
                sleep(0.5)

                while True:

                    try:
                        supplier_id = int(input("\033[1;93mID: \033[0m"))

                    except ValueError:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if supplier_id <= 0:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        "SELECT * FROM Suppliers WHERE supplier_id = %s",
                        (supplier_id,)
                    )

                    supplier = cursor.fetchone()

                except Exception as e:

                    print(f"\033[1;91mFailed to load the supplier\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return

                finally:
                    cursor.close()

                if not supplier:

                    print("\033[1;91m✕ No Supplier Found\033[0m\n")
                    sleep(1)

                    if repeat_operation("search", "supplier", "Delete Supplier"):
                        break

                    return

                (
                    supplier_id,
                    supplier_name,
                    contact_person,
                    phone_number,
                    supplier_email,
                    address,
                    created_at,
                    updated_at
                ) = supplier

                print_supplier(
                    supplier_id,
                    supplier_name,
                    phone_number,
                    supplier_email,
                    address,
                    contact_person
                )

                sleep(0.5)

                break

            elif choice == 2:

                print("\n\033[1;93mPlease enter the Supplier Name below....\n")
                sleep(0.5)

                while True:

                    try:
                        supplier_name = input("\033[1;93mSUPPLIER NAME: \033[0m").strip()

                    except Exception as e:

                        print(f"\033[1;91mFailed to continue with searching the supplier\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        connection.rollback()
                        return

                    if not supplier_name:
                        print("\033[1;91m❌ Supplier name cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", supplier_name):
                        print("\033[1;91m❌ Supplier name contains invalid characters\033[0m\n")
                        sleep(1)
                        continue

                    if len(supplier_name) > 100:
                        print("\033[1;91m❌ Supplier name can have a maximum of 100 characters\033[0m\n")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        "SELECT * FROM Suppliers WHERE LOWER(supplier_name)=LOWER(%s)",
                        (supplier_name,)
                    )

                    supplier = cursor.fetchone()

                except Exception as e:

                    print(f"\033[1;91mFailed to load the supplier\n\033[1;93mReason: {e}\033[0m")
                    sleep(0.5)
                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                    sleep(1)
                    connection.rollback()
                    return

                finally:
                    cursor.close()

                if not supplier:

                    print("\033[1;91m✕ No Supplier Found\033[0m\n")
                    sleep(1)

                    if repeat_operation("search", "supplier", "Delete Supplier"):
                        break

                    return

                (
                    supplier_id,
                    supplier_name,
                    contact_person,
                    phone_number,
                    supplier_email,
                    address,
                    created_at,
                    updated_at
                ) = supplier

                print_supplier(
                    supplier_id,
                    supplier_name,
                    phone_number,
                    supplier_email,
                    address,
                    contact_person
                )

                sleep(0.5)

                break

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

               
        sleep(0.5)

        print("\033[1;93m┌───────────────────────────────────┐\033[0m") 
        print("\033[1;93m│           \033[1;91mARE YOU SURE?          \033[1;93m │\033[0m")
        print("\033[1;93m├───────────────────────────────────┤\033[0m")
        print("\033[1;93m│  \033[1;93m⚠️  THIS ACTION CANNOT BE UNDONE \033[1;93m │\033[0m")
        print("\033[1;93m├─────────────────┬─────────────────┤\033[0m")
        print(f"\033[1;93m│ \033[1;97m{"   [1] \033[1;92mYES     ":<10} \033[1;93m│ \033[1;97m{"    [2] \033[1;91mNO ":<22} \033[1;93m│")
        print("\033[1;93m└─────────────────┴─────────────────┘\033[0m")
        
        sleep(0.5)

        while True:

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 2:

                print("\033[1;97mCancelling...\033[0m")
                sleep(1)

                if repeat_operation("delete", "supplier", "Delete Supplier"):
                    break

                return

            elif choice == 1:

                print("\033[1;93mDeleting supplier...\033[0m")
                sleep(0.5)

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        DELETE FROM Suppliers
                        WHERE supplier_id = %s
                        """,
                        (supplier_id,)
                    )

                    connection.commit()

                    print("\033[1;92m✓ Supplier deleted successfully\033[0m")
                    sleep(1)

                    if repeat_operation("delete", "supplier", "Delete Supplier"):
                        break

                    return

                except mysql.connector.IntegrityError:

                    connection.rollback()

                    print(
                        "\033[1;91m❌ This supplier cannot be deleted because purchases are linked to it.\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease update or remove those purchase records first.\033[0m\n"
                    )

                    sleep(1)

                    if repeat_operation("delete", "supplier", "Delete Supplier"):
                        break

                    return

                except Exception as e:

                    connection.rollback()

                    print(
                        f"\033[1;91mFailed to delete the supplier\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    return

                finally:

                    cursor.close()

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

        continue

        
def get_product_name(connection, current_name=None):

    while True:

        try:
            product_name = input("\033[1;93mPRODUCT NAME: \033[0m").strip()

        except Exception as e:

            print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)

            connection.rollback()
            return None

        if not product_name:
            print("\033[1;91m❌ Product name cannot be empty\033[0m\n")
            sleep(1)
            continue

        if len(product_name) > 150:
            print("\033[1;91m❌ Product name can have a maximum of 150 characters\033[0m\n")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", product_name):
            print("\033[1;91m❌ Product name contains invalid characters\033[0m\n")
            sleep(1)
            continue

        if current_name and product_name.lower() == current_name.lower():
            return current_name

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                "SELECT 1 FROM Products WHERE LOWER(product_name)=LOWER(%s)",
                (product_name,)
            )

            if cursor.fetchone():
                print("\033[1;91m✕ Product already exists\033[0m")
                sleep(1)
                continue

        finally:
            cursor.close()

        return product_name
def get_buying_price():

    while True:

        try:
            buying_price = float(input("\033[1;93mBUYING PRICE: ₹\033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid price\033[0m")
            sleep(1)
            continue

        if buying_price < 0:
            print("\033[1;91m❌ Buying price cannot be negative\033[0m")
            sleep(1)
            continue

        return buying_price
def get_selling_price(buying_price, current_price=None):

    while True:

        try:
            selling_price = float(input("\033[1;93mSELLING PRICE: ₹\033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid price\033[0m")
            sleep(1)
            continue

        if selling_price < 0:
            print("\033[1;91m❌ Selling price cannot be negative\033[0m")
            sleep(1)
            continue

        if selling_price < buying_price:
            print("\033[1;91m❌ Selling price cannot be less than buying price\033[0m")
            sleep(1)
            continue

        if current_price is not None and selling_price == current_price:
            return current_price

        return selling_price
def get_quantity(current_quantity=None):

    while True:

        try:
            quantity = int(input("\033[1;93mQUANTITY: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid quantity\033[0m")
            sleep(1)
            continue

        if quantity < 0:
            print("\033[1;91m❌ Quantity cannot be negative\033[0m")
            sleep(1)
            continue

        if current_quantity is not None and quantity == current_quantity:
            return current_quantity

        return quantity
def get_reorder_level(current_level=None):

    while True:

        try:
            reorder_level = int(input("\033[1;93mREORDER LEVEL: \033[0m"))

        except ValueError:
            print("\033[1;91mEnter a valid reorder level\033[0m")
            sleep(1)
            continue

        if reorder_level < 0:
            print("\033[1;91m❌ Reorder level cannot be negative\033[0m")
            sleep(1)
            continue

        if current_level is not None and reorder_level == current_level:
            return current_level

        return reorder_level
def get_product_description(current_description=None):

    print("\033[1;93mPlease enter the Product Description: <Press Enter to leave it blank>\033[0m\n")
    sleep(0.5)

    while True:

        try:
            description = input("\033[1;93mDESCRIPTION: \033[0m")

        except Exception:
            return None

        if len(description) > 1000:
            print("\033[1;91m❌ Description can have a maximum of 1000 characters\033[0m")
            sleep(1)
            continue

        if current_description is not None and description == current_description:
            return current_description

        return description
def review_new_product(
    product_name,
    category_name,
    supplier_name,
    buying_price,
    selling_price,
    quantity,
    reorder_level,
    description
):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;97m│                   REVIEW NEW PRODUCT                       │\033[0m")
    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print("\033[1;97mProduct Name\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(product_name)

    print("\n\033[1;97mCategory\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(category_name)

    print("\n\033[1;97mSupplier\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(supplier_name)

    print("\n\033[1;97mBuying Price\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"₹{buying_price:.2f}")

    print("\n\033[1;97mSelling Price\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"₹{selling_price:.2f}")

    print("\n\033[1;97mQuantity\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(quantity)

    print("\n\033[1;97mReorder Level\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(reorder_level)

    print("\n\033[1;97mDescription\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")

    if description:
        print(description)
    else:
        print("No description")

    print("\n\033[36m──────────────────────────────────────────────────────────────\033[0m")
def print_product(
    product_id,
    product_name,
    category_name,
    supplier_name,
    buying_price,
    selling_price,
    quantity,
    reorder_level,
    description,
    pause=True
):

    print("\033[36m┌────┬──────────────────────────────┐\033[0m")
    print(f"\033[1;97m│ {'ID':<2} │ {'Product Name':<28} │\033[0m")
    print("\033[36m├────┼──────────────────────────────┤\033[0m")
    print(f"│ {product_id:<2} │ {product_name:<28} │")
    print("\033[36m└────┴──────────────────────────────┘\033[0m")

    print()

    print("\033[1;97mCategory\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(category_name)

    print("\n\033[1;97mSupplier\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(supplier_name)

    print("\n\033[1;97mBuying Price\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(f"₹{buying_price:.2f}")

    print("\n\033[1;97mSelling Price\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(f"₹{selling_price:.2f}")

    print("\n\033[1;97mQuantity\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(quantity)

    print("\n\033[1;97mReorder Level\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")
    print(reorder_level)

    print("\n\033[1;97mDescription\033[0m")
    print("\033[36m──────────────────────────────────────────────\033[0m")

    if description:
        print(description)
    else:
        print("No description available.")

    print("\033[36m──────────────────────────────────────────────\033[0m")

    if pause:
        sleep(0.5)
        input("\n\033[1;97mPress Enter to continue...\033[0m")
def review_product_update(
    product_id,

    product_name,
    new_product_name,

    category_name,
    new_category_name,

    supplier_name,
    new_supplier_name,

    buying_price,
    new_buying_price,

    selling_price,
    new_selling_price,

    quantity,
    new_quantity,

    reorder_level,
    new_reorder_level,

    description,
    new_description
):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;97m│                 REVIEW PRODUCT UPDATE                      │\033[0m")
    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print(f"\n\033[1;97mProduct ID : \033[1;93m{product_id}\033[0m\n")

    print("\033[1;97mProduct Name\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {product_name}")

    if new_product_name is not None:
        print(f"\033[1;92mUpdated :\033[0m {new_product_name}")

    print()

    print("\033[1;97mCategory\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {category_name}")

    if new_category_name is not None:
        print(f"\033[1;92mUpdated :\033[0m {new_category_name}")

    print()

    print("\033[1;97mSupplier\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {supplier_name}")

    if new_supplier_name is not None:
        print(f"\033[1;92mUpdated :\033[0m {new_supplier_name}")

    print()

    print("\033[1;97mBuying Price\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m ₹{buying_price:.2f}")

    if new_buying_price is not None:
        print(f"\033[1;92mUpdated :\033[0m ₹{new_buying_price:.2f}")

    print()

    print("\033[1;97mSelling Price\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m ₹{selling_price:.2f}")

    if new_selling_price is not None:
        print(f"\033[1;92mUpdated :\033[0m ₹{new_selling_price:.2f}")

    print()

    print("\033[1;97mQuantity\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {quantity}")

    if new_quantity is not None:
        print(f"\033[1;92mUpdated :\033[0m {new_quantity}")

    print()

    print("\033[1;97mReorder Level\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")
    print(f"\033[1;93mCurrent :\033[0m {reorder_level}")

    if new_reorder_level is not None:
        print(f"\033[1;92mUpdated :\033[0m {new_reorder_level}")

    print()

    print("\033[1;97mDescription\033[0m")
    print("\033[36m──────────────────────────────────────────────────────────────\033[0m")

    print("\033[1;93mCurrent :\033[0m")

    if description:
        print(description)
    else:
        print("No description")

    if new_description is not None:
        print("\n\033[1;92mUpdated :\033[0m")

        if new_description:
            print(new_description)
        else:
            print("No description")

    print("\n\033[36m──────────────────────────────────────────────────────────────\033[0m")


def add_product(connection):
    while True:

        clear()
        title("ADD PRODUCT")
        sleep(0.1)
        breadcrumb("Home", "Products", "Add Product")
        sleep(0.5)

        print("\n\033[1;93mPlease enter the details as prompted:\033[0m\n")
        sleep(0.5)

        # ---------------- Product Name ---------------- #

        product_name = get_product_name(connection)

        if product_name is None:
            continue

        # ---------------- Buying Price ---------------- #

        buying_price = get_buying_price()

        if buying_price is None:
            continue

        # ---------------- Selling Price ---------------- #

        selling_price = get_selling_price(
            buying_price
        )

        if selling_price is None:
            continue

                # ---------------- Category ---------------- #

        print("\n\033[1;93mAvailable Categories:\033[0m\n")
        sleep(0.5)

        view_category(connection)

        print()

        while True:

            try:

                category_id = int(input("\033[1;93mCATEGORY ID: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            except Exception as e:

                print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            cursor = connection.cursor(buffered=True)

            try:

                cursor.execute(
                    "SELECT category_name FROM Categories WHERE category_id = %s",
                    (category_id,)
                )

                category = cursor.fetchone()

                if not category:

                    print("\033[1;91m✕ Category does not exist\033[0m")
                    sleep(1)
                    continue

            except Exception as e:

                print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            finally:

                cursor.close()

            break


        # ---------------- Supplier ---------------- #

        print("\n\033[1;93mAvailable Suppliers:\033[0m\n")
        sleep(0.5)

        view_suppliers(connection)

        print()

        while True:

            try:

                supplier_id = int(input("\033[1;93mSUPPLIER ID: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            except Exception as e:

                print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            cursor = connection.cursor(buffered=True)

            try:

                cursor.execute(
                    "SELECT supplier_name FROM Suppliers WHERE supplier_id = %s",
                    (supplier_id,)
                )

                supplier = cursor.fetchone()

                if not supplier:

                    print("\033[1;91m✕ Supplier does not exist\033[0m")
                    sleep(1)
                    continue

            except Exception as e:

                print(f"\033[1;91mFailed to continue with adding the product\n\033[1;93mReason: {e}\033[0m")
                sleep(0.5)
                print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                sleep(1)
                connection.rollback()
                return

            finally:

                cursor.close()

            break

                # ---------------- Quantity ---------------- #

        quantity = get_quantity()

        if quantity is None:
            continue

        # ---------------- Reorder Level ---------------- #

        reorder_level = get_reorder_level()

        if reorder_level is None:
            continue

        # ---------------- Product Description ---------------- #

        description = get_product_description()

        if description is None:
            continue

        sleep(0.5)

        category_name = category[0]
        supplier_name = supplier[0]

        review_new_product(
            product_name,
            category_name,
            supplier_name,
            buying_price,
            selling_price,
            quantity,
            reorder_level,
            description
        )

        sleep(0.5)

        if confirm_changes():

            print("\033[1;93mInitializing product...\033[0m")
            sleep(0.5)

            cursor = connection.cursor(buffered=True)

            try:

                cursor.execute(
                    """
                    INSERT INTO Products
                    (
                        product_name,
                        category_id,
                        supplier_id,
                        buying_price,
                        selling_price,
                        quantity,
                        reorder_level,
                        description
                    )
                    VALUES
                    (
                        %s,%s,%s,%s,%s,%s,%s,%s
                    )
                    """,
                    (
                        product_name,
                        category_id,
                        supplier_id,
                        buying_price,
                        selling_price,
                        quantity,
                        reorder_level,
                        description
                    )
                )

                connection.commit()

                print("\033[1;92m✓ Product added successfully\033[0m")
                sleep(1)

                if repeat_operation("add", "product"):
                    continue

                return

            except Exception as e:

                print(
                    f"\033[1;91mFailed to add the product\n"
                    f"\033[1;93mReason: {e}\033[0m"
                )

                sleep(0.5)

                print(
                    "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                )

                sleep(1)

                connection.rollback()

                return

            finally:

                cursor.close()

        else:

            print("\033[1;97mCancelling...\033[0m")
            sleep(1)

            if repeat_operation("add", "product"):
                continue

            return

def view_products(connection):

    while True:

        clear()
        title("VIEW PRODUCTS")
        sleep(0.1)
        breadcrumb("Home", "Products", "View Products")
        sleep(0.5)

        print(
        "\n\033[1;93mSort By:\n"
        "\033[1;97m"
        "[1] Product ID (Ascending)\n"
        "[2] Product ID (Descending)\n"
        "[3] Product Name (A-Z)\n"
        "[4] Product Name (Z-A)\n"
        "[5] Buying Price (Low to High)\n"
        "[6] Buying Price (High to Low)\n"
        "[7] Selling Price (Low to High)\n"
        "[8] Selling Price (High to Low)\n"
        "[9] Quantity (Low to High)\n"
        "[10] Quantity (High to Low)\n\n"
        "[0] Back\033[0m"
        )

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
                order_by = "p.product_id ASC"
                break

            elif choice == 2:
                order_by = "p.product_id DESC"
                break

            elif choice == 3:
                order_by = "p.product_name ASC"
                break

            elif choice == 4:
                order_by = "p.product_name DESC"
                break

            elif choice == 5:
                order_by = "p.buying_price ASC"
                break

            elif choice == 6:
                order_by = "p.buying_price DESC"
                break

            elif choice == 7:
                order_by = "p.selling_price ASC"
                break

            elif choice == 8:
                order_by = "p.selling_price DESC"
                break

            elif choice == 9:
                order_by = "p.quantity ASC"
                break

            elif choice == 10:
                order_by = "p.quantity DESC"
                break

            else:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                f"""
                SELECT
                    p.product_id,
                    p.product_name,
                    c.category_name,
                    s.supplier_name,
                    p.buying_price,
                    p.selling_price,
                    p.quantity,
                    p.reorder_level,
                    p.description
                FROM Products p
                LEFT JOIN Categories c
                    ON p.category_id = c.category_id
                LEFT JOIN Suppliers s
                    ON p.supplier_id = s.supplier_id
                ORDER BY {order_by};
                """
            )

            products = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the products\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        if not products:

            print("\n\033[1;91m❌ No products found.\033[0m")
            sleep(1)
            input("\n\033[1;97mPress Enter to continue...\033[0m")
            return

        clear()
        title("VIEW PRODUCTS")
        breadcrumb("Home", "Products", "View Products")

        print()

        for product in products:

            print_product(*product, pause=False)

            print()

        input("\n\033[1;97mPress Enter to continue...\033[0m")

        continue

def search_products(connection):

    while True:

        clear()
        title("SEARCH PRODUCTS")
        sleep(0.1)
        breadcrumb("Home", "Products", "Search Products")
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Type:\n"
            "\033[1;97m"
            "[1] Search by ID\n"
            "[2] Search by Name\n\n"
            "[0] Back\033[0m"
        )

        while True:

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:
                return

            # ---------------- Search By ID ---------------- #

            elif choice == 1:

                print("\n\033[1;93mPlease enter the Product ID below....\n")
                sleep(0.5)

                while True:

                    try:

                        product_id = int(input("\033[1;93mPRODUCT ID: \033[0m"))

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if product_id <= 0:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            Products.product_id,
                            Products.product_name,
                            Categories.category_name,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE Products.product_id = %s
                        """,
                        (product_id,)
                    )

                    product = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the product\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not product:

                    print("\033[1;91m✕ No Product Found\033[0m\n")
                    sleep(1)

                    if repeat_operation("search", "product", "Search Products"):
                        break

                    return

                print_product(*product)

                if repeat_operation("search", "product", "Search Products"):
                    break

                continue
            
            # ---------------- Search By Name ---------------- #

            elif choice == 2:

                print("\n\033[1;93mPlease enter the Product Name below....\n")
                sleep(0.5)

                while True:

                    try:

                        product_name = input("\033[1;93mPRODUCT NAME: \033[0m").strip()

                    except Exception as e:

                        print(
                            f"\033[1;91mFailed to continue with searching the product\n"
                            f"\033[1;93mReason: {e}\033[0m"
                        )

                        sleep(0.5)

                        print(
                            "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                        )

                        sleep(1)

                        connection.rollback()

                        return

                    if not product_name:

                        print("\033[1;91m❌ Product name cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if len(product_name) > 150:

                        print(
                            "\033[1;91m❌ Product name can have a maximum of 150 characters\033[0m\n"
                        )

                        sleep(1)
                        continue

                    if not re.fullmatch(
                        r"[A-Za-z0-9 _.,'()&/+-]+",
                        product_name
                    ):

                        print(
                            "\033[1;91m❌ Product name contains invalid characters\033[0m\n"
                        )

                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            Products.product_id,
                            Products.product_name,
                            Categories.category_name,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE LOWER(Products.product_name)=LOWER(%s)
                        """,
                        (product_name,)
                    )

                    product = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the product\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not product:

                    print("\033[1;91m✕ No Product Found\033[0m\n")

                    sleep(1)

                    if repeat_operation(
                        "search",
                        "product",
                        "Search Products"
                    ):
                        break

                    return

                print_product(*product)

                if repeat_operation(
                    "search",
                    "product",
                    "Search Products"
                ):
                    break

                continue

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

def delete_product(connection):

    while True:

        clear()
        title("DELETE PRODUCT")
        sleep(0.1)
        breadcrumb("Home", "Products", "Delete Product")
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Product:\033[0m\n"
            "\033[1;97m"
            "[1] Search by ID\n"
            "[2] Search by Name\n\n"
            "[0] Back\033[0m"
        )

        while True:

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:
                return

            # ---------------- Search By ID ---------------- #

            elif choice == 1:

                print("\n\033[1;93mPlease enter the Product ID below....\n")
                sleep(0.5)

                while True:

                    try:
                        product_id = int(input("\033[1;93mPRODUCT ID: \033[0m"))

                    except ValueError:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if product_id <= 0:
                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            Products.product_id,
                            Products.product_name,
                            Categories.category_name,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE Products.product_id = %s
                        """,
                        (product_id,)
                    )

                    product = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the product\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not product:

                    print("\033[1;91m✕ No Product Found\033[0m\n")
                    sleep(1)

                    if repeat_operation("search", "product", "Delete Product"):
                        break

                    continue

                print_product(*product)

                sleep(0.5)

                break

            # ---------------- Search By Name ---------------- #

            elif choice == 2:

                print("\n\033[1;93mPlease enter the Product Name below....\n")
                sleep(0.5)

                while True:

                    try:

                        product_name = input("\033[1;93mPRODUCT NAME: \033[0m").strip()

                    except Exception as e:

                        print(
                            f"\033[1;91mFailed to continue with searching the product\n"
                            f"\033[1;93mReason: {e}\033[0m"
                        )

                        sleep(0.5)

                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                        sleep(1)

                        connection.rollback()

                        return

                    if not product_name:

                        print("\033[1;91m❌ Product name cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if len(product_name) > 150:

                        print("\033[1;91m❌ Product name can have a maximum of 150 characters\033[0m\n")
                        sleep(1)
                        continue

                    if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", product_name):

                        print("\033[1;91m❌ Product name contains invalid characters\033[0m\n")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            Products.product_id,
                            Products.product_name,
                            Categories.category_name,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE LOWER(Products.product_name)=LOWER(%s)
                        """,
                        (product_name,)
                    )

                    product = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the product\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not product:

                    print("\033[1;91m✕ No Product Found\033[0m\n")
                    sleep(1)

                    if repeat_operation("search", "product", "Delete Product"):
                        break

                    continue

                print_product(*product)

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
        
        sleep(0.5)

        while True:

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 2:

                print("\033[1;97mCancelling...\033[0m")
                sleep(1)

                if repeat_operation(
                    "delete",
                    "product",
                    "Delete Product"
                ):
                    break

                return

            elif choice == 1:

                print("\033[1;93mDeleting product...\033[0m")
                sleep(0.5)

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        DELETE FROM Products
                        WHERE product_id = %s
                        """,
                        (product[0],)
                    )

                    connection.commit()

                    print("\033[1;92m✓ Product deleted successfully\033[0m")
                    sleep(1)

                    if repeat_operation(
                        "delete",
                        "product",
                        "Delete Product"
                    ):
                        break

                    return

                except mysql.connector.IntegrityError:

                    connection.rollback()

                    print(
                        "\033[1;91m❌ This product cannot be deleted because it is linked to purchases or sales.\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease remove or update those records before trying again.\033[0m\n"
                    )

                    sleep(1)

                    if repeat_operation(
                        "delete",
                        "product",
                        "Delete Product"
                    ):
                        break

                    continue

                except Exception as e:

                    connection.rollback()

                    print(
                        f"\033[1;91mFailed to delete the product\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    return

                finally:

                    cursor.close()

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)

        continue

def update_product(connection):

    while True:

        clear()
        title("UPDATE PRODUCT")
        sleep(0.1)
        breadcrumb("Home", "Products", "Update Product")
        sleep(0.5)

        while True:

            print(
            "\n\033[1;93mSearch Product:\033[0m\n"
            "\033[1;97m"
            "[1] Search by ID\n"
            "[2] Search by Name\n\n"
            "[0] Back\033[0m"
        )

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:
                return

            # ---------------- Search By ID ---------------- #

            elif choice == 1:

                print("\n\033[1;93mPlease enter the Product ID below....\n")
                sleep(0.5)

                while True:

                    try:
                        product_id = int(input("\033[1;93mPRODUCT ID: \033[0m"))

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if product_id <= 0:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            Products.product_id,
                            Products.product_name,
                            Products.category_id,
                            Categories.category_name,
                            Products.supplier_id,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE Products.product_id = %s
                        """,
                        (product_id,)
                    )

                    product = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the product\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not product:

                    print("\033[1;91m✕ No Product Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "product",
                        "Update Product"
                    ):
                        break

                    continue

                (
                    product_id,
                    product_name,
                    category_id,
                    category_name,
                    supplier_id,
                    supplier_name,
                    buying_price,
                    selling_price,
                    quantity,
                    reorder_level,
                    description
                ) = product

                print_product(
                    product_id,
                    product_name,
                    category_name,
                    supplier_name,
                    buying_price,
                    selling_price,
                    quantity,
                    reorder_level,
                    description
                )

                break

            # ---------------- Search By Name ---------------- #

            elif choice == 2:

                print("\n\033[1;93mPlease enter the Product Name below....\n")
                sleep(0.5)

                while True:

                    try:
                        search_name = input("\033[1;93mPRODUCT NAME: \033[0m").strip()

                    except Exception as e:

                        print(
                            f"\033[1;91mFailed to continue with searching the product\n"
                            f"\033[1;93mReason: {e}\033[0m"
                        )

                        sleep(0.5)

                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                        sleep(1)

                        connection.rollback()

                        return

                    if not search_name:

                        print("\033[1;91m❌ Product name cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if len(search_name) > 150:

                        print("\033[1;91m❌ Product name can have a maximum of 150 characters\033[0m\n")
                        sleep(1)
                        continue

                    if not re.fullmatch(r"[A-Za-z0-9 _.,'()&/+-]+", search_name):

                        print("\033[1;91m❌ Product name contains invalid characters\033[0m\n")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            Products.product_id,
                            Products.product_name,
                            Products.category_id,
                            Categories.category_name,
                            Products.supplier_id,
                            Suppliers.supplier_name,
                            Products.buying_price,
                            Products.selling_price,
                            Products.quantity,
                            Products.reorder_level,
                            Products.description
                        FROM Products
                        LEFT JOIN Categories
                            ON Products.category_id = Categories.category_id
                        LEFT JOIN Suppliers
                            ON Products.supplier_id = Suppliers.supplier_id
                        WHERE LOWER(Products.product_name)=LOWER(%s)
                        """,
                        (search_name,)
                    )

                    product = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the product\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print("\033[1;93mPlease fix this issue before trying again\033[0m\n")

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not product:

                    print("\033[1;91m✕ No Product Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "product",
                        "Update Product"
                    ):
                        break

                    continue

                (
                    product_id,
                    product_name,
                    category_id,
                    category_name,
                    supplier_id,
                    supplier_name,
                    buying_price,
                    selling_price,
                    quantity,
                    reorder_level,
                    description
                ) = product

                print_product(
                    product_id,
                    product_name,
                    category_name,
                    supplier_name,
                    buying_price,
                    selling_price,
                    quantity,
                    reorder_level,
                    description
                )

                break

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

        print(
            "\n\033[1;93mUpdate Options:\n"
            "\033[1;97m"
            "[1] Product Name\n"
            "[2] Category\n"
            "[3] Supplier\n"
            "[4] Buying Price\n"
            "[5] Selling Price\n"
            "[6] Quantity\n"
            "[7] Reorder Level\n"
            "[8] Description\n"
            "[9] Update All\n\n"
            "[0] Cancel\033[0m"
        )

        while True:

            try:

                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:

                print("\033[1;97mCancelling...\033[0m")
                sleep(1)

                if repeat_operation(
                    "update",
                    "product",
                    "Products Menu"
                ):
                    break

                continue

            # ---------------- Product Name ---------------- #

            elif choice == 1:

                new_product_name = get_product_name(
                    connection,
                    product_name
                )

                if new_product_name is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Category ---------------- #

            elif choice == 2:

                print("\n\033[1;93mAvailable Categories:\033[0m\n")
                sleep(0.5)

                view_category(connection)

                print()

                while True:

                    try:

                        new_category_id = int(
                            input("\033[1;93mCATEGORY ID: \033[0m")
                        )

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    cursor = connection.cursor(buffered=True)

                    try:

                        cursor.execute(
                            """
                            SELECT category_name
                            FROM Categories
                            WHERE category_id = %s
                            """,
                            (new_category_id,)
                        )

                        category = cursor.fetchone()

                    finally:

                        cursor.close()

                    if not category:

                        print("\033[1;91m✕ Category does not exist\033[0m")
                        sleep(1)
                        continue

                    new_category_name = category[0]

                    break

                break

            # ---------------- Supplier ---------------- #

            elif choice == 3:

                print("\n\033[1;93mAvailable Suppliers:\033[0m\n")
                sleep(0.5)

                view_suppliers(connection)

                print()

                while True:

                    try:

                        new_supplier_id = int(
                            input("\033[1;93mSUPPLIER ID: \033[0m")
                        )

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    cursor = connection.cursor(buffered=True)

                    try:

                        cursor.execute(
                            """
                            SELECT supplier_name
                            FROM Suppliers
                            WHERE supplier_id = %s
                            """,
                            (new_supplier_id,)
                        )

                        supplier = cursor.fetchone()

                    finally:

                        cursor.close()

                    if not supplier:

                        print("\033[1;91m✕ Supplier does not exist\033[0m")
                        sleep(1)
                        continue

                    new_supplier_name = supplier[0]

                    break

                break

            
            # ---------------- Buying Price ---------------- #

            elif choice == 4:

                new_buying_price = get_buying_price(
                    buying_price
                )

                if new_buying_price is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Selling Price ---------------- #

            elif choice == 5:

                new_selling_price = get_selling_price(
                    new_buying_price,
                    selling_price
                )

                if new_selling_price is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Quantity ---------------- #

            elif choice == 6:

                new_quantity = get_quantity(
                    quantity
                )

                if new_quantity is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Reorder Level ---------------- #

            elif choice == 7:

                new_reorder_level = get_reorder_level(
                    reorder_level
                )

                if new_reorder_level is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Description ---------------- #

            elif choice == 8:

                new_description = get_product_description(
                    description
                )

                if new_description is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Update All ---------------- #

            elif choice == 9:

                new_product_name = get_product_name(
                    connection,
                    product_name
                )

                print()

                print("\n\033[1;93mAvailable Categories:\033[0m\n")
                sleep(0.5)

                view_category(connection)

                while True:

                    try:

                        new_category_id = int(
                            input("\033[1;93mCATEGORY ID: \033[0m")
                        )

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    cursor = connection.cursor(buffered=True)

                    try:

                        cursor.execute(
                            """
                            SELECT category_name
                            FROM Categories
                            WHERE category_id=%s
                            """,
                            (new_category_id,)
                        )

                        category = cursor.fetchone()

                    finally:

                        cursor.close()

                    if category:

                        new_category_name = category[0]
                        break

                    print("\033[1;91m✕ Category does not exist\033[0m")
                    sleep(1)

                print()

                print("\n\033[1;93mAvailable Suppliers:\033[0m\n")
                sleep(0.5)

                view_suppliers(connection)

                while True:

                    try:

                        new_supplier_id = int(
                            input("\033[1;93mSUPPLIER ID: \033[0m")
                        )

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    cursor = connection.cursor(buffered=True)

                    try:

                        cursor.execute(
                            """
                            SELECT supplier_name
                            FROM Suppliers
                            WHERE supplier_id=%s
                            """,
                            (new_supplier_id,)
                        )

                        supplier = cursor.fetchone()

                    finally:

                        cursor.close()

                    if supplier:

                        new_supplier_name = supplier[0]
                        break

                    print("\033[1;91m✕ Supplier does not exist\033[0m")
                    sleep(1)

                new_buying_price = get_buying_price(
                    buying_price
                )

                new_selling_price = get_selling_price(
                    new_buying_price,
                    selling_price
                )

                new_quantity = get_quantity(
                    quantity
                )

                new_reorder_level = get_reorder_level(
                    reorder_level
                )

                new_description = get_product_description(
                    description
                )

                break

            else:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue
        
                # ---------------- Review & Save Changes ---------------- #

        if choice == 1:

            review_product_update(
                product_id,
                product_name,
                new_product_name,
                category_name,
                None,
                supplier_name,
                None,
                buying_price,
                None,
                selling_price,
                None,
                quantity,
                None,
                reorder_level,
                None,
                description,
                None
            )

            query = """
            UPDATE Products
            SET product_name = %s
            WHERE product_id = %s
            """

            values = (
                new_product_name,
                product_id
            )


        elif choice == 2:

            review_product_update(
                product_id,
                product_name,
                None,
                category_name,
                new_category_name,
                supplier_name,
                None,
                buying_price,
                None,
                selling_price,
                None,
                quantity,
                None,
                reorder_level,
                None,
                description,
                None
            )

            query = """
            UPDATE Products
            SET category_id = %s
            WHERE product_id = %s
            """

            values = (
                new_category_id,
                product_id
            )


        elif choice == 3:

            review_product_update(
                product_id,
                product_name,
                None,
                category_name,
                None,
                supplier_name,
                new_supplier_name,
                buying_price,
                None,
                selling_price,
                None,
                quantity,
                None,
                reorder_level,
                None,
                description,
                None
            )

            query = """
            UPDATE Products
            SET supplier_id = %s
            WHERE product_id = %s
            """

            values = (
                new_supplier_id,
                product_id
            )


        elif choice == 4:

            review_product_update(
                product_id,
                product_name,
                None,
                category_name,
                None,
                supplier_name,
                None,
                buying_price,
                new_buying_price,
                selling_price,
                None,
                quantity,
                None,
                reorder_level,
                None,
                description,
                None
            )

            query = """
            UPDATE Products
            SET buying_price = %s
            WHERE product_id = %s
            """

            values = (
                new_buying_price,
                product_id
            )


        elif choice == 5:

            review_product_update(
                product_id,
                product_name,
                None,
                category_name,
                None,
                supplier_name,
                None,
                buying_price,
                None,
                selling_price,
                new_selling_price,
                quantity,
                None,
                reorder_level,
                None,
                description,
                None
            )

            query = """
            UPDATE Products
            SET selling_price = %s
            WHERE product_id = %s
            """

            values = (
                new_selling_price,
                product_id
            )


        elif choice == 6:

            review_product_update(
                product_id,
                product_name,
                None,
                category_name,
                None,
                supplier_name,
                None,
                buying_price,
                None,
                selling_price,
                None,
                quantity,
                new_quantity,
                reorder_level,
                None,
                description,
                None
            )

            query = """
            UPDATE Products
            SET quantity = %s
            WHERE product_id = %s
            """

            values = (
                new_quantity,
                product_id
            )


        elif choice == 7:

            review_product_update(
                product_id,
                product_name,
                None,
                category_name,
                None,
                supplier_name,
                None,
                buying_price,
                None,
                selling_price,
                None,
                quantity,
                None,
                reorder_level,
                new_reorder_level,
                description,
                None
            )

            query = """
            UPDATE Products
            SET reorder_level = %s
            WHERE product_id = %s
            """

            values = (
                new_reorder_level,
                product_id
            )


        elif choice == 8:

            review_product_update(
                product_id,
                product_name,
                None,
                category_name,
                None,
                supplier_name,
                None,
                buying_price,
                None,
                selling_price,
                None,
                quantity,
                None,
                reorder_level,
                None,
                description,
                new_description
            )

            query = """
            UPDATE Products
            SET description = %s
            WHERE product_id = %s
            """

            values = (
                new_description,
                product_id
            )


        elif choice == 9:

            review_product_update(
                product_id,
                product_name,
                new_product_name,
                category_name,
                new_category_name,
                supplier_name,
                new_supplier_name,
                buying_price,
                new_buying_price,
                selling_price,
                new_selling_price,
                quantity,
                new_quantity,
                reorder_level,
                new_reorder_level,
                description,
                new_description
            )

            query = """
            UPDATE Products
            SET
                product_name = %s,
                category_id = %s,
                supplier_id = %s,
                buying_price = %s,
                selling_price = %s,
                quantity = %s,
                reorder_level = %s,
                description = %s
            WHERE product_id = %s
            """

            values = (
                new_product_name,
                new_category_id,
                new_supplier_id,
                new_buying_price,
                new_selling_price,
                new_quantity,
                new_reorder_level,
                new_description,
                product_id
            )


        if not confirm_changes():

            print("\033[1;97mCancelling...\033[0m")
            sleep(1)

            if repeat_operation("update", "product", "Products Menu"):
                continue

            continue


        if execute_update(connection, query, values):

            if repeat_operation("update", "product", "Products Menu"):
                continue

            continue
        

def get_first_name(current_first_name=None):

    while True:

        try:

            first_name = input("\033[1;93mFIRST NAME: \033[0m").strip()

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            return None

        if not first_name:

            print("\033[1;91m❌ First name cannot be empty\033[0m")
            sleep(1)
            continue

        if len(first_name) > 50:

            print("\033[1;91m❌ First name can have a maximum of 50 characters\033[0m")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z .'-]+", first_name):

            print("\033[1;91m❌ First name contains invalid characters\033[0m")
            sleep(1)
            continue

        if current_first_name is not None:

            if first_name.lower() == current_first_name.lower():

                print("\033[1;91mNo changes were made.\033[0m")
                sleep(1)
                return None

        return first_name
def get_last_name(current_last_name=None):

    print(
        "\033[1;93mPlease enter the last name: "
        "<Press Enter to leave it blank>\033[0m\n"
    )

    sleep(0.5)

    while True:

        try:

            last_name = input("\033[1;93mLAST NAME: \033[0m").strip()

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            return None

        if not last_name:
            return ""

        if len(last_name) > 50:

            print("\033[1;91m❌ Last name can have a maximum of 50 characters\033[0m")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z .'-]+", last_name):

            print("\033[1;91m❌ Last name contains invalid characters\033[0m")
            sleep(1)
            continue

        if current_last_name is not None:

            if last_name.lower() == current_last_name.lower():

                print("\033[1;91mNo changes were made.\033[0m")
                sleep(1)
                return None

        return last_name

def review_new_customer(
    first_name,
    last_name,
    phone_number,
    customer_email,
    address
):

    clear()
    title("REVIEW CUSTOMER")
    sleep(0.1)
    breadcrumb("Home", "Customers", "Add Customer", "Review")
    sleep(0.5)

    print("\n\033[1;93mPlease review the customer details below:\033[0m\n")

    print("\033[1;97mFirst Name:\033[0m")
    print(f"  {first_name}\n")

    print("\033[1;97mLast Name:\033[0m")
    if last_name:
        print(f"  {last_name}\n")
    else:
        print("  Not Provided\n")

    print("\033[1;97mPhone Number:\033[0m")
    print(f"  {phone_number}\n")

    print("\033[1;97mEmail:\033[0m")
    if customer_email:
        print(f"  {customer_email}\n")
    else:
        print("  Not Provided\n")

    print("\033[1;97mAddress:\033[0m")
    if address:
        print(f"  {address}\n")
    else:
        print("  Not Provided\n")

def print_customer(
    customer_id,
    first_name,
    last_name,
    phone_number,
    customer_email,
    address,
    pause=True
):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
    print(f"\033[1;97m│ Customer ID : \033[1;93m{customer_id:<43}\033[1;97m│\033[0m")
    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print(f"\033[1;97mFirst Name   : \033[1;93m{first_name}\033[0m")

    print(
        f"\033[1;97mLast Name    : "
        f"\033[1;93m{last_name if last_name else 'Not Provided'}\033[0m"
    )

    print(f"\033[1;97mPhone Number : \033[1;93m{phone_number}\033[0m")

    print(
        f"\033[1;97mEmail        : "
        f"\033[1;93m{customer_email if customer_email else 'Not Provided'}\033[0m"
    )

    print(
        f"\033[1;97mAddress      : "
        f"\033[1;93m{address if address else 'Not Provided'}\033[0m"
    )

    if pause:
        input("\n\033[1;97mPress Enter to continue...\033[0m")

def review_customer_update(
    customer_id,

    first_name,
    new_first_name,

    last_name,
    new_last_name,

    phone_number,
    new_phone_number,

    customer_email,
    new_customer_email,

    address,
    new_address
):

    clear()
    title("REVIEW CUSTOMER UPDATE")
    sleep(0.1)
    breadcrumb("Home", "Customers", "Update Customer", "Review")
    sleep(0.5)

    print("\n\033[1;93mPlease review the updated customer details below:\033[0m\n")

    print(f"\033[1;97mCustomer ID:\033[0m")
    print(f"  {customer_id}\n")

    # ---------------- First Name ---------------- #

    print("\033[1;97mFirst Name:\033[0m")
    print(f"  Current : {first_name}")

    if new_first_name is not None:
        print(f"  Updated : {new_first_name}")

    print()

    # ---------------- Last Name ---------------- #

    print("\033[1;97mLast Name:\033[0m")
    print(f"  Current : {last_name if last_name else 'Not Provided'}")

    if new_last_name is not None:
        print(
            f"  Updated : "
            f"{new_last_name if new_last_name else 'Not Provided'}"
        )

    print()

    # ---------------- Phone Number ---------------- #

    print("\033[1;97mPhone Number:\033[0m")
    print(f"  Current : {phone_number}")

    if new_phone_number is not None:
        print(f"  Updated : {new_phone_number}")

    print()

    # ---------------- Email ---------------- #

    print("\033[1;97mEmail:\033[0m")
    print(
        f"  Current : "
        f"{customer_email if customer_email else 'Not Provided'}"
    )

    if new_customer_email is not None:
        print(
            f"  Updated : "
            f"{new_customer_email if new_customer_email else 'Not Provided'}"
        )

    print()

    # ---------------- Address ---------------- #

    print("\033[1;97mAddress:\033[0m")
    print(
        f"  Current : "
        f"{address if address else 'Not Provided'}"
    )

    if new_address is not None:
        print(
            f"  Updated : "
            f"{new_address if new_address else 'Not Provided'}"
        )

    print()

def add_customer(connection):

    while True:

        clear()
        title("ADD CUSTOMER")
        sleep(0.1)
        breadcrumb("Home", "Customers", "Add Customer")
        sleep(0.5)

        print("\n\033[1;93mPlease enter the details as prompted:\033[0m\n")
        sleep(0.5)

        # ---------------- First Name ---------------- #

        first_name = get_first_name()

        if first_name is None:
            continue

        # ---------------- Last Name ---------------- #

        last_name = get_last_name()

        if last_name is None:
            continue

        # ---------------- Phone Number ---------------- #

        phone_number = get_phone(
            connection,
            "Customers",
            None
        )

        if phone_number is None:
            continue

        # ---------------- Email ---------------- #

        customer_email = get_email(
            connection,
            None,
            "Customers",
            50
        )

        if customer_email is None:
            continue

        # ---------------- Address ---------------- #

        address = get_address(150)

        if address is None:
            continue

        sleep(0.5)

        review_new_customer(
            first_name,
            last_name,
            phone_number,
            customer_email,
            address
        )

        sleep(0.5)

        if confirm_changes():

            print("\033[1;93mInitializing customer...\033[0m")
            sleep(0.5)

            cursor = connection.cursor(buffered=True)

            try:

                cursor.execute(
                    """
                    INSERT INTO Customers
                    (
                        first_name,
                        last_name,
                        phone_number,
                        email,
                        address
                    )
                    VALUES
                    (
                        %s,%s,%s,%s,%s
                    )
                    """,
                    (
                        first_name,
                        last_name,
                        phone_number,
                        customer_email,
                        address
                    )
                )

                connection.commit()

                print("\033[1;92m✓ Customer added successfully\033[0m")
                sleep(1)

                if repeat_operation("add", "customer"):
                    continue

                continue

            except Exception as e:

                print(
                    f"\033[1;91mFailed to add the customer\n"
                    f"\033[1;93mReason: {e}\033[0m"
                )

                sleep(0.5)

                print(
                    "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                )

                sleep(1)

                connection.rollback()

                return

            finally:

                cursor.close()

        else:

            print("\033[1;97mCancelling...\033[0m")
            sleep(1)

            if repeat_operation("add", "customer"):
                continue

            continue

def view_customers(connection):

    while True:

        clear()
        title("VIEW CUSTOMERS")
        sleep(0.1)
        breadcrumb("Home", "Customers", "View Customers")
        sleep(0.5)

        print(
            "\n\033[1;93mSort By:\n"
            "\033[1;97m"
            "[1] Customer ID (Ascending)\n"
            "[2] Customer ID (Descending)\n"
            "[3] First Name (A-Z)\n"
            "[4] First Name (Z-A)\n"
            "[5] Last Name (A-Z)\n"
            "[6] Last Name (Z-A)\n\n"
            "[0] Back\033[0m"
        )

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
                order_by = "customer_id ASC"
                break

            elif choice == 2:
                order_by = "customer_id DESC"
                break

            elif choice == 3:
                order_by = "first_name ASC"
                break

            elif choice == 4:
                order_by = "first_name DESC"
                break

            elif choice == 5:
                order_by = "last_name ASC"
                break

            elif choice == 6:
                order_by = "last_name DESC"
                break

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                f"""
                SELECT
                    customer_id,
                    first_name,
                    last_name,
                    phone_number,
                    email,
                    address
                FROM Customers
                ORDER BY {order_by};
                """
            )

            customers = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the customers\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        if not customers:

            print("\n\033[1;91m❌ No customers found.\033[0m")
            sleep(1)
            input("\n\033[1;97mPress Enter to continue...\033[0m")
            return

        clear()
        title("VIEW CUSTOMERS")
        breadcrumb("Home", "Customers", "View Customers")

        print()

        for customer in customers:

            (
                customer_id,
                first_name,
                last_name,
                phone_number,
                customer_email,
                address
            ) = customer

            print_customer(
                customer_id,
                first_name,
                last_name,
                phone_number,
                customer_email,
                address,
                pause=False
            )

            print()

        input("\n\033[1;97mPress Enter to continue...\033[0m")

        return

def search_customers(connection):

    while True:

        clear()
        title("SEARCH CUSTOMERS")
        sleep(0.1)
        breadcrumb("Home", "Customers", "Search Customers")
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Type:\n"
            "\033[1;97m"
            "[1] Search by ID\n"
            "[2] Search by First Name\n\n"
            "[0] Back\033[0m"
        )

        while True:

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:
                return

            # ---------------- Search By ID ---------------- #

            elif choice == 1:

                print("\n\033[1;93mPlease enter the Customer ID below....\n")
                sleep(0.5)

                while True:

                    try:

                        customer_id = int(input("\033[1;93mCUSTOMER ID: \033[0m"))

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if customer_id <= 0:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            customer_id,
                            first_name,
                            last_name,
                            phone_number,
                            email,
                            address
                        FROM Customers
                        WHERE customer_id = %s
                        """,
                        (customer_id,)
                    )

                    customer = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the customer\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not customer:

                    print("\033[1;91m✕ No Customer Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "customer",
                        "Search Customers"
                    ):
                        break

                    continue

                print_customer(*customer)

                if repeat_operation(
                    "search",
                    "customer",
                    "Search Customers"
                ):
                    break

                continue

                        # ---------------- Search By First Name ---------------- #

            # ---------------- Search By First Name ---------------- #
            elif choice == 2:

                print("\n\033[1;93mPlease enter the Customer First Name below....\n")
                sleep(0.5)

                first_name = get_first_name()

                if first_name is None:
                    continue

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            customer_id,
                            first_name,
                            last_name,
                            phone_number,
                            email,
                            address
                        FROM Customers
                        WHERE LOWER(first_name) = LOWER(%s)
                        """,
                        (first_name,)
                    )

                    customer = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the customer\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not customer:

                    print("\033[1;91m✕ No Customer Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "customer",
                        "Search Customers"
                    ):
                        break

                    continue

                print_customer(*customer)

                if repeat_operation(
                    "search",
                    "customer",
                    "Search Customers"
                ):
                    break

                continue

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

def delete_customer(connection):

    while True:

        clear()
        title("DELETE CUSTOMER")
        sleep(0.1)
        breadcrumb("Home", "Customers", "Delete Customer")
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Customer:\033[0m\n"
            "\033[1;97m"
            "[1] Search by ID\n"
            "[2] Search by First Name\n\n"
            "[0] Back\033[0m"
        )

        while True:

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:
                return

            # ---------------- Search By ID ---------------- #

            elif choice == 1:

                print("\n\033[1;93mPlease enter the Customer ID below....\n")
                sleep(0.5)

                while True:

                    try:

                        customer_id = int(input("\033[1;93mCUSTOMER ID: \033[0m"))

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if customer_id <= 0:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            customer_id,
                            first_name,
                            last_name,
                            phone_number,
                            email,
                            address
                        FROM Customers
                        WHERE customer_id = %s
                        """,
                        (customer_id,)
                    )

                    customer = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the customer\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not customer:

                    print("\033[1;91m✕ No Customer Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "customer",
                        "Delete Customer"
                    ):
                        break

                    continue

                print_customer(*customer)

                sleep(0.5)

                break

            # ---------------- Search By First Name ---------------- #

            elif choice == 2:

                print("\n\033[1;93mPlease enter the Customer First Name below....\n")
                sleep(0.5)

                first_name = get_first_name()

                if first_name is None:
                    continue

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            customer_id,
                            first_name,
                            last_name,
                            phone_number,
                            email,
                            address
                        FROM Customers
                        WHERE LOWER(first_name) = LOWER(%s)
                        """,
                        (first_name,)
                    )

                    customer = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the customer\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not customer:

                    print("\033[1;91m✕ No Customer Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "customer",
                        "Delete Customer"
                    ):
                        break

                    continue

                print_customer(*customer)

                sleep(0.5)

                break

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue
        
        
        (
            customer_id,
            first_name,
            last_name,
            phone_number,
            customer_email,
            address
        ) = customer

        sleep(0.5)
        print("\033[1;93m┌───────────────────────────────────┐\033[0m") 
        print("\033[1;93m│           \033[1;91mARE YOU SURE?          \033[1;93m │\033[0m")
        print("\033[1;93m├───────────────────────────────────┤\033[0m")
        print("\033[1;93m│  \033[1;93m⚠️  THIS ACTION CANNOT BE UNDONE \033[1;93m │\033[0m")
        print("\033[1;93m├─────────────────┬─────────────────┤\033[0m")
        print(f"\033[1;93m│ \033[1;97m{"   [1] \033[1;92mYES     ":<10} \033[1;93m│ \033[1;97m{"    [2] \033[1;91mNO ":<22} \033[1;93m│")
        print("\033[1;93m└─────────────────┴─────────────────┘\033[0m")


        sleep(0.5)

        while True:

            try:

                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 2:

                print("\033[1;97mCancelling...\033[0m")
                sleep(1)

                if repeat_operation(
                    "delete",
                    "customer",
                    "Delete Customer"
                ):
                    break

                continue

            elif choice == 1:

                print("\033[1;93mDeleting customer...\033[0m")
                sleep(0.5)

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        DELETE FROM Customers
                        WHERE customer_id = %s
                        """,
                        (customer_id,)
                    )

                    connection.commit()

                    print("\033[1;92m✓ Customer deleted successfully\033[0m")
                    sleep(1)

                    if repeat_operation(
                        "delete",
                        "customer",
                        "Delete Customer"
                    ):
                        break

                    continue

                except mysql.connector.IntegrityError:

                    connection.rollback()

                    print(
                        "\033[1;91m❌ This customer cannot be deleted because it is linked to one or more sales.\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease delete or update those sales before trying again.\033[0m\n"
                    )

                    sleep(1)

                    if repeat_operation(
                        "delete",
                        "customer",
                        "Delete Customer"
                    ):
                        break

                    continue

                except Exception as e:

                    connection.rollback()

                    print(
                        f"\033[1;91mFailed to delete the customer\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    return

                finally:

                    cursor.close()

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)

        continue

def update_customer(connection):

    while True:

        clear()
        title("UPDATE CUSTOMER")
        sleep(0.1)
        breadcrumb("Home", "Customers", "Update Customer")
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Customer:\033[0m\n"
            "\033[1;97m"
            "[1] Search by ID\n"
            "[2] Search by First Name\n\n"
            "[0] Back\033[0m"
        )

        while True:

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:
                return

            # ---------------- Search By ID ---------------- #

            elif choice == 1:

                print("\n\033[1;93mPlease enter the Customer ID below....\n")
                sleep(0.5)

                while True:

                    try:

                        customer_id = int(input("\033[1;93mCUSTOMER ID: \033[0m"))

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if customer_id <= 0:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            customer_id,
                            first_name,
                            last_name,
                            phone_number,
                            email,
                            address
                        FROM Customers
                        WHERE customer_id = %s
                        """,
                        (customer_id,)
                    )

                    customer = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the customer\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not customer:

                    print("\033[1;91m✕ No Customer Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "customer",
                        "Update Customer"
                    ):
                        break

                    continue

                (
                    customer_id,
                    first_name,
                    last_name,
                    phone_number,
                    customer_email,
                    address
                ) = customer

                print_customer(
                    customer_id,
                    first_name,
                    last_name,
                    phone_number,
                    customer_email,
                    address
                )

                break

            # ---------------- Search By First Name ---------------- #

            elif choice == 2:

                print("\n\033[1;93mPlease enter the Customer First Name below....\n")
                sleep(0.5)

                search_first_name = get_first_name()

                if search_first_name is None:
                    continue

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            customer_id,
                            first_name,
                            last_name,
                            phone_number,
                            email,
                            address
                        FROM Customers
                        WHERE LOWER(first_name) = LOWER(%s)
                        """,
                        (search_first_name,)
                    )

                    customer = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the customer\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not customer:

                    print("\033[1;91m✕ No Customer Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "customer",
                        "Update Customer"
                    ):
                        break

                    continue

                (
                    customer_id,
                    first_name,
                    last_name,
                    phone_number,
                    customer_email,
                    address
                ) = customer

                print_customer(
                    customer_id,
                    first_name,
                    last_name,
                    phone_number,
                    customer_email,
                    address
                )

                break

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

        print(
        "\n\033[1;93mUpdate Options:\n"
        "\033[1;97m"
        "[1] First Name\n"
        "[2] Last Name\n"
        "[3] Phone Number\n"
        "[4] Email\n"
        "[5] Address\n"
        "[6] Update All\n\n"
        "[0] Cancel\033[0m"
        )

        while True:

            try:

                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:

                print("\033[1;97mCancelling...\033[0m")
                sleep(1)

                if repeat_operation(
                    "update",
                    "customer",
                    "Update Customer"
                ):
                    break

                continue

            # ---------------- First Name ---------------- #

            elif choice == 1:

                new_first_name = get_first_name(
                    first_name
                )

                if new_first_name is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Last Name ---------------- #

            elif choice == 2:

                new_last_name = get_last_name(
                    last_name
                )

                if new_last_name is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Phone Number ---------------- #

            elif choice == 3:

                new_phone_number = get_phone(
                    connection,
                    "Customers",
                    phone_number
                )

                if new_phone_number is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Email ---------------- #

            elif choice == 4:

                new_customer_email = get_email(
                    connection,
                    customer_email,
                    "Customers",
                    50
                )

                if new_customer_email is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Address ---------------- #

            elif choice == 5:

                new_address = get_address(
                    150,
                    address
                )

                if new_address is None:

                    print("\033[1;91mNo changes were made.\033[0m")
                    sleep(1)
                    continue

                break

            # ---------------- Update All ---------------- #

            elif choice == 6:

                new_first_name = get_first_name(
                    first_name
                )

                new_last_name = get_last_name(
                    last_name
                )

                new_phone_number = get_phone(
                    connection,
                    "Customers",
                    phone_number
                )

                new_customer_email = get_email(
                    connection,
                    customer_email,
                    "Customers",
                    50
                )

                new_address = get_address(
                    150,
                    address
                )

                break

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

     # ---------------- Review & Save Changes ---------------- #

        if choice == 1:

            review_customer_update(
                customer_id,
                first_name,
                new_first_name,
                last_name,
                None,
                phone_number,
                None,
                customer_email,
                None,
                address,
                None
            )

            query = """
            UPDATE Customers
            SET first_name = %s
            WHERE customer_id = %s
            """

            values = (
                new_first_name,
                customer_id
            )


        elif choice == 2:

            review_customer_update(
                customer_id,
                first_name,
                None,
                last_name,
                new_last_name,
                phone_number,
                None,
                customer_email,
                None,
                address,
                None
            )

            query = """
            UPDATE Customers
            SET last_name = %s
            WHERE customer_id = %s
            """

            values = (
                new_last_name,
                customer_id
            )


        elif choice == 3:

            review_customer_update(
                customer_id,
                first_name,
                None,
                last_name,
                None,
                phone_number,
                new_phone_number,
                customer_email,
                None,
                address,
                None
            )

            query = """
            UPDATE Customers
            SET phone_number = %s
            WHERE customer_id = %s
            """

            values = (
                new_phone_number,
                customer_id
            )


        elif choice == 4:

            review_customer_update(
                customer_id,
                first_name,
                None,
                last_name,
                None,
                phone_number,
                None,
                customer_email,
                new_customer_email,
                address,
                None
            )

            query = """
            UPDATE Customers
            SET email = %s
            WHERE customer_id = %s
            """

            values = (
                new_customer_email,
                customer_id
            )


        elif choice == 5:

            review_customer_update(
                customer_id,
                first_name,
                None,
                last_name,
                None,
                phone_number,
                None,
                customer_email,
                None,
                address,
                new_address
            )

            query = """
            UPDATE Customers
            SET address = %s
            WHERE customer_id = %s
            """

            values = (
                new_address,
                customer_id
            )


        elif choice == 6:

            review_customer_update(
                customer_id,
                first_name,
                new_first_name,
                last_name,
                new_last_name,
                phone_number,
                new_phone_number,
                customer_email,
                new_customer_email,
                address,
                new_address
            )

            query = """
            UPDATE Customers
            SET
                first_name = %s,
                last_name = %s,
                phone_number = %s,
                email = %s,
                address = %s
            WHERE customer_id = %s
            """

            values = (
                new_first_name,
                new_last_name,
                new_phone_number,
                new_customer_email,
                new_address,
                customer_id
            )


        if not confirm_changes():

            print("\033[1;97mCancelling...\033[0m")
            sleep(1)

            if repeat_operation(
                "update",
                "customer",
                "Update Customer"
            ):
                continue

            continue


        if execute_update(
            connection,
            query,
            values
        ):

            if repeat_operation(
                "update",
                "customer",
                "Update Customer"
            ):
                continue

            continue


def get_supplier_id(connection):

    print("\n\033[1;93mAvailable Suppliers:\033[0m\n")
    sleep(0.5)

    view_suppliers(connection)

    print()

    while True:

        try:

            supplier_id = int(input("\033[1;93mSUPPLIER ID: \033[0m"))

        except ValueError:

            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return None

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT supplier_name
                FROM Suppliers
                WHERE supplier_id = %s
                """,
                (supplier_id,)
            )

            supplier = cursor.fetchone()

            if not supplier:

                print("\033[1;91m✕ Supplier does not exist\033[0m")
                sleep(1)
                continue

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return None

        finally:

            cursor.close()

        return supplier_id, supplier[0]
def purchase_exists(
    connection,
    purchase_id
):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            """
            SELECT 1
            FROM Purchases
            WHERE purchase_id = %s
            """,
            (purchase_id,)
        )

        return cursor.fetchone() is not None

    finally:

        cursor.close()

def get_purchase(
    connection,
    purchase_id
):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            """
            SELECT
            Purchases.purchase_id,
            Suppliers.supplier_name,
            Users.username,
            Purchases.purchase_date,
            Purchases.total_amount,
            Purchases.status
        FROM Purchases
        LEFT JOIN Suppliers
            ON Purchases.supplier_id = Suppliers.supplier_id
        LEFT JOIN Users
            ON Purchases.user_id = Users.user_id
        WHERE Purchases.purchase_id = %s;
            """,
            (purchase_id,)
        )

        return cursor.fetchone()

    finally:

        cursor.close()

def print_purchase(
    purchase_id,
    supplier_name,
    username,
    purchase_date,
    total_amount,
    status,
    pause=True
):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")
    print(f"\033[1;97m│ Purchase ID : \033[1;93m{purchase_id:<43}\033[1;97m│\033[0m")
    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print(
        f"\033[1;97mSupplier      : "
        f"\033[1;93m{supplier_name}\033[0m"
    )

    print(
        f"\033[1;97mAdded By      : "
        f"\033[1;93m{username}\033[0m"
    )

    print(
        f"\033[1;97mPurchase Date : "
        f"\033[1;93m{purchase_date}\033[0m"
    )

    print(
        f"\033[1;97mTotal Amount  : "
        f"\033[1;93m₹{total_amount:.2f}\033[0m"
    )

    print(
        f"\033[1;97mStatus        : "
        f"\033[1;93m{status}\033[0m"
    )

    if pause:

        input("\n\033[1;97mPress Enter to continue...\033[0m")

def review_new_purchase(
    supplier_name,
    username,
    total_amount
):

    clear()
    title("REVIEW PURCHASE")
    sleep(0.1)
    breadcrumb("Home", "Purchases", "New Purchase", "Review")
    sleep(0.5)

    print("\n\033[1;93mPlease review the purchase details below:\033[0m\n")

    print("\033[1;97mSupplier:\033[0m")
    print(f"  {supplier_name}\n")

    print("\033[1;97mAdded By:\033[0m")
    print(f"  {username}\n")

    print("\033[1;97mTotal Amount:\033[0m")
    print(f"  ₹{total_amount:.2f}\n")

def get_product_id(connection):

    print("\n\033[1;93mAvailable Products:\033[0m\n")
    sleep(0.5)

    view_products(connection, pause=False)

    print()

    while True:

        try:

            product_id = int(input("\033[1;93mPRODUCT ID: \033[0m"))

        except ValueError:

            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return None

        if product_id <= 0:

            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    product_name,quantity
                FROM Products
                WHERE product_id = %s
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if not product:

                print("\033[1;91m✕ Product does not exist\033[0m")
                sleep(1)
                continue

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return None

        finally:

            cursor.close()

        return (
            product_id,
            product[0]
        )

def get_purchase_quantity():

    while True:

        try:

            quantity = int(input("\033[1;93mQUANTITY: \033[0m"))

        except ValueError:

            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            return None

        if quantity <= 0:

            print("\033[1;91m❌ Quantity must be greater than 0\033[0m")
            sleep(1)
            continue

        return quantity

def get_unit_price():

    while True:

        try:

            unit_price = float(input("\033[1;93mUNIT PRICE: ₹\033[0m"))

        except ValueError:

            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            return None

        if unit_price < 0:

            print("\033[1;91m❌ Unit price cannot be negative\033[0m")
            sleep(1)
            continue

        return round(unit_price, 2)

def calculate_subtotal(
    quantity,
    unit_price
):

    subtotal = quantity * unit_price

    return round(subtotal, 2)

def calculate_purchase_total(
    purchase_items
):

    total_amount = 0

    for item in purchase_items:

        total_amount += item["subtotal"]

    return round(total_amount, 2)

def print_purchase_item(
    product_name,
    quantity,
    unit_price,
    subtotal
):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")

    print(
        f"\033[1;97m│ Product : "
        f"\033[1;93m{product_name:<45}"
        f"\033[1;97m│\033[0m"
    )

    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print(
        f"\033[1;97mQuantity    : "
        f"\033[1;93m{quantity}\033[0m"
    )

    print(
        f"\033[1;97mUnit Price  : "
        f"\033[1;93m₹{unit_price:.2f}\033[0m"
    )

    print(
        f"\033[1;97mSubtotal    : "
        f"\033[1;93m₹{subtotal:.2f}\033[0m"
    )

def increase_product_stock(
    connection,
    product_id,
    quantity
):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            """
            UPDATE Products
            SET quantity = quantity + %s
            WHERE product_id = %s
            """,
            (
                quantity,
                product_id
            )
        )

    finally:

        cursor.close()



def add_purchase(connection, user_id):

    while True:

        clear()
        title("NEW PURCHASE")
        sleep(0.1)
        breadcrumb("Home", "Purchases", "New Purchase")
        sleep(0.5)

        print("\n\033[1;93mPlease enter the details as prompted:\033[0m\n")
        sleep(0.5)

        # ---------------- Supplier ---------------- #

        supplier = get_supplier_id(connection)

        if supplier is None:
            continue

        supplier_id, supplier_name = supplier

        purchase_items = []

        # ---------------- Purchase Items ---------------- #

        while True:

            product = get_product_id(connection)

            if product is None:
                continue

            product_id, product_name = product

            quantity = get_purchase_quantity()

            if quantity is None:
                continue

            unit_price = get_unit_price()

            if unit_price is None:
                continue

            subtotal = calculate_subtotal(
                quantity,
                unit_price
            )

            duplicate = False

            for item in purchase_items:

                if item["product_id"] == product_id:

                    print(...)
                    sleep(1)

                    duplicate = True
                    break

            if duplicate:
                continue

            else:
                purchase_items.append(
                    {
                        "product_id": product_id,
                        "product_name": product_name,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "subtotal": subtotal
                    }
                )
            
            print("\n\033[1;93mAdd another product?\033[0m\n")
            print("\033[1;92m[1] ✔ Yes")
            print("[2] ✖ No\033[0m")

            while True:

                try:

                    choice = int(input("\033[1;93mChoice: \033[0m"))

                except ValueError:

                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if choice == 1:
                    break

                elif choice == 2:
                    break

                else:

                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)

            if choice == 2:
                break

        if not purchase_items:

            print("\033[1;91m❌ No products were added to the purchase.\033[0m")
            sleep(1)
            continue

        total_amount = calculate_purchase_total(
            purchase_items
        )

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    username
                FROM Users
                WHERE user_id = %s
                """,
                (user_id,)
            )

            user = cursor.fetchone()

            if not user:

                print("\033[1;91m✕ Current user does not exist\033[0m")
                sleep(1)
                connection.rollback()
                return

            username = user[0]

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue with adding the purchase\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        review_new_purchase(
            supplier_name,
            username,
            purchase_items,
            total_amount
        )

        sleep(0.5)

        if not confirm_changes():

            print("\033[1;97mCancelling...\033[0m")
            sleep(1)

            if repeat_operation(
                "add",
                "purchase",
                "New Purchase"
            ):
                continue

            continue

        print("\033[1;93mInitializing purchase...\033[0m")
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            # ---------------- Insert Purchase ---------------- #

            cursor.execute(
                """
                INSERT INTO Purchases
                (
                    supplier_id,
                    user_id,
                    total_amount
                )
                VALUES
                (
                    %s,%s,%s
                )
                """,
                (
                    supplier_id,
                    user_id,
                    total_amount
                )
            )

            purchase_id = cursor.lastrowid

            # ---------------- Insert Purchase Items ---------------- #

            for item in purchase_items:

                cursor.execute(
                    """
                    INSERT INTO Purchase_Items
                    (
                        purchase_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES
                    (
                        %s,%s,%s,%s,%s
                    )
                    """,
                    (
                        purchase_id,
                        item["product_id"],
                        item["quantity"],
                        item["unit_price"],
                        item["subtotal"]
                    )
                )

                # ---------------- Increase Product Stock ---------------- #

                increase_product_stock(
                    connection,
                    item["product_id"],
                    item["quantity"]
                )

            connection.commit()

            print("\033[1;92m✓ Purchase added successfully\033[0m")
            sleep(1)

            if repeat_operation(
                "add",
                "purchase",
                "New Purchase"
            ):
                continue

            continue
        
        except Exception as e:

            print(
                f"\033[1;91mFailed to add the purchase\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

def purchase_history(connection):

    while True:

        clear()
        title("PURCHASE HISTORY")
        sleep(0.1)
        breadcrumb("Home", "Purchases", "Purchase History")
        sleep(0.5)

        print(
            "\n\033[1;93mSort By:\n"
            "\033[1;97m"
            "[1] Purchase ID (Ascending)\n"
            "[2] Purchase ID (Descending)\n"
            "[3] Purchase Date (Oldest First)\n"
            "[4] Purchase Date (Newest First)\n"
            "[5] Total Amount (Low to High)\n"
            "[6] Total Amount (High to Low)\n\n"
            "[0] Back\033[0m"
        )

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
                order_by = "Purchases.purchase_id ASC"
                break

            elif choice == 2:
                order_by = "Purchases.purchase_id DESC"
                break

            elif choice == 3:
                order_by = "Purchases.purchase_date ASC"
                break

            elif choice == 4:
                order_by = "Purchases.purchase_date DESC"
                break

            elif choice == 5:
                order_by = "Purchases.total_amount ASC"
                break

            elif choice == 6:
                order_by = "Purchases.total_amount DESC"
                break

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                f"""
                SELECT
                    Purchases.purchase_id,
                    Suppliers.supplier_name,
                    Users.username,
                    Purchases.purchase_date,
                    Purchases.total_amount,
                    Purchases.status
                FROM Purchases
                LEFT JOIN Suppliers
                    ON Purchases.supplier_id = Suppliers.supplier_id
                LEFT JOIN Users
                    ON Purchases.user_id = Users.user_id
                ORDER BY {order_by};
                """
            )

            purchases = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the purchase history\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        if not purchases:

            print("\n\033[1;91m❌ No purchases found.\033[0m")
            sleep(1)
            input("\n\033[1;97mPress Enter to continue...\033[0m")
            return

        clear()
        title("PURCHASE HISTORY")
        breadcrumb("Home", "Purchases", "Purchase History")

        print()

        for purchase in purchases:

            print_purchase(
                *purchase,
                pause=False
            )

            print()

        input("\n\033[1;97mPress Enter to continue...\033[0m")

        return

def search_purchase(connection):

    while True:

        clear()
        title("SEARCH PURCHASE")
        sleep(0.1)
        breadcrumb("Home", "Purchases", "Search Purchase")
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Type:\n"
            "\033[1;97m"
            "[1] Search by Purchase ID\n"
            "[2] Search by Supplier Name\n\n"
            "[0] Back\033[0m"
        )

        while True:

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:
                return

            # ---------------- Search By Purchase ID ---------------- #

            elif choice == 1:

                print("\n\033[1;93mPlease enter the Purchase ID below....\n")
                sleep(0.5)

                while True:

                    try:

                        purchase_id = int(input("\033[1;93mPURCHASE ID: \033[0m"))

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if purchase_id <= 0:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                purchase = get_purchase(
                    connection,
                    purchase_id
                )

                if purchase is None:

                    print("\033[1;91m✕ No Purchase Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "purchase",
                        "Search Purchase"
                    ):
                        break

                    continue

                print_purchase(*purchase)

                if repeat_operation(
                    "search",
                    "purchase",
                    "Search Purchase"
                ):
                    break

                continue

            # ---------------- Search By Supplier Name ---------------- #

            elif choice == 2:

                print("\n\033[1;93mPlease enter the Supplier Name below....\n")
                sleep(0.5)

                supplier_name = get_supplier_name(
                    connection,
                    None
                )

                if supplier_name is None:
                    continue

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            Purchases.purchase_id,
                            Suppliers.supplier_name,
                            Users.username,
                            Purchases.purchase_date,
                            Purchases.total_amount,
                            Purchases.status
                        FROM Purchases
                        LEFT JOIN Suppliers
                            ON Purchases.supplier_id = Suppliers.supplier_id
                        LEFT JOIN Users
                            ON Purchases.user_id = Users.user_id
                        WHERE LOWER(Suppliers.supplier_name)=LOWER(%s)
                        """,
                        (supplier_name,)
                    )

                    purchases = cursor.fetchall()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the purchase\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not purchases:

                    print("\033[1;91m✕ No Purchase Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "purchase",
                        "Search Purchase"
                    ):
                        break

                    continue
                
                for purchase in purchases:
                    print_purchase(*purchase, pause = False)
                    print()

                if repeat_operation(
                    "search",
                    "purchase",
                    "Search Purchase"
                ):
                    break

                continue

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)



def decrease_product_stock(
    connection,
    product_id,
    quantity
):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            """
            UPDATE Products
            SET quantity = quantity - %s
            WHERE product_id = %s
            """,
            (
                quantity,
                product_id
            )
        )

    finally:

        cursor.close()

def sale_exists(
    connection,
    sale_id
):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            """
            SELECT 1
            FROM Sales
            WHERE sale_id = %s
            """,
            (sale_id,)
        )

        return cursor.fetchone() is not None

    finally:

        cursor.close()

def get_sale(
    connection,
    sale_id
):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            """
            SELECT
                Sales.sale_id,
                Customers.first_name,
                Customers.last_name,
                Users.username,
                Sales.sale_date,
                Sales.total_amount,
                Sales.status
            FROM Sales
            LEFT JOIN Customers
                ON Sales.customer_id = Customers.customer_id
            LEFT JOIN Users
                ON Sales.user_id = Users.user_id
            WHERE Sales.sale_id = %s
            """,
            (sale_id,)
        )

        return cursor.fetchone()

    finally:

        cursor.close()

def print_sale_item(
    product_name,
    quantity,
    unit_price,
    subtotal
):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")

    print(
        f"\033[1;97m│ Product : "
        f"\033[1;93m{product_name:<45}"
        f"\033[1;97m│\033[0m"
    )

    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print(
        f"\033[1;97mQuantity    : "
        f"\033[1;93m{quantity}\033[0m"
    )

    print(
        f"\033[1;97mUnit Price  : "
        f"\033[1;93m₹{unit_price:.2f}\033[0m"
    )

    print(
        f"\033[1;97mSubtotal    : "
        f"\033[1;93m₹{subtotal:.2f}\033[0m"
    )

def print_sale(
    sale_id,
    first_name,
    last_name,
    username,
    sale_date,
    total_amount,
    status,
    pause=True
):

    print("\033[36m┌────────────────────────────────────────────────────────────┐\033[0m")

    print(
        f"\033[1;97m│ Sale ID : "
        f"\033[1;93m{sale_id:<46}"
        f"\033[1;97m│\033[0m"
    )

    print("\033[36m└────────────────────────────────────────────────────────────┘\033[0m")

    print(
        f"\033[1;97mCustomer     : "
        f"\033[1;93m{first_name} {last_name}\033[0m"
    )

    print(
        f"\033[1;97mSold By      : "
        f"\033[1;93m{username}\033[0m"
    )

    print(
        f"\033[1;97mSale Date    : "
        f"\033[1;93m{sale_date}\033[0m"
    )

    print(
        f"\033[1;97mTotal Amount : "
        f"\033[1;93m₹{total_amount:.2f}\033[0m"
    )

    print(
        f"\033[1;97mStatus       : "
        f"\033[1;93m{status}\033[0m"
    )

    if pause:

        input("\n\033[1;97mPress Enter to continue...\033[0m")

def review_new_sale(
    customer_name,
    username,
    sale_items,
    total_amount
):

    clear()
    title("REVIEW SALE")
    breadcrumb("Home", "Sales", "Review Sale")

    print("\n\033[1;93mPlease review the details below:\033[0m\n")

    print(
        f"\033[1;97mCustomer     : "
        f"\033[1;93m{customer_name}\033[0m"
    )

    print(
        f"\033[1;97mSold By      : "
        f"\033[1;93m{username}\033[0m"
    )

    print("\n\033[1;96mItems:\033[0m\n")

    for item in sale_items:

        print_sale_item(
            item["product_name"],
            item["quantity"],
            item["unit_price"],
            item["subtotal"]
        )

        print()

    print(
        f"\033[1;97mGrand Total : "
        f"\033[1;92m₹{total_amount:.2f}\033[0m\n"
    )

def get_customer_id(connection):

    print("\n\033[1;93mAvailable Customers:\033[0m\n")
    sleep(0.5)

    view_customers(
        connection,
    )

    print()

    while True:

        try:

            customer_id = int(input("\033[1;93mCUSTOMER ID: \033[0m"))

        except ValueError:

            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            return None

        if customer_id <= 0:

            print("\033[1;91mEnter a valid input\033[0m")
            sleep(1)
            continue

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    customer_id,
                    first_name,
                    last_name
                FROM Customers
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            customer = cursor.fetchone()

            if not customer:

                print("\033[1;91m✕ Customer does not exist\033[0m")
                sleep(1)
                continue

            return customer

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            return None

        finally:

            cursor.close()

def get_customer_name(
    connection,
    customer_id
):

    while True:

        try:

            customer_name = input(
                "\033[1;93mCUSTOMER NAME: \033[0m"
            ).strip()

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            return None

        if not customer_name:

            print("\033[1;91m❌ Customer name cannot be empty\033[0m")
            sleep(1)
            continue

        if len(customer_name) > 101:

            print(
                "\033[1;91m❌ Customer name can have a maximum of 101 characters\033[0m"
            )

            sleep(1)
            continue

        if not re.fullmatch(
            r"[A-Za-z ]+",
            customer_name
        ):

            print(
                "\033[1;91m❌ Customer name contains invalid characters\033[0m"
            )

            sleep(1)
            continue

        cursor = connection.cursor(buffered=True)

        try:

            if customer_id is None:

                cursor.execute(
                    """
                    SELECT
                        customer_id
                    FROM Customers
                    WHERE LOWER(
                        CONCAT(
                            first_name,
                            ' ',
                            last_name
                        )
                    ) = LOWER(%s)
                    """,
                    (customer_name,)
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        customer_id
                    FROM Customers
                    WHERE LOWER(
                        CONCAT(
                            first_name,
                            ' ',
                            last_name
                        )
                    ) = LOWER(%s)
                    AND customer_id != %s
                    """,
                    (
                        customer_name,
                        customer_id
                    )
                )

            customer = cursor.fetchone()

            if not customer:

                print("\033[1;91m✕ Customer does not exist\033[0m")
                sleep(1)
                continue

            return customer_name

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            return None

        finally:

            cursor.close()


def add_sale(connection, user_id):

    while True:

        clear()
        title("NEW SALE")
        sleep(0.1)
        breadcrumb("Home", "Sales", "New Sale")
        sleep(0.5)

        print("\n\033[1;93mPlease enter the details as prompted:\033[0m\n")
        sleep(0.5)

        # ---------------- Customer ---------------- #

        customer = get_customer_id(connection)

        if customer is None:
            continue

        customer_id, first_name, last_name = customer

        sale_items = []

        # ---------------- Sale Items ---------------- #

        while True:

            product = get_product_id(connection)

            if product is None:
                continue

            product_id, product_name = product

            cursor = connection.cursor(buffered=True)

            try:

                cursor.execute(
                    """
                    SELECT
                        quantity,
                        selling_price
                    FROM Products
                    WHERE product_id = %s
                    """,
                    (product_id,)
                )

                product_details = cursor.fetchone()

                if not product_details:

                    print("\033[1;91m✕ Product does not exist\033[0m")
                    sleep(1)
                    continue

                available_stock, selling_price = product_details

            except Exception as e:

                print(
                    f"\033[1;91mFailed to continue with adding the sale\n"
                    f"\033[1;93mReason: {e}\033[0m"
                )

                sleep(0.5)

                print(
                    "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                )

                sleep(1)

                connection.rollback()

                return

            finally:

                cursor.close()

            quantity = get_purchase_quantity()

            if quantity is None:
                continue

            if quantity > available_stock:

                print(
                    f"\033[1;91m❌ Only {available_stock} unit(s) available in stock.\033[0m"
                )

                sleep(1)

                continue

            duplicate = False

            for item in sale_items:

                if item["product_id"] == product_id:

                    print(
                        "\033[1;91m❌ This product has already been added to the sale.\033[0m"
                    )

                    sleep(1)

                    duplicate = True
                    break

            if duplicate:
                continue

            subtotal = calculate_subtotal(
                quantity,
                selling_price
            )

            sale_items.append(
                {
                    "product_id": product_id,
                    "product_name": product_name,
                    "quantity": quantity,
                    "unit_price": selling_price,
                    "subtotal": subtotal
                }
            )

            print("\n\033[1;93mAdd another product?\033[0m\n")
            print("\033[1;92m[1] ✔ Yes")
            print("[2] ✖ No\033[0m")

            while True:

                try:

                    choice = int(input("\033[1;93mChoice: \033[0m"))

                except ValueError:

                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)
                    continue

                if choice == 1:
                    break

                elif choice == 2:
                    break

                else:

                    print("\033[1;91mEnter a valid input\033[0m")
                    sleep(1)

            if choice == 2:
                break

        if not sale_items:

            print("\033[1;91m❌ No products were added to the sale.\033[0m")
            sleep(1)
            continue

        total_amount = calculate_purchase_total(sale_items)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    username
                FROM Users
                WHERE user_id = %s
                """,
                (user_id,)
            )

            user = cursor.fetchone()

            if not user:

                print("\033[1;91m✕ Current user does not exist\033[0m")
                sleep(1)
                connection.rollback()
                return

            username = user[0]

        except Exception as e:

            print(
                f"\033[1;91mFailed to continue with adding the sale\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        review_new_sale(
            f"{first_name} {last_name}",
            username,
            sale_items,
            total_amount
        )

        sleep(0.5)

        if not confirm_changes():

            print("\033[1;97mCancelling...\033[0m")
            sleep(1)

            if repeat_operation(
                "add",
                "sale",
                "New Sale"
            ):
                continue

            continue

        print("\033[1;93mInitializing sale...\033[0m")
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            # ---------------- Insert Sale ---------------- #

            cursor.execute(
                """
                INSERT INTO Sales
                (
                    customer_id,
                    user_id,
                    total_amount
                )
                VALUES
                (
                    %s,%s,%s
                )
                """,
                (
                    customer_id,
                    user_id,
                    total_amount
                )
            )

            sale_id = cursor.lastrowid

            # ---------------- Insert Sale Items ---------------- #

            for item in sale_items:

                cursor.execute(
                    """
                    INSERT INTO Sale_Items
                    (
                        sale_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES
                    (
                        %s,%s,%s,%s,%s
                    )
                    """,
                    (
                        sale_id,
                        item["product_id"],
                        item["quantity"],
                        item["unit_price"],
                        item["subtotal"]
                    )
                )

                # ---------------- Decrease Product Stock ---------------- #

                decrease_product_stock(
                    connection,
                    item["product_id"],
                    item["quantity"]
                )

            connection.commit()

            print("\033[1;92m✓ Sale added successfully\033[0m")
            sleep(1)

            if repeat_operation(
                "add",
                "sale",
                "New Sale"
            ):
                continue

            continue

        except Exception as e:

            print(
                f"\033[1;91mFailed to add the sale\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

def search_sale(connection):

    while True:

        clear()
        title("SEARCH SALE")
        sleep(0.1)
        breadcrumb("Home", "Sales", "Search Sale")
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Type:\n"
            "\033[1;97m"
            "[1] Search by Sale ID\n"
            "[2] Search by Customer Name\n\n"
            "[0] Back\033[0m"
        )

        while True:

            try:

                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:
                return

            # ---------------- Search By Sale ID ---------------- #

            elif choice == 1:

                print("\n\033[1;93mPlease enter the Sale ID below....\n")
                sleep(0.5)

                while True:

                    try:

                        sale_id = int(input("\033[1;93mSALE ID: \033[0m"))

                    except ValueError:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    if sale_id <= 0:

                        print("\033[1;91mEnter a valid input\033[0m")
                        sleep(1)
                        continue

                    break

                sale = get_sale(
                    connection,
                    sale_id
                )

                if sale is None:

                    print("\033[1;91m✕ No Sale Found\033[0m\n")
                    sleep(1)

                    if repeat_operation(
                        "search",
                        "sale",
                        "Search Sale"
                    ):
                        break

                    continue

                print_sale(*sale)

                if repeat_operation(
                    "search",
                    "sale",
                    "Search Sale"
                ):
                    break

                continue

                # ---------------- Search By Customer Name ---------------- #

            elif choice == 2:

                print("\n\033[1;93mPlease enter the Customer Name below....\n")
                sleep(0.5)

                customer_name = get_customer_name(
                    connection,
                    None
                )

                if customer_name is None:
                    continue

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            Sales.sale_id,
                            Customers.first_name,
                            Customers.last_name,
                            Users.username,
                            Sales.sale_date,
                            Sales.total_amount,
                            Sales.status
                        FROM Sales
                        LEFT JOIN Customers
                            ON Sales.customer_id = Customers.customer_id
                        LEFT JOIN Users
                            ON Sales.user_id = Users.user_id
                        WHERE LOWER(
                            CONCAT(
                                Customers.first_name,
                                ' ',
                                Customers.last_name
                            )
                        ) = LOWER(%s)
                        """,
                        (customer_name,)
                    )

                    sales = cursor.fetchall()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the sale\n"
                        f"\033[1;93mReason: {e}\033[0m"
                    )

                    sleep(0.5)

                    print(
                        "\033[1;93mPlease fix this issue before trying again\033[0m\n"
                    )

                    sleep(1)

                    connection.rollback()

                    return

                finally:

                    cursor.close()

                if not sales:

                    print("\033[1;91m✕ No Sale Found\033[0m\n")

                    sleep(1)

                    if repeat_operation(
                        "search",
                        "sale",
                        "Search Sale"
                    ):
                        break

                    continue

                for sale in sales:

                    print_sale(
                        *sale,
                        pause=False
                    )

                    print()

                if repeat_operation(
                    "search",
                    "sale",
                    "Search Sale"
                ):
                    break

                continue

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)

def sales_history(connection):

    while True:

        clear()
        title("SALES HISTORY")
        sleep(0.1)
        breadcrumb("Home", "Sales", "Sales History")
        sleep(0.5)

        print(
            "\n\033[1;93mSort By:\n"
            "\033[1;97m"
            "[1] Sale ID (Ascending)\n"
            "[2] Sale ID (Descending)\n"
            "[3] Sale Date (Oldest First)\n"
            "[4] Sale Date (Newest First)\n"
            "[5] Total Amount (Low to High)\n"
            "[6] Total Amount (High to Low)\n\n"
            "[0] Back\033[0m"
        )

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
                order_by = "Sales.sale_id ASC"
                break

            elif choice == 2:
                order_by = "Sales.sale_id DESC"
                break

            elif choice == 3:
                order_by = "Sales.sale_date ASC"
                break

            elif choice == 4:
                order_by = "Sales.sale_date DESC"
                break

            elif choice == 5:
                order_by = "Sales.total_amount ASC"
                break

            elif choice == 6:
                order_by = "Sales.total_amount DESC"
                break

            else:

                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                f"""
                SELECT
                    Sales.sale_id,
                    Customers.first_name,
                    Customers.last_name,
                    Users.username,
                    Sales.sale_date,
                    Sales.total_amount,
                    Sales.status
                FROM Sales
                LEFT JOIN Customers
                    ON Sales.customer_id = Customers.customer_id
                LEFT JOIN Users
                    ON Sales.user_id = Users.user_id
                ORDER BY {order_by};
                """
            )

            sales = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the sales history\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        if not sales:

            print("\n\033[1;91m❌ No sales found.\033[0m")
            sleep(1)
            input("\n\033[1;97mPress Enter to continue...\033[0m")
            return

        clear()
        title("SALES HISTORY")
        breadcrumb("Home", "Sales", "Sales History")

        print()

        for sale in sales:

            print_sale(
                *sale,
                pause=False
            )

            print()

        input("\n\033[1;97mPress Enter to continue...\033[0m")

        return








