from route.func.errmaker import errmaker
from route.func.mysql import sqry
from flask import request, jsonify
from route.func.validation import valid_sid, valid_token
import sys

def main():
    try:
        sql = sqry()
        data = request.get_json()
        sid = data["sid"]
        token = data["token"]
        event_id = data["event_id"]
        ip = request.remote_addr
        msg, err = valid_sid(sid)
        if err:
            return msg

        msg, err = valid_token(ip, sid, token, "delete event", sql)
        if err:
            return msg
        
        result, err = sql.sqdel(f"{sid}_events", f"id='{event_id}'")
        if err:
            return result

        result, err = sql.sqadd("logs", ["ip", "info"], [ip, f'delete event to user sid={sid} where id={event_id}'])
        if err:
            return result

        x = {
            "status_code": 200,
            "success": True,
            "message": "Delete event success"
        }
        sql.kill_connect()
        return jsonify(x)
    except Exception as error:
        print(error, file=sys.stderr)
        return errmaker(500, f'Please contact owner')