from random import choice
from string import digits, ascii_letters
from route.func.mysql import sqry
from flask import request, jsonify
from route.func.encrypt import encrypt_string
from route.func.validation import valid_sid
import json
from route.func.errmaker import errmaker
import pyotp
import sys

def main():
    try:
        sql = sqry()
        data = request.get_json()
        sid = data["sid"]
        password = data["password"]
        ip = request.remote_addr
        msg, err = valid_sid(sid)
        if err:
            return msg

        result, err = sql.sqsel("users", ["password", "token"], f"sid='{sid}'")
        if err:
            return result

        if len(result) == 0:
            return errmaker(400, "User not found")
        pas = result[0][0].split("$")
        salt = pas[1]
        check_pass = pas[0]
        password = encrypt_string(password+salt, "sha256")
        token = json.loads(result[0][1])
        token[ip] = encrypt_string(''.join(choice(ascii_letters+digits) for i in range(20))+sid+ip, "sha256")

        if password != check_pass:
            result, err = sql.sqadd("logs", ["ip", "info"], [ip, f'trying to login to sid={sid} but password is not correct'])
            if err:
                return result
            return errmaker(400, "Password is incorrect")
        
        result, err = sql.squpd("users", {"token": f"'{json.dumps(token)}'"}, f"sid='{sid}'")
        if err:
            return result

        result, err = sql.sqadd("logs", ["ip", "info"], [ip, f'login to sid={sid}'])
        if err:
            return result

        result, err = sql.sqsel("users", ["username", "firstname", "lastname", "secret_code", "working_hour"], f"sid='{sid}'")
        if err:
            return result
        
        x = {
            "status_code": 200,
            "success": True,
            "message": "Login success",
            "data": {
                "token": token[ip],
                "secret_code": result[0][3],
                "firstname": result[0][1],
                "lastname": result[0][2],
                "sid": sid,
                "username": result[0][0],
                "working_hour": json.loads(result[0][4])
            }
        }
        sql.kill_connect()
        return jsonify(x)
    except Exception as error:
        print(error, file=sys.stderr)
        return errmaker(500, f'Please contact owner')
