from route.func.mysql import cursor, db
from flask import request, jsonify
from route.func.valid_sid import valid_sid
import json

def main():
    try:
        data = request.get_json()
        sid = data["sid"]
        token = data["token"]
        ip = request.remote_addr
        _, err = valid_sid(sid)
        if err:
            x = {
                "status_code": 400,
                "success": False,
                "message": "Sid in invalid",
                "data": {}
            }
            return jsonify(x)

        cursor.execute(f"SELECT username, firstname, lastname, token, secret_code, working_hour FROM users WHERE sid='{sid}'")
        result = cursor.fetchall()
        if len(result) == 0:
            x = {
                "status_code": 400,
                "success": False,
                "message": "user not found",
                "data": {}
            }
            return jsonify(x)
        tokendb = json.loads(result[0][3])

        if token not in tokendb.values():
            cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'trying to get user sid={sid} data but token is unauthorized')")
            db.commit()
            x = {
                "status_code": 400,
                "success": False,
                "message": "token is unauthorized",
                "data": {}
            }
            return jsonify(x)
        cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'get user sid={sid} data')")
        db.commit()
        
        x = {
            "status_code": 200,
            "success": True,
            "message": "Get user data success",
            "data": {
                "secret_code": result[0][4],
                "firstname": result[0][1],
                "lastname": result[0][2],
                "sid": sid,
                "username": result[0][0],
                "working_hour": json.loads(result[0][5])
            }
        }
        return jsonify(x)
    except:
        x = {
            "status_code": 500,
            "success": False,
            "message": "Process error",
            "data": {}
        }
        return jsonify(x)