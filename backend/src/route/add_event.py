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
        events = data["events"]
        ip = request.remote_addr
        msg, err = valid_sid(sid)
        if err:
            return msg
        
        msg, err = valid_token(ip, sid, token, "get user", sql)
        if err:
            return msg
        
        for i in range(len(events)):
            result, err = sql.sqadd(f"{sid}_events", ["event_title", "event_des", "event_start", "event_end", "event_color"], [f'{events[i]["event_title"]}', f'{events[i]["event_des"]}', f'{events[i]["event_date"][0].replace("T", " ")}', f'{events[i]["event_date"][1].replace("T", " ")}', f'{events[i]["event_color"]}'])
            if err:
                return result

        result, err = sql.sqadd("logs", ["ip", "info"], [ip, f'add event to user sid={sid}'])
        if err:
            return result

        x = {
            "status_code": 200,
            "success": True,
            "message": "Add event success"
        }
        sql.kill_connect()
        return jsonify(x)
    except Exception as error:
        print(error, file=sys.stderr)
        return errmaker(500, f'Please contact owner')