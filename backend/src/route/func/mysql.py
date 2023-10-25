import MySQLdb
from os import getenv
from dotenv import load_dotenv

load_dotenv()

db = MySQLdb.connect(
 host = getenv('host'),
 user = getenv('user'),
 password = getenv('pass'),
 database = "CUCalen"
)

cursor = db.cursor()

print("test")