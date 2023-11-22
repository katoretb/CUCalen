from random import randrange, choice
from string import digits, ascii_letters
from route.func.mysql import sqry
from flask import request, jsonify
from route.func.encrypt import encrypt_string
from route.func.validation import valid_sid
from route.func.mkqrbase64 import mb64qr
from route.func.errmaker import errmaker
import json
import pyotp
import sys

def main():
    try:
        sql = sqry()
        data = request.get_json()
        fn = data["firstname"]
        ln = data["lastname"]
        sid = data["sid"]
        un = data["username"]
        password = data["password"]
        ip = request.remote_addr
        msg, err = valid_sid(sid)
        if err:
            return msg

        result, err = sql.sqsel("users", ["sid"], f"sid='{sid}'")
        if err:
            return result

        if len(result) != 0:
            return errmaker(400, "The user already exists")

        default_working_hour = []
        for i in range(7):
            x = {
                "day": i+1,
                "hours": [
                    [8, 0],
                    [16, 0]
                ],
                "busy_hours": [
                    [
                        [12, 0],
                        [13, 0]
                    ]
                ]
            }
            default_working_hour.append(x)

        sc = encrypt_string(f'{randrange(1, 10**10):010}'+sid, "md5")

        salt = ''.join(choice(ascii_letters+digits) for i in range(20))
        password = f'{encrypt_string(password+salt, "sha256")}${salt}'

        token = {ip: encrypt_string(''.join(choice(ascii_letters+digits) for i in range(20))+sid+ip, "sha256")}

        k = pyotp.random_base32()

        ke = [
                "sid",
                "username",
                "firstname",
                "lastname",
                "password",
                "working_hour",
                "subjects",
                "token",
                "secret_code",
                "authkey"
                ]
        va = [  
                f'{sid}',
                f'{un}',
                f'{fn}',
                f'{ln}',
                f'{password}',
                f'{json.dumps(default_working_hour)}',
                f'{{}}',
                f'{json.dumps(token)}',
                f'{sc}',
                f'{k}'
                ]
        result, err = sql.sqadd("users", ke, va)
        if err:
            return result

        result, err = sql.sqadd("logs", ["ip", "info"], [ip, f'add user sid={sid}'])
        if err:
            return result

        c = [
            "id INT NOT NULL AUTO_INCREMENT",
            "event_title VARCHAR(256) NOT NULL",
            "event_des VARCHAR(256) NOT NULL",
            "event_start DATETIME NOT NULL",
            "event_end DATETIME NOT NULL",
            "event_color VARCHAR(7) NOT NULL",
            "PRIMARY KEY (id)"
        ]
        result, err = sql.sqcre(f"{sid}_events", c)
        if err:
            return result
        
        totp_auth = pyotp.totp.TOTP(k).provisioning_uri( 
            name=sid, 
            issuer_name='CUCalen'
        )

        x = {
            "status_code": 200,
            "success": True,
            "message": "Add account success",
            "data": {
                "token": token[ip],
                "qr": mb64qr(totp_auth)
            }
        }
        sql.kill_connect()
        return jsonify(x)
    except Exception as error:
        print(error, file=sys.stderr)
        return errmaker(500, f'Please contact web administrator')
