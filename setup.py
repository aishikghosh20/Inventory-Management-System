from pathlib import Path
from time import sleep
from getpass import getpass
import sys

def setup_check():
    env_file = Path(".env")

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

    while True:
        password = getpass("\033[1;96mPassword: \033[0m")

        if password:
            break

        print("\033[1;91m❌ Password cannot be empty\033[0m\n")
        sleep(0.5)

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
        
        if env_path.exist():
            return True
        
        return False, "Failed to create .env file"
    
    except Exception as e:
        return False, str(e)
    



