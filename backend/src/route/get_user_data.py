from route.func.mysql import sqry
from flask import request, jsonify
from route.func.validation import valid_sid, valid_token
import json

def main():
    sql = sqry()
    data = request.get_json()
    sid = data["sid"]
    token = data["token"]
    ip = request.remote_addr
    msg, err = valid_sid(sid)
    if err:
        return msg

    msg, err = valid_token(ip, sid, token, "get user")
    if err:
        return msg
    
    result, err = sql.sqsel("users", ["username", "firstname", "lastname", "secret_code", "working_hour"], f"sid='{sid}'")
    if err:
        return result
    
    resul, err = sql.sqadd("logs", ["ip", "info"], [ip, f'get user sid={sid} data'])
    if err:
        return resul
    
    x = {
        "status_code": 200,
        "success": True,
        "message": "Get user data success",
        "data": {
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