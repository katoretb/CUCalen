from random import randrange, choice
from string import digits, ascii_letters
from route.func.mysql import cursor, db
from flask import request, jsonify
from route.func.encrypt import encrypt_string
from route.func.valid_sid import valid_sid
import json

def guderr(code, msg): #get user data error
    x = {
        "status_code": code,
        "success": False,
        "message": msg,
        "secret_code": "",
        "firstname": "",
        "lastname": "",
        "sid": "",
        "username": "",
        "working_hour": [],
        "token": ""
    }
    return jsonify(x)

def main():
    try:
        data = request.get_json()
        sid = data["sid"]
        password = data["password"]
        ip = request.remote_addr
        _, err = valid_sid(sid)
        if err:
            return guderr(400, "Sid in invalid")

        cursor.execute(f"SELECT password, token FROM users WHERE sid='{sid}'")
        result = cursor.fetchall()
        if len(result) == 0:
            return guderr(400, "user not found")
        pas = result[0][0].split("$")
        salt = pas[1]
        check_pass = pas[0]
        password = encrypt_string(password+salt, "sha256")
        token = json.loads(result[0][1])
        token[ip] = encrypt_string(''.join(choice(ascii_letters+digits) for i in range(20))+sid+ip, "sha256")

        if password != check_pass:
            cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'trying to login to sid={sid} but password is not correct')")
            db.commit()
            return guderr(400, "password is not correct")
        cursor.execute(f"UPDATE users SET token='{json.dumps(token)}' WHERE sid='{sid}'")
        db.commit()
        cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'login to sid={sid}')")
        db.commit()

        cursor.execute(f"SELECT username, firstname, lastname, secret_code, working_hour FROM users WHERE sid='{sid}'")
        result = cursor.fetchall()
        
        x = {
            "status_code": 200,
            "success": True,
            "token": token[ip],
            "message": "Login success",
            "secret_code": result[0][3],
            "firstname": result[0][1],
            "lastname": result[0][2],
            "sid": sid,
            "username": result[0][0],
            "working_hour": json.loads(result[0][4])
        }
        return jsonify(x)
    except:
        return guderr(500, "Process error")
    