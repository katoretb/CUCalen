from route.func.mysql import cursor, db
from flask import request, jsonify
from route.func.valid_sid import valid_sid
import json

def guderr(code, msg):
    x = {
        "status_code": code,
        "success": False,
        "message": msg
    }
    return jsonify(x)

def main():
    try:
        data = request.get_json()
        sid = data["sid"]
        token = data["token"]
        fn = data["firstname"]
        ln = data["lastname"]
        un = data["username"]
        wh = data["working_hour"]
        ip = request.remote_addr
        _, err = valid_sid(sid)
        if err:
            return guderr(400, "Sid in invalid")

        cursor.execute(f"SELECT token, working_hour FROM users WHERE sid='{sid}'")
        result = cursor.fetchall()
        whdb = json.loads(result[0][1])
        if len(result) == 0:
            return guderr(400, "user not found")
        tokendb = json.loads(result[0][0])
        if token not in tokendb.values():
            cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'trying to eidt user sid={sid} data but token is unauthorized')")
            db.commit()
            return guderr(400, "token is unauthorized")
        
        if len(wh) < 7:
            for i in wh:
                for j in range(len(whdb)):
                    if whdb[j]["day"] == i["day"]:
                        whdb[j]["hours"] = i["hours"]
                        whdb[j]["busy_hours"] = i["busy_hours"]
            wh = whdb

        cursor.execute(f"UPDATE users SET firstname='{fn}', lastname='{ln}', username='{un}', working_hour='{json.dumps(wh)}' WHERE sid='{sid}'")
        db.commit()

        cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'edit user sid={sid} data')")
        db.commit()
        
        x = {
            "status_code": 200,
            "success": True,
            "message": "Edit user data success"
        }
        return jsonify(x)
    except:
        return guderr(500, "Process error")