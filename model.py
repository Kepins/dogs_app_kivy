import os
from dotenv import load_dotenv
import mysql.connector

# load environment variables from '.env' file
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    passwd=os.getenv('MYSQL_PASSWD'),
    database=os.getenv('MYSQL_DATABASE')
)

# mycursor = db.cursor()
