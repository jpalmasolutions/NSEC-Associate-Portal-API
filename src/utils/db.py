from mysql.connector import connection, MySQLConnection
from src.aws.secrets import get_secret
import os

db: MySQLConnection = None

def get_db_connection() -> MySQLConnection:

    global db

    if db == None:

        tag = os.environ.get('NSEC_DATABASE_PWD_SECRET_TAG','')
        db_pwd = get_secret(secret_name=tag)[tag]

        db = connection.MySQLConnection(
                user = os.environ.get('NSEC_DATABASE_USER'),
                password = db_pwd,
                host = os.environ.get('NSEC_DATABASE_HOST'),
                database = os.environ.get('NSEC_DATABASE')
            )
    elif db.is_connected() == False:
        db.connect()
    
    return db

def close_db_connection(connection : MySQLConnection) -> None:
    connection.close()