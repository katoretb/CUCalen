from random import randrange, choice
from string import digits, ascii_letters
from route.func.mysql import cursor, db
from flask import request, jsonify
from route.func.encrypt import encrypt_string
from route.func.valid_sid import valid_sid
import json


def main():
    try:
        data = request.get_json()
        sid = data["sid"]
        password = data["password"]
        ip = request.remote_addr
        _, err = valid_sid(sid)
        if err:
            x = {
                "status_code": 400,
                "success": False,
                "token": "",
                "message": "Sid in invalid"
            }
            return jsonify(x)

        cursor.execute(f"SELECT password, token FROM users WHERE sid='{sid}'")
        result = cursor.fetchall()
        if len(result) == 0:
            x = {
                "status_code": 400,
                "success": False,
                "token": "",
                "message": "user not found"
            }
            return jsonify(x)
        pas = result[0][0].split("$")
        salt = pas[1]
        check_pass = pas[0]
        password = encrypt_string(password+salt, "sha256")
        token = json.loads(result[0][1])
        token[ip] = encrypt_string(''.join(choice(ascii_letters+digits) for i in range(20))+sid+ip, "sha256")

        if password != check_pass:
            cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'trying to login to sid={sid} but password is not correct')")
            db.commit()
            x = {
                "status_code": 400,
                "success": False,
                "token": "",
                "message": "password is not correct"
            }
            return jsonify(x)
        cursor.execute(f"UPDATE users SET token='{json.dumps(token)}' WHERE sid='{sid}'")
        db.commit()
        cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'login to sid={sid}')")
        db.commit()
        
        x = {
            "status_code": 200,
            "success": True,
            "token": token[ip],
            "message": "Login success"
        }
        return jsonify(x)
    except:
        x = {
            "status_code": 500,
            "success": False,
            "token": "",
            "message": "Process error"
        }
        return jsonify(x)