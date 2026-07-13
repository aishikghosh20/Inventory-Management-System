from pathlib import Path
from time import sleep
from getpass import getpass
import sys
from config import BASE_DIR

def setup_check():
    env_file = Path(BASE_DIR/".env")

    if env_file.exists():
        return True
    
    return False

def setup_wizard():
    print("\033[1;73mIt looks like this is your first time running this application\033[0m\n")
    sleep(0.5)
    print("\033[1;73mLets configure your MySQL Server...\033[0m\n")
    sleep(0.5)
    print(f"{" ":<12}{"\033[1;93m<Press Enter to use default values>\033[0m"}\n")
    sleep(0.1)

    host = input("\033[1;96mHost [localhost](default): \033[0m").strip()
    if not host:
        host = "localhost"

    while True:
        port = (input("\033[1;96mPort [3306](default): \033[0m")).strip()
        if not port:
            port = 3306
            break
        if port.isdigit():
            port = int(port)
            break

        print("\033[1;91m❌ Please enter a valid port number\033[0m\n")
        sleep(0.5)

    user = input("\033[1;96mUser [root](default): \033[0m").strip()
    if not user:
        user = "root"

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

    print("\033[1;97mChecking connection...")
    return host,port,user,password
    

def save_config(host, port, user, password):

    if getattr(sys, "frozen", False):
        # Running as an executable
        BASE_DIR = Path(sys.executable).parent
    else:
        # Running from source code
        BASE_DIR = Path(__file__).resolve().parent

    env_path = BASE_DIR / ".env"

    try:
        with open(env_path, "w") as file:
            file.write(f"DB_HOST={host}\n")
            file.write(f"DB_PORT={port}\n")
            file.write(f"DB_USER={user}\n")
            file.write(f'DB_PASSWORD="{password}"\n')
            file.write("DB_NAME=inventory_management\n")
        
        if env_path.exists():
            return True, "Configuration saved successfully"
        
        return False, "Failed to create .env file"
    
    except Exception as e:
        return False, str(e)
    



