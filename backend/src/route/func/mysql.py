import MySQLdb
from os import getenv
from dotenv import load_dotenv

load_dotenv()

mydb = MySQLdb.connect(
 host = getenv('host'),
 user = getenv('user'),
 password = getenv('pass'),
 database = "CUCalen"
)

mycursor = mydb.cursor()

print("test")