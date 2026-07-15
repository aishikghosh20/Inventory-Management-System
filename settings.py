import mysql.connector
from pathlib import Path
import sys, os
from time import sleep
from intializing_db import exit_app
import bcrypt
import re
from getpass import getpass
from time import sleep
from getpass import getpass
from time import sleep
from crud import confirm_changes, repeat_operation




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

def verify_current_password(
    entered_password,
    stored_hash
):

    return bcrypt.checkpw(
        entered_password.encode(),
        stored_hash.encode()
    )

def get_new_password():

    while True:

        print("\033[1;97mPassword Visibility:\n1. Hide Password (More Secure)\n2. Show Password\033[0m\n")
        while True:
            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 1:
                import pwinput
                while True:
                    password = pwinput.pwinput(prompt="\033[1;96mPassword: \033[0m", mask= "*")

                    if password:
                        break

                    print("\033[1;91m❌ Password cannot be empty\033[0m\n")
                    sleep(0.5)

            elif choice == 2:
                while True:
                    password = input("\033[1;96mPassword: \033[0m")

                    if password:
                        break

                    print("\033[1;91m❌ Password cannot be empty\033[0m\n")
                    sleep(0.5)

            else:
                print("\033[1;91mPlease enter 1 or 2...\033[0m")
                sleep(1)
                continue

            if password:
                break




        if len(password) < 8:

            print(
                "\033[1;91mPassword must contain at least 8 characters\033[0m"
            )

            sleep(1)

            continue

        if len(password) > 30:

            print(
                "\033[1;91mPassword cannot exceed 30 characters\033[0m"
            )

            sleep(1)

            continue

        return password

def confirm_new_password(
    new_password
):

    while True:

        print("\033[1;97mPassword Visibility:\n1. Hide Password (More Secure)\n2. Show Password\033[0m\n")
        while True:
            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 1:
                import pwinput
                while True:
                    password = pwinput.pwinput(prompt="\033[1;96mConfirm Password: \033[0m", mask= "*")

                    if password:
                        break

                    print("\033[1;91m❌ Password cannot be empty\033[0m\n")
                    sleep(0.5)

            elif choice == 2:
                while True:
                    password = input("\033[1;96mConfirm Password: \033[0m")

                    if password:
                        break

                    print("\033[1;91m❌ Password cannot be empty\033[0m\n")
                    sleep(0.5)

            else:
                print("\033[1;91mPlease enter 1 or 2...\033[0m")
                sleep(1)
                continue

            if password:
                break


        if password != new_password:

            print(
                "\033[1;91mPasswords do not match\033[0m"
            )

            sleep(1)

            continue

        return True

def review_password_change(
    username
):

    clear()
    title("REVIEW PASSWORD CHANGE")
    sleep(0.1)
    breadcrumb(
        "Home",
        "Settings",
        "Change Password",
        "Review"
    )

    print()

    print("\033[36m══════════════════════════════════════════════════════════════\033[0m")

    print(
        f"\033[1;97mUsername              : "
        f"\033[1;93m{username}\033[0m"
    )

    print(
        "\033[1;97mCurrent Password      : "
        "\033[1;92m✓ Verified\033[0m"
    )

    print(
        "\033[1;97mNew Password          : "
        "\033[1;92m✓ Valid\033[0m"
    )

    print(
        "\033[1;97mConfirmation          : "
        "\033[1;92m✓ Matched\033[0m"
    )

    print("\033[36m══════════════════════════════════════════════════════════════\033[0m")

    print()

def hash_password(
    password
):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

