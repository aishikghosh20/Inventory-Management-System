import mysql.connector
from pathlib import Path
import sys
from time import sleep
from intializing_db import exit_app
import re, bcrypt

def count_users(connection):
    cursor = connection.cursor(buffered = True)
    try:
        cursor.execute("SELECT COUNT(*) FROM USERS;")
        result  = cursor.fetchone() # returns a tuple with the result count
        cursor.close()
    except  Exception as e:
        print(f"\033[1;91mFailed: {e}\033[0m")
        sleep(1)
        cursor.close()
        exit_app()

    count = result[0] # to get the actual result from the tuple
    return count

def create_user(connection, count):
    print("\033[36m==========================================")
    print("\033[1;97m       CREATE ADMINISTRATOR ACCOUNT \033[0m")
    print("\033[36m==========================================\033[0m")
    sleep(0.1)

    print("\033[1;73mWelcome !\033[0m\n")
    sleep(0.5)

    print("\033[1;73mLets create your account\033[0m\n")
    sleep(0.5)

    print("\033[1;93mPlease enter the credentials as prompted:\033[0m\n")
    sleep(0.5)

    while True:
        try:
            username = input("\033[1;93mUSERNAME: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app()

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
            exit_app()

        finally:
            cursor.close()

    while True:
        try:
            first_name = input("\033[1;93mFIRST NAME: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app()

        if not first_name:
            print("\033[1;91m❌ First name cannot be empty\033[0m\n")
            sleep(1)
            continue

        break

    while True:
        try:
            last_name = input("\033[1;93mLAST NAME: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app()

        if not last_name:
            print("\033[1;91m❌ Last name cannot be empty\033[0m\n")
            sleep(1)
            continue

        break

    while True:
        try:
            email = input("\033[1;93mEMAIL: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app()

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
            exit_app()

        finally:
            cursor.close()

    while True:
        try:
            phone_number = input("\033[1;93mPHONE NUMBER: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app()

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
            exit_app()

        finally:
            cursor.close()


    while True:
        try:
            password = input("\033[1;93mPASSWORD: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app()

        if not password:
            print("\033[1;91m❌ Password cannot be empty\033[0m\n")
            sleep(1)
            continue

        if len(password) < 8:
            print("\033[1;91m❌ Password must be atleast 8 characters long\033[0m\n")
            sleep(1)
            continue

        try:
            confirm_password = input("\033[1;93mCONFIRM PASSWORD: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app()

        if not confirm_password:
            print("\033[1;91m❌ Password cannot be empty\033[0m\n")
            sleep(1)
            continue

        if  confirm_password != password:
            print("\033[1;91m❌ Passwords do not match\033[0m\n")
            sleep(0.5)
            print("\033[1;93mPlease try again...\033[0m\n")
            sleep(0.5)
            continue
        else:
            break

    # To get a hashed password to store in the database
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) 
    hashed_password = hashed_password.decode("utf-8") # converts into a normal string, for the password to be stored

    
    if count == 0:
        role = "Administrator"
        print("\033[1;97mNo existing users detected...\033[0m")
        sleep(0.5)
        print("\033[1;97mAdministrator role assigned automatically\033[0m")
        sleep(1)

    else:
        print("\033[1;93mSelect Role:")
        print("\033[1;97m[1] Administrator\n[2] Manager\n[3] Sales Staff\n[4] Inventory Staff\n[5] Viewer \033[0m")
        while True:
            try:
                choice = int(input("\033[1;93Choice:  \033[0m"))

            except ValueError:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            if choice == 1:
                role = "Administrator"
            elif choice == 2:
                role = "Manager"
            elif choice == 3:
                role = "Sales Staff"
            elif choice == 4:
                role = "Inventory Staff"
            elif choice == 5:
                role = "Viewer"

            else:
                print("\033[1;91mEnter a valid input\033[0m")
                sleep(1)
                continue

            break

    print("\033[1;93mInitializing user...")
    sleep(0.5)

    cursor = connection.cursor(buffered = True)
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
        VALUES (%s, %s, %s, %s, %s, %s, %s)
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

    except  Exception as e:
        print(f"\033[1;91mFailed to initialize\n\033[1;93mReason: {e}\033[0m")
        sleep(0.5)
        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
        sleep(1)
        exit_app()

    finally:
        cursor.close()

def user_login(connection):
    print("\033[36m==========================================")
    print("\033[1;97m           LOGIN \033[0m")
    print("\033[36m==========================================\033[0m")
    sleep(0.1)

    print("\033[1;73mLets login to your account\033[0m\n")
    sleep(0.5)

    print("\033[1;93mPlease enter the credentials as prompted:\033[0m\n")
    sleep(0.5)

    while True:
        try:
            username = input("\033[1;93mUSERNAME: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app()

        if not username:
            print("\033[1;91m❌ Username cannot be empty\033[0m\n")
            sleep(1)
            continue

        if not re.fullmatch(r"[A-Za-z0-9_]+", username):
            print("\033[1;91m❌ Username can only contain letters, numbers and underscores\033[0m\n")
            sleep(1)
            continue

        break
        

    while True:
        try:
            password = input("\033[1;93mPASSWORD: \033[0m").strip()

        except  Exception as e:
            print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
            sleep(0.5)
            print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
            sleep(1)
            exit_app()

        if not password:
            print("\033[1;91m❌ Password cannot be empty\033[0m\n")
            sleep(1)
            continue

        break


    cursor = connection.cursor(buffered = True)
    try:
        cursor.execute("SELECT user_id, first_name, last_name, password_hash, role FROM USERS WHERE username= %s", (username,))
        result = cursor.fetchone()  

    except  Exception as e:
        print(f"\033[1;91mFailed to continue with the application\n\033[1;93mReason: {e}\033[0m")
        sleep(0.5)
        print("\033[1;93mPlease fix this issue before trying again\033[0m\n")
        sleep(1)
        exit_app()

    finally:
        cursor.close()

    if result is None:
        return False
    else:
        user_id = result[0]
        first_name = result[1]
        last_name = result[2]
        stored_hash = result[3]
        role = result[4]
        match = bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))

        if match:
            print(f"\033[1;92mWelcome back, {first_name}!!\033[0m")
            sleep(1)
            return {"user_id" : user_id, "first_name" : first_name, "username": username, "last_name": last_name, "role" : role}
        else:
            return False
        
