from route.func.mysql import cursor, db
from flask import request, jsonify
from route.func.valid_sid import valid_sid
import json

def guderr(code, msg):
    x = {
        "status_code": code,
        "success": False,
        "message": msg,
        "secret_code": "",
        "firstname": "",
        "lastname": "",
        "sid": "",
        "username": ""
    }
    return jsonify(x)

def main():
    try:
        data = request.get_json()
        sid = data["sid"]
        token = data["token"]
        ip = request.remote_addr
        _, err = valid_sid(sid)
        if err:
            return guderr(400, "Sid in invalid")

        cursor.execute(f"SELECT username, firstname, lastname, token, secret_code FROM users WHERE sid='{sid}'")
        result = cursor.fetchall()
        if len(result) == 0:
            return guderr(400, "user not found")
        tokendb = json.loads(result[0][3])

        if token not in tokendb.values():
            cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'trying to get user sid={sid} data but token is unauthorized')")
            db.commit()
            return guderr(400, "token is unauthorized")
        cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'get user sid={sid} data')")
        db.commit()
        
        x = {
            "status_code": 200,
            "success": True,
            "message": "Get user data success",
            "secret_code": result[0][4],
            "firstname": result[0][1],
            "lastname": result[0][2],
            "sid": sid,
            "username": result[0][0]
        }
        return jsonify(x)
    except:
        return guderr(500, "Process error")