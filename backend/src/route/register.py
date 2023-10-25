from random import randrange, choice
from string import digits, ascii_letters
from route.func.mysql import mycursor, mydb
from flask import request, jsonify
from route.func.encrypt import encrypt_string
from route.func.valid_sid import valid_sid
import json


def main():
    try:
        data = request.get_json()
        fn = data["firstname"]
        ln = data["lastname"]
        sid = data["sid"]
        un = data["username"]
        password = data["password"]
        ip = request.remote_addr
        _, err = valid_sid(sid)
        if err:
            x = {
                "status_code": 500,
                "success": False,
                "token": "",
                "message": "Sid in invalid"
            }
            return jsonify(x)

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
        token = {ip: encrypt_string(''.join(choice(ascii_letters+digits) for i in range(20))+sid+ip, "sha256")}

        mycursor.execute(f"INSERT INTO users (sid, username, firstname, lastname, password, working_hour, subjects, token, secret_code) VALUES ('{sid}', '{un}', '{fn}', '{ln}', '{password}', '{json.dumps(default_working_hour)}', '{{}}', '{json.dumps(token)}', '{sc}')")
        mydb.commit()
        mycursor.execute(f"CREATE TABLE {sid}_events (id INT NOT NULL AUTO_INCREMENT , event_title VARCHAR(256) NOT NULL , event_des VARCHAR(256) NOT NULL , event_start DATETIME NOT NULL , event_end DATETIME NOT NULL , PRIMARY KEY (id))")

        x = {
            "status_code": 200,
            "success": True,
            "token": token[0],
            "message": "Add account success"
        }
        return jsonify(x)
    except:
        x = {
            "status_code": 500,
            "success": False,
            "token": "",
            "message": "Proc"
        }
        return jsonify(x)