def user_exists(
    connection,
    user_id
):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            """
            SELECT 1
            FROM Users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        return cursor.fetchone() is not None

    finally:

        cursor.close()

def get_user(
    connection,
    user_id
):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            """
            SELECT
                user_id,
                username,
                first_name,
                last_name,
                role,
                created_at
            FROM Users
            WHERE user_id=%s
            """,
            (user_id,)
        )

        return cursor.fetchone()

    finally:

        cursor.close()

def print_user(
    user_id,
    username,
    first_name,
    last_name,
    role,
    created_at,
    pause=True
):

    print("\033[36m┌──────────────────────────────────────────────────────────────┐\033[0m")

    print(
        f"\033[1;97m│ USER ID : "
        f"\033[1;93m{user_id:<50}"
        f"\033[1;97m│\033[0m"
    )

    print("\033[36m└──────────────────────────────────────────────────────────────┘\033[0m")

    print(f"\033[1;97mUsername      : \033[1;93m{username}\033[0m")
    print(f"\033[1;97mFirst Name    : \033[1;93m{first_name}\033[0m")
    print(f"\033[1;97mLast Name     : \033[1;93m{last_name}\033[0m")
    print(f"\033[1;97mRole          : \033[1;93m{role}\033[0m")
    print(f"\033[1;97mCreated At    : \033[1;93m{created_at}\033[0m")

    print()

    if pause:

        input(
            "\033[1;97mPress Enter to continue...\033[0m"
        )

def review_new_user(
    username,
    first_name,
    last_name,
    role
):

    clear()
    title("REVIEW USER")
    sleep(0.1)
    breadcrumb(
        "Home",
        "Settings",
        "User Management",
        "Review"
    )

    print()

    print(f"\033[1;97mUsername      : \033[1;93m{username}\033[0m")
    print(f"\033[1;97mFirst Name    : \033[1;93m{first_name}\033[0m")
    print(f"\033[1;97mLast Name     : \033[1;93m{last_name}\033[0m")
    print(f"\033[1;97mRole          : \033[1;93m{role}\033[0m")

    print()

def review_user_update(
    username,
    first_name,
    last_name,
    role
):

    clear()
    title("REVIEW USER UPDATE")
    sleep(0.1)
    breadcrumb(
        "Home",
        "Settings",
        "User Management",
        "Review"
    )

    print()

    print(f"\033[1;97mUsername      : \033[1;93m{username}\033[0m")
    print(f"\033[1;97mFirst Name    : \033[1;93m{first_name}\033[0m")
    print(f"\033[1;97mLast Name     : \033[1;93m{last_name}\033[0m")
    print(f"\033[1;97mRole          : \033[1;93m{role}\033[0m")

    print()

def get_role():

    roles = [
        "Administrator",
        "Manager",
        "Inventory Staff",
        "Sales Staff",
        "Viewer"
    ]

    while True:

        print("\n\033[1;93mAvailable Roles:\033[0m\n")

        for index, role in enumerate(
            roles,
            start=1
        ):

            print(
                f"\033[1;97m[{index}] {role}\033[0m"
            )

        try:

            choice = int(
                input(
                    "\n\033[1;93mChoice: \033[0m"
                )
            )

        except ValueError:

            print("\033[1;91mEnter a valid input\033[0m")

            sleep(1)

            continue

        if 1 <= choice <= len(roles):

            return roles[choice-1]

        print("\033[1;91mEnter a valid choice\033[0m")

        sleep(1)

def get_username(connection):
    while True:
        try:
            username = input("\033[1;93mUSERNAME: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app(connection)

        if not username:
            print("\033[1;91m❌ Username cannot be empty\033[0m\n")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z0-9_]+", username):
            print("\033[1;91m❌ Username can only contain letters, numbers and underscores\033[0m\n")
            sleep(1)
            continue
        
        cursor = connection.cursor(buffered = True)
        try:
            cursor.execute("SELECT 1 FROM USERS WHERE username= %s", (username,))
            if cursor.fetchone():  # returns 1 is the username is present in the table
                print("\033[1;91m✕ Username already exists")
                sleep(1)
                continue
            else:
                break

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app(connection)

        finally:
            cursor.close()

    return username

def get_first_name(connection):
    while True:
        try:
            first_name = input("\033[1;93mFIRST NAME: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app(connection)

        if not first_name:
            print("\033[1;91m❌ First name cannot be empty\033[0m\n")
            sleep(1)
            continue

        break
    return first_name

def get_last_name(connection):
    while True:
        try:
            last_name = input("\033[1;93mLAST NAME: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app(connection)

        if not last_name:
            print("\033[1;91m❌ Last name cannot be empty\033[0m\n")
            sleep(1)
            continue

        break
    return last_name

def get_email(connection):
    while True:
        try:
            email = input("\033[1;93mEMAIL: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app(connection)

        if not email:
            print("\033[1;91m❌ Email cannot be empty\033[0m\n")
            sleep(1)
            continue
            
        if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            print("\033[1;91m❌ Invalid email address\033[0m\n")
            sleep(1)
            continue
        
        cursor = connection.cursor(buffered = True)
        try:
            cursor.execute("SELECT 1 FROM USERS WHERE email= %s", (email,))
            if cursor.fetchone():  # returns 1 if the emails is present in the table
                print("\033[1;91m✕ Email already exists")
                sleep(1)
                continue
            else:
                break

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app(connection)

        finally:
            cursor.close()

    return email

def get_phone(connection):
    while True:
        try:
            phone_number = input("\033[1;93mPHONE NUMBER: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app(connection)

        if not phone_number:
            print("\033[1;91m❌ Phone number cannot be empty\033[0m\n")
            sleep(1)
            continue

        if not re.fullmatch(r"^\+?[0-9\s-]+$", phone_number):
            print("\033[1;91m❌ Invalid phone number\033[0m\n")
            sleep(1)
            continue

        count_digits = phone_number.replace(" ","").replace("-","").replace("+","")

        if  len(count_digits) <7 or len(count_digits)>15:
            print("\033[1;91m❌ Invalid phone number length\033[0m\n")
            sleep(1)
            continue

        cursor = connection.cursor(buffered = True)
        try:
            cursor.execute("SELECT 1 FROM USERS WHERE phone_number= %s", (phone_number,))
            if cursor.fetchone():  # returns 1 if the emails is present in the table
                print("\033[1;91m✕ Phone number already exists")
                sleep(1)
                continue
            else:
                break

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app(connection)

        finally:
            cursor.close()

    return phone_number


def add_user(
    connection,
    current_user_id
):

    while True:

        clear()
        title("ADD USER")
        sleep(0.1)
        breadcrumb(
            "Home",
            "Settings",
            "User Management",
            "Add User"
        )
        sleep(0.5)

        print(
            "\n\033[1;93mPlease enter the details as prompted:\033[0m\n"
        )

        sleep(0.5)

        # ---------------- Username ---------------- #

        username = get_username(connection )

        if username is None:

            continue

        # ---------------- First Name ---------------- #

        first_name = get_first_name(connection)

        if first_name is None:

            continue

        # ---------------- Last Name ---------------- #

        last_name = get_last_name(connection)

        if last_name is None:

            continue

        # ---------------- Email ---------------- #

        email = get_email(connection)

        if email is None:

            continue

        # ---------------- Phone Number ---------------- #

        phone_number = get_phone(connection)

        if phone_number is None:

            continue

        # ---------------- Password ---------------- #

        password = get_new_password()

        if password is None:

            continue

        if not confirm_new_password(
            password
        ):

            continue

        # ---------------- Role ---------------- #

        role = get_role()

        if role is None:
            continue

        hashed_password = hash_password(
            password
        )

        sleep(0.5)

        review_new_user(
            username,
            first_name,
            last_name,
            role
        )

        sleep(0.5)

        if not confirm_changes():

            print("\033[1;97mCancelling...\033[0m")

            sleep(1)

            if repeat_operation(
                "add",
                "user",
                "User"
            ):

                continue

            return

        print("\033[1;93mInitializing user...\033[0m")

        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                INSERT INTO Users
                (
                    username,
                    password_hash,
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    role
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s,%s
                )
                """,
                (
                    username,
                    hashed_password,
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    role
                )
            )

            connection.commit()

            print(
                "\033[1;92m✓ User added successfully\033[0m"
            )

            sleep(1)

            if repeat_operation(
                "add",
                "user",
                "User"
            ):

                continue

            return

        except Exception as e:

            print(
                f"\033[1;91mFailed to add the user\n"
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

def view_users(connection):

    while True:

        clear()
        title("VIEW USERS")
        sleep(0.1)
        breadcrumb(
            "Home",
            "Settings",
            "User Management",
            "View Users"
        )
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    user_id,
                    username,
                    first_name,
                    last_name,
                    role,
                    created_at
                FROM Users
                ORDER BY
                    first_name ASC,
                    last_name ASC
                """
            )

            users = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the users\n"
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

        if not users:

            print(
                "\033[1;91m✕ No users found\033[0m"
            )

            sleep(1)

            return

        clear()
        title("VIEW USERS")
        breadcrumb(
            "Home",
            "Settings",
            "User Management",
            "View Users"
        )

        print()

        for user in users:

            print_user(
                *user,
                pause=False
            )

            print()

        input(
            "\033[1;97mPress Enter to continue...\033[0m"
        )

        return
        

def search_users(connection):

    while True:

        clear()
        title("SEARCH USER")
        sleep(0.1)
        breadcrumb(
            "Home",
            "Settings",
            "User Management",
            "Search User"
        )
        sleep(0.5)

        print(
            "\n\033[1;93mSearch Type:\n"
            "\033[1;97m"
            "[1] Search by User ID\n"
            "[2] Search by Username\n\n"
            "[0] Back\033[0m"
        )

        while True:

            try:

                choice = int(
                    input("\033[1;93mChoice: \033[0m")
                )

            except ValueError:

                print(
                    "\033[1;91mEnter a valid input\033[0m"
                )

                sleep(1)

                continue

            if choice == 0:

                return

            # ---------------- Search By User ID ---------------- #

            elif choice == 1:

                print(
                    "\n\033[1;93mPlease enter the User ID below....\033[0m\n"
                )

                sleep(0.5)

                while True:

                    try:

                        user_id = int(
                            input(
                                "\033[1;93mUSER ID: \033[0m"
                            )
                        )

                    except ValueError:

                        print(
                            "\033[1;91mEnter a valid input\033[0m"
                        )

                        sleep(1)

                        continue

                    if user_id <= 0:

                        print(
                            "\033[1;91mEnter a valid input\033[0m"
                        )

                        sleep(1)

                        continue

                    break

                user = get_user(
                    connection,
                    user_id
                )

                if not user:

                    print(
                        "\033[1;91m✕ No User Found\033[0m\n"
                    )

                    sleep(1)

                    if repeat_operation(
                        "search",
                        "user",
                        "user menu"
                    ):

                        break

                    return

                print_user(
                    *user,
                    pause=False
                )

                print()

                if repeat_operation(
                    "search",
                    "user",
                    "user menu"
                ):

                    break

                return

            # ---------------- Search By Username ---------------- #

            elif choice == 2:

                print(
                    "\n\033[1;93mPlease enter the Username below....\033[0m\n"
                )

                sleep(0.5)
                while True:
                    try:
                        username = input("\033[1;93mUSERNAME: \033[0m").strip()

                    except  Exception as e:
                        print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
                        sleep(0.5)
                        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
                        sleep(1)
                        exit_app(connection)

                    if not username:
                        print("\033[1;91m❌ Username cannot be empty\033[0m\n")
                        sleep(1)
                        continue

                    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
                        print("\033[1;91m❌ Username can only contain letters, numbers and underscores\033[0m\n")
                        sleep(1)
                        continue

                    break

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT
                            user_id,
                            username,
                            first_name,
                            last_name,
                            role,
                            created_at
                        FROM Users
                        WHERE LOWER(username)=LOWER(%s)
                        """,
                        (username,)
                    )

                    user = cursor.fetchone()

                except Exception as e:

                    print(
                        f"\033[1;91mFailed to load the user\n"
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

                if not user:

                    print(
                        "\033[1;91m✕ No User Found\033[0m\n"
                    )

                    sleep(1)

                    if repeat_operation(
                        "search",
                        "user",
                        "user menu"
                    ):

                        break

                    return

                print_user(
                    *user,
                    pause=False
                )

                print()

                if repeat_operation(
                    "search",
                    "user",
                    "user menu"
                ):

                    break

                return

            else:

                print(
                    "\033[1;91mEnter a valid input\033[0m"
                )

                sleep(1)

def update_user(
    connection,
    current_user_id
):

    while True:

        clear()
        title("UPDATE USER")
        sleep(0.1)
        breadcrumb(
            "Home",
            "Settings",
            "User Management",
            "Update User"
        )
        sleep(0.5)

        print(
            "\n\033[1;93mPlease enter the User ID below...\033[0m\n"
        )

        while True:

            try:

                user_id = int(
                    input(
                        "\033[1;93mUSER ID: \033[0m"
                    )
                )

            except ValueError:

                print(
                    "\033[1;91mEnter a valid input\033[0m"
                )

                sleep(1)

                continue

            if user_id <= 0:

                print(
                    "\033[1;91mEnter a valid input\033[0m"
                )

                sleep(1)

                continue

            break

        if not user_exists(
            connection,
            user_id
        ):

            print(
                "\033[1;91m✕ User does not exist\033[0m"
            )

            sleep(1)

            if repeat_operation(
                "update",
                "user",
                "User menu"
            ):

                continue

            return

        if user_id == current_user_id:

            print(
                "\033[1;91mYou cannot update your own account while logged in.\033[0m"
            )

            sleep(1)

            if repeat_operation(
                "update",
                "user",
                "User menu"
            ):

                continue

            return

        user = get_user(
            connection,
            user_id
        )

        (
            user_id,
            current_username,
            current_first_name,
            current_last_name,
            current_role,
            created_at
        ) = user

        print("\n\033[1;97mCurrent Details:\033[0m\n")

        print_user(
            *user,
            pause=False
        )

        sleep(0.5)

        while True:

            print("\n\033[1;93mUpdate Options:\033[0m")
            print(
                "\033[1;97m"
                "[1] Username\n"
                "[2] First Name\n"
                "[3] Last Name\n"
                "[4] Role\n"
                "[5] Update All\n\n"
                "[0] Cancel\033[0m"
            )

            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 0:
                return

            elif choice == 1:   
                # ---------------- Username ---------------- #

                username = get_username(
                    connection
                )

                if username is None:
                    continue

                first_name = current_first_name
                last_name = current_last_name
                role = current_role

                break

            elif choice == 2:

                # ---------------- First Name ---------------- #

                first_name = get_first_name(connection)

                if first_name is None:
                    continue

                username = current_username
                last_name = current_last_name
                role = current_role

                break

            elif choice == 3:

                # ---------------- Last Name ---------------- #

                last_name = get_last_name(connection)

                if last_name is None:

                    continue

                username = current_username
                first_name = current_first_name
                role = current_role

                break

            elif choice == 4:

                # ---------------- Role ---------------- #

                role = get_role()

                if role is None:

                    continue

                username = current_username
                first_name = current_first_name
                last_name = current_last_name

                break

            elif choice == 5:
                username = get_username(
                    connection
                )

                if username is None:
                    continue

                first_name = get_first_name(connection)

                if first_name is None:
                    continue

                last_name = get_last_name(connection)

                if last_name is None:

                    continue

                role = get_role()

                if role is None:

                    continue

                break

            else:
                print("\033[1;91mInvalid choice\033[0m")
                sleep(1)
                continue

        sleep(0.5)
        if choice in (4,5):
            if current_role == "Administrator" and role != "Administrator":

                cursor = connection.cursor(buffered=True)

                try:

                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM Users
                        WHERE role='Administrator'
                        """
                    )

                    admin_count = cursor.fetchone()[0]

                finally:

                    cursor.close()

                if admin_count == 1:

                    print(
                        "\033[1;91mCannot change the role of the last Administrator.\033[0m"
                    )

                    sleep(1)

                    if repeat_operation(
                        "update",
                        "user",
                        "User menu"
                    ):

                        continue

                    return

                sleep(0.5)


        review_user_update(
            username,
            first_name,
            last_name,
            role
        )

        sleep(0.5)

        if not confirm_changes():

            print("\033[1;97mCancelling...\033[0m")

            sleep(1)

            if repeat_operation(
                "update",
                "user",
                "User menu"
            ):

                continue

            return

        print("\033[1;93mUpdating user...\033[0m")

        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:
            cursor.execute(
                """
                UPDATE Users
                SET
                    username = %s,
                    first_name = %s,
                    last_name = %s,
                    role = %s
                WHERE user_id = %s
                """,
                (
                    username,
                    first_name,
                    last_name,
                    role,
                    user_id
                )
            )

            connection.commit()

            print(
                "\033[1;92m✓ User updated successfully\033[0m"
            )

            sleep(1)

            if repeat_operation(
                "update",
                "user",
                "User menu"
            ):

                continue

            return

        except Exception as e:

            print(
                f"\033[1;91mFailed to update the user\n"
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

def delete_user(
    connection,
    current_user_id
):

    while True:

        clear()
        title("DELETE USER")
        sleep(0.1)
        breadcrumb(
            "Home",
            "Settings",
            "User Management",
            "Delete User"
        )
        sleep(0.5)

        print(
            "\n\033[1;93mPlease enter the User ID below...\033[0m\n"
        )

        while True:

            try:

                user_id = int(
                    input(
                        "\033[1;93mUSER ID: \033[0m"
                    )
                )

            except ValueError:

                print(
                    "\033[1;91mEnter a valid input\033[0m"
                )

                sleep(1)

                continue

            if user_id <= 0:

                print(
                    "\033[1;91mEnter a valid input\033[0m"
                )

                sleep(1)

                continue

            break

        if not user_exists(
            connection,
            user_id
        ):

            print(
                "\033[1;91m✕ User does not exist\033[0m"
            )

            sleep(1)

            if repeat_operation(
                "delete",
                "user",
                "User menu"
            ):

                continue

            return

        if user_id == current_user_id:

            print(
                "\033[1;91mYou cannot delete your own account while logged in.\033[0m"
            )

            sleep(1)

            if repeat_operation(
                "delete",
                "user",
                "User menu"
            ):

                continue

            return

        user = get_user(
            connection,
            user_id
        )

        (
            user_id,
            username,
            first_name,
            last_name,
            current_role,
            created_at
        ) = user

        if current_role == "Administrator":

            cursor = connection.cursor(buffered=True)

            try:

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM Users
                    WHERE role='Administrator'
                    """
                )

                admin_count = cursor.fetchone()[0]

            finally:

                cursor.close()

            if admin_count == 1:

                print(
                    "\033[1;91mCannot delete the last Administrator.\033[0m"
                )

                sleep(1)

                if repeat_operation(
                    "delete",
                    "user",
                    "User menu"
                ):

                    continue

                return

        print("\n\033[1;97mUser Details:\033[0m\n")

        print_user(
            *user,
            pause=False
        )

        sleep(0.5)

        print("\033[1;93m┌───────────────────────────────────┐\033[0m") 
        print("\033[1;93m│           \033[1;91mARE YOU SURE?          \033[1;93m │\033[0m")
        print("\033[1;93m├───────────────────────────────────┤\033[0m")
        print("\033[1;93m│  \033[1;93m⚠️  THIS ACTION CANNOT BE UNDONE \033[1;93m │\033[0m")
        print("\033[1;93m├─────────────────┬─────────────────┤\033[0m")
        print(f"\033[1;93m│ \033[1;97m{"   [1] \033[1;92mYES     ":<10} \033[1;93m│ \033[1;97m{"    [2] \033[1;91mNO ":<22} \033[1;93m│")
        print("\033[1;93m└─────────────────┴─────────────────┘\033[0m")

        sleep(0.5)

        if not confirm_changes():

            print("\033[1;97mCancelling...\033[0m")

            sleep(1)

            if repeat_operation(
                "delete",
                "user",
                "User menu"
            ):

                continue

            return

        print("\033[1;93mDeleting user...\033[0m")

        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                DELETE FROM Users
                WHERE user_id = %s
                """,
                (user_id,)
            )

            connection.commit()

            print(
                "\033[1;92m✓ User deleted successfully\033[0m"
            )

            sleep(1)

            if repeat_operation(
                "delete",
                "user",
                "User menu"
            ):

                continue

            return

        except Exception as e:

            print(
                f"\033[1;91mFailed to delete the user\n"
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


def change_password(
    connection,
    user_id,
    username
):

    while True:

        clear()
        title("CHANGE PASSWORD")
        sleep(0.1)
        breadcrumb(
            "Home",
            "Settings",
            "Change Password"
        )
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    password_hash
                FROM Users
                WHERE user_id = %s
                """,
                (user_id,)
            )

            user = cursor.fetchone()

            if not user:

                print(
                    "\033[1;91m✕ Current user does not exist\033[0m"
                )

                sleep(1)

                connection.rollback()

                return

            stored_hash = user[0]

        except Exception as e:

            print(
                f"\033[1;91mFailed to verify the user\n"
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

        print(
            "\n\033[1;93mPlease verify your current password.\033[0m\n"
        )

        print("\033[1;97mPassword Visibility:\n1. Hide Password (More Secure)\n2. Show Password\033[0m\n")
        while True:
            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 1:
                import pwinput
                while True:
                    current_password = pwinput.pwinput(prompt="\033[1;96mCurrent Password: \033[0m", mask= "*")

                    if current_password:
                        break

                    print("\033[1;91m❌ Password cannot be empty\033[0m\n")
                    sleep(0.5)

            elif choice == 2:
                while True:
                    current_password = input("\033[1;96mCurrent Password: \033[0m")

                    if current_password:
                        break

                    print("\033[1;91m❌ Password cannot be empty\033[0m\n")
                    sleep(0.5)

            else:
                print("\033[1;91mPlease enter 1 or 2...\033[0m")
                sleep(1)
                continue

            if current_password:
                break


        # if current_password.lower() == "cancel":

        #     print("\033[1;97mCancelling...\033[0m")

        #     sleep(1)

        #     return

        if not verify_current_password(
            current_password,
            stored_hash
        ):

            print(
                "\033[1;91mIncorrect current password\033[0m"
            )

            sleep(1)

            continue

        print(
            "\033[1;92m✓ Current password verified\033[0m\n"
        )

        sleep(0.5)

        print("\033[1;97mPassword Visibility:\n1. Hide Password (More Secure)\n2. Show Password\033[0m\n")
        while True:
            try:
                choice = int(input("\033[1;93mChoice: \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 1:
                import pwinput
                while True:
                    new_password = pwinput.pwinput(prompt="\033[1;96mNew Password: \033[0m", mask= "*")

                    if new_password:
                        break

                    print("\033[1;91m❌ Password cannot be empty\033[0m\n")
                    sleep(0.5)

            elif choice == 2:
                while True:
                    new_password = input("\033[1;96mNew Password: \033[0m")

                    if new_password:
                        break

                    print("\033[1;91m❌ Password cannot be empty\033[0m\n")
                    sleep(0.5)

            else:
                print("\033[1;91mPlease enter 1 or 2...\033[0m")
                sleep(1)
                continue

            if new_password:
                break

        if new_password is None:
            continue

        if verify_current_password(
            new_password,
            stored_hash
        ):

            print(
                "\033[1;91mNew password cannot be the same as the current password\033[0m"
            )

            sleep(1)

            continue

        if not confirm_new_password(
            new_password
        ):

            continue

        sleep(0.5)

        review_password_change(
            username
        )

        sleep(0.5)

        if not confirm_changes():

            print("\033[1;97mCancelling...\033[0m")

            sleep(1)

            return

        print("\033[1;93mUpdating password...\033[0m")

        sleep(0.5)

        hashed_password = hash_password(
            new_password
        )

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                UPDATE Users
                SET password_hash = %s
                WHERE user_id = %s
                """,
                (
                    hashed_password,
                    user_id
                )
            )

            connection.commit()

            print(
                "\033[1;93mYour password has been changed successfully.\n"
                "For security reasons, please log in again.\033[0m"
            )

            sleep(1)
            input("\033[1;97mPress Enter to exit app...\033[0m")

            exit_app(connection)

        except Exception as e:

            print(
                f"\033[1;91mFailed to change the password\n"
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


def manage_users(
    connection,
    current_user_id
):

    while True:

        clear()
        title("USER MANAGEMENT")
        sleep(0.2)
        breadcrumb(
            "Home",
            "Settings",
            "User Management"
        )
        sleep(0.5)

        print(
            "\n"
            "\033[1;97m"
            "[1] ➕ Add User\n"
            "[2] 📋 View Users\n"
            "[3] 🔍 Search User\n"
            "[4] ✏️ Update User\n"
            "[5] 🗑️ Delete User\n\n"
            "[0] ← Back"
            "\033[0m\n"
        )

        while True:

            try:

                choice = int(
                    input("\033[1;93mChoice: \033[0m")
                )

            except ValueError:

                print(
                    "\033[1;91mEnter a valid input\033[0m"
                )

                sleep(1)

                continue

            if choice < 0 or choice > 5:

                print(
                    "\033[1;91mEnter a valid choice\033[0m"
                )

                sleep(1)

                continue

            if choice == 0:

                return

            elif choice == 1:

                print(
                    "\n\033[1;97mInitializing user creation...\033[0m"
                )

                sleep(0.5)

                add_user(
                    connection,
                    current_user_id
                )

                break

            elif choice == 2:

                print(
                    "\n\033[1;97mLoading users...\033[0m"
                )

                sleep(0.5)

                view_users(connection)

                break

            elif choice == 3:

                print(
                    "\n\033[1;97mLoading search bar...\033[0m"
                )

                sleep(0.5)

                search_users(connection)

                break

            elif choice == 4:

                print(
                    "\n\033[1;97mUpdating user...\033[0m"
                )

                sleep(0.5)

                update_user(
                    connection,
                    current_user_id
                )

                break

            elif choice == 5:

                print(
                    "\n\033[1;97mDeleting user...\033[0m"
                )

                sleep(0.5)

                delete_user(
                    connection,
                    current_user_id
                )

                break


def print_role_summary(
    role,
    total_users
):

    print("\033[36m┌──────────────────────────────────────────────────────────────┐\033[0m")

    print(
        f"\033[1;97m│ ROLE : "
        f"\033[1;93m{role:<53}"
        f"\033[1;97m│\033[0m"
    )

    print("\033[36m└──────────────────────────────────────────────────────────────┘\033[0m")

    print(
        f"\033[1;97mTotal Users : "
        f"\033[1;93m{total_users}\033[0m"
    )

    print()

def print_role_user(
    user_id,
    username,
    first_name,
    last_name,
    created_at
):

    print("\033[36m┌──────────────────────────────────────────────────────────────┐\033[0m")

    print(
        f"\033[1;97m│ USER ID : "
        f"\033[1;93m{user_id:<50}"
        f"\033[1;97m│\033[0m"
    )

    print("\033[36m└──────────────────────────────────────────────────────────────┘\033[0m")

    print(
        f"\033[1;97mUsername     : "
        f"\033[1;93m{username}\033[0m"
    )

    print(
        f"\033[1;97mFirst Name   : "
        f"\033[1;93m{first_name}\033[0m"
    )

    print(
        f"\033[1;97mLast Name    : "
        f"\033[1;93m{last_name}\033[0m"
    )

    print(
        f"\033[1;97mCreated At   : "
        f"\033[1;93m{created_at}\033[0m"
    )

    print()

def review_role_update(
    username,
    old_role,
    new_role
):

    clear()

    title("REVIEW ROLE UPDATE")

    sleep(0.1)

    breadcrumb(
        "Home",
        "Settings",
        "Role Management",
        "Review"
    )

    print()

    print(
        f"\033[1;97mUsername      : "
        f"\033[1;93m{username}\033[0m"
    )

    print(
        f"\033[1;97mCurrent Role  : "
        f"\033[1;93m{old_role}\033[0m"
    )

    print(
        f"\033[1;97mNew Role      : "
        f"\033[1;92m{new_role}\033[0m"
    )

    print()

def count_role_users(
    connection,
    role
):

    cursor = connection.cursor(buffered=True)

    try:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Users
            WHERE role = %s
            """,
            (role,)
        )

        return cursor.fetchone()[0]

    finally:

        cursor.close()

def view_roles(connection):

    while True:

        clear()
        title("VIEW ROLES")
        sleep(0.1)
        breadcrumb(
            "Home",
            "Settings",
            "Role Management",
            "View Roles"
        )
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    role,
                    COUNT(*)
                FROM Users
                GROUP BY role
                ORDER BY role
                """
            )

            roles = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the roles\n"
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

        if not roles:

            print(
                "\033[1;91m✕ No roles found\033[0m"
            )

            sleep(1)

            return

        for role in roles:

            print_role_summary(*role)

        input(
            "\033[1;97mPress Enter to continue...\033[0m"
        )

        return

def users_by_role(connection):

    while True:

        clear()
        title("USERS BY ROLE")
        sleep(0.1)
        breadcrumb(
            "Home",
            "Settings",
            "Role Management",
            "Users By Role"
        )
        sleep(0.5)

        role = get_role()

        if role is None:

            continue

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    user_id,
                    username,
                    first_name,
                    last_name,
                    created_at
                FROM Users
                WHERE role = %s
                ORDER BY
                    first_name ASC,
                    last_name ASC
                """,
                (role,)
            )

            users = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load users\n"
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

        if not users:

            print(
                f"\033[1;91m✕ No users found with the role '{role}'\033[0m"
            )

            sleep(1)

            return

        clear()
        title(f"{role.upper()} USERS")
        breadcrumb(
            "Home",
            "Settings",
            "Role Management",
            role
        )

        print()

        print(
            f"\033[1;96mTotal Users : {len(users)}\033[0m\n"
        )

        for user in users:

            print_role_user(*user)

        input(
            "\033[1;97mPress Enter to continue...\033[0m"
        )

        return


def manage_roles(connection):

    while True:

        clear()
        title("ROLE MANAGEMENT")
        sleep(0.2)

        breadcrumb(
            "Home",
            "Settings",
            "Role Management"
        )

        sleep(0.5)

        print(
            "\n"
            "\033[1;97m"
            "[1] 📋 View Roles\n"
            "[2] 👥 Users By Role\n\n"
            "[0] ← Back"
            "\033[0m\n"
        )

        while True:

            try:

                choice = int(
                    input("\033[1;93mChoice: \033[0m")
                )

            except ValueError:

                print(
                    "\033[1;91mEnter a valid input\033[0m"
                )

                sleep(1)

                continue

            if choice < 0 or choice > 2:

                print(
                    "\033[1;91mEnter a valid choice\033[0m"
                )

                sleep(1)

                continue

            if choice == 0:

                return

            elif choice == 1:

                print(
                    "\n\033[1;97mLoading roles...\033[0m"
                )

                sleep(0.5)

                view_roles(connection)

                break

            elif choice == 2:

                print(
                    "\n\033[1;97mLoading users by role...\033[0m"
                )

                sleep(0.5)

                users_by_role(connection)

                break


def print_database_information(
    database_name,
    version,
    users,
    products,
    categories,
    suppliers,
    customers,
    purchases,
    sales,
    inventory_value
):

    clear()

    title("DATABASE INFORMATION")

    sleep(0.1)

    breadcrumb(
        "Home",
        "Settings",
        "Database Information"
    )

    print()

    print("\033[36m══════════════════════════════════════════════════════════════\033[0m")

    print(f"\033[1;97mDatabase Name      : \033[1;93m{database_name}\033[0m")
    print(f"\033[1;97mMySQL Version      : \033[1;93m{version}\033[0m")
    print(f"\033[1;97mTotal Users        : \033[1;93m{users}\033[0m")
    print(f"\033[1;97mTotal Products     : \033[1;93m{products}\033[0m")
    print(f"\033[1;97mTotal Categories   : \033[1;93m{categories}\033[0m")
    print(f"\033[1;97mTotal Suppliers    : \033[1;93m{suppliers}\033[0m")
    print(f"\033[1;97mTotal Customers    : \033[1;93m{customers}\033[0m")
    print(f"\033[1;97mTotal Purchases    : \033[1;93m{purchases}\033[0m")
    print(f"\033[1;97mTotal Sales        : \033[1;93m{sales}\033[0m")
    print(f"\033[1;97mInventory Value    : \033[1;93m₹ {inventory_value:.2f}\033[0m")

    print("\033[36m══════════════════════════════════════════════════════════════\033[0m")

    print()

def db_info(connection):

    while True:

        clear()
        title("DATABASE INFORMATION")
        sleep(0.1)

        breadcrumb(
            "Home",
            "Settings",
            "Database Information"
        )

        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute("SELECT DATABASE()")
            database_name = cursor.fetchone()[0]

            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Users")
            users = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Products")
            products = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Categories")
            categories = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Suppliers")
            suppliers = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Customers")
            customers = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Purchases")
            purchases = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Sales")
            sales = cursor.fetchone()[0]


            cursor.execute(
                """
                SELECT
                    IFNULL(
                        SUM(quantity * selling_price),
                        0
                    )
                FROM Products
                """
            )

            inventory_value = float(
                cursor.fetchone()[0]
            )

        except Exception as e:

            print(
                f"\033[1;91mFailed to load database information\n"
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


        print_database_information(
            database_name,
            version,
            users,
            products,
            categories,
            suppliers,
            customers,
            purchases,
            sales,
            inventory_value
        )

        input(
            "\033[1;97mPress Enter to continue...\033[0m"
        )

        return










