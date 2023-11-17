from route.func.mysql import sqry
from flask import request, jsonify
from route.func.validation import valid_sid, valid_token
import json

def main():
    sql = sqry()
    data = request.get_json()
    sid = data["sid"]
    token = data["token"]
    fn = data["firstname"]
    ln = data["lastname"]
    un = data["username"]
    wh = data["working_hour"]
    ip = request.remote_addr
    msg, err = valid_sid(sid)
    if err:
        return msg

    msg, err = valid_token(ip, sid, token, "eidt user", sql)
    if err:
        return msg

    result, err = sql.sqsel("users", ["working_hour"], f"sid='{sid}'")
    if err:
        return result

    whdb = json.loads(result[0][0])
    
    if len(wh) < 7:
        for i in wh:
            for j in range(len(whdb)):
                if whdb[j]["day"] == i["day"]:
                    whdb[j]["hours"] = i["hours"]
                    whdb[j]["busy_hours"] = i["busy_hours"]
        wh = whdb

    d = {
        "firstname": f"'{fn}'",
        "lastname": f"'{ln}'",
        "username": f"'{un}'",
        "working_hour": f"'{json.dumps(wh)}'"
    }
    result, err = sql.squpd("users", d, f"sid='{sid}'")
    if err:
        return result

    result, err = sql.sqadd("logs", ["ip", "info"], [ip, f'edit user sid={sid} data'])
    if err:
        return result
    
    x = {
        "status_code": 200,
        "success": True,
        "message": "Edit user data success"
    }
    sql.kill_connect()
    return jsonify(x)