from random import randrange, choice
from string import digits, ascii_letters
from func.mysql import mycursor, mydb
from func.encrypt import encrypt_string
import json

data = {
    "firstname": "test",
    "lastname": "test",
    "username": "test",
    "sid": "6634473123",
    "password": "test"
}
fn = data["firstname"]
ln = data["lastname"]
sid = data["sid"]
un = data["username"]
password = data["password"]

default_working_hour = []
for i in range(7):
    x = {
        "days": i+1,
        "hours": [
            [8, 0],
            [16, 0]
        ]
    }
    default_working_hour.append(x)

sc = encrypt_string(f'{randrange(1, 10**10):010}'+sid, "md5")
salt = ''.join(choice(ascii_letters+digits) for i in range(20))
password = f'{encrypt_string(password+salt, "sha256")}${salt}'
token = [encrypt_string(''.join(choice(ascii_letters+digits) for i in range(20))+sid, "sha256")]

sql = f"INSERT INTO users (sid, username, firstname, lastname, password, working_hour, subjects, token, secret_code) VALUES ('{sid}', '{un}', '{fn}', '{ln}', '{password}', '{json.dumps(default_working_hour)}', '{{}}', '{json.dumps(token)}', '{sc}')"
mycursor.execute(sql)
mydb.commit()
mycursor.execute(f"CREATE TABLE {sid}_events (id INT NOT NULL AUTO_INCREMENT , event_title VARCHAR(256) NOT NULL , event_des VARCHAR(256) NOT NULL , event_start DATETIME NOT NULL , event_end DATETIME NOT NULL , PRIMARY KEY (id))")
