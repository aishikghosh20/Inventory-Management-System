import os
from time import sleep
from database import connect_to_server, connect_using_env
from setup import setup_check, setup_wizard, save_config
from intializing_db import database_exists, create_database, connect_database, tables_exists, tables_create

def clear(): # To clear the screen
    os.system("cls")
    sleep(0.2)
    
  
def title():
    # menu
    print("\033[36m==========================================")
    print("\033[1;97m      INVENTORY MANAGEMENT SYSTEM \033[0m")
    print("\033[36m==========================================\033[0m")

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
    sleep(1.5)
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
           