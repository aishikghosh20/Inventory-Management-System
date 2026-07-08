# to connect to the MySQL server using the credentials from config.py

import mysql.connector
import time

def connect_to_server(host, port, user, password):
    try: 
        connection = mysql.connector.connect(
        host = host,
        port = port,
        user = user,
        password = password
        )
        return connection
    
    except Exception as e:
        print(f"\033[1;91mConnection Failed : \033[1;97m{e}\033[0m\n")
        time.sleep(0.5)
        return None
    
def connect_using_env():
    from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
    try: 
        connection = mysql.connector.connect(
        host = DB_HOST,
        port = DB_PORT,
        user = DB_USER,
        password = DB_PASSWORD
        )
        return connection
    
    except Exception as e:
        print(f"\033[1;91mConnection Failed : \033[1;97m{e}\033[0m\n")
        time.sleep(0.5)
        return None
