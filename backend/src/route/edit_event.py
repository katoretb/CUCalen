from route.func.mysql import sqry
from flask import request, jsonify
from route.func.validation import valid_sid, valid_token

def main():
    sql = sqry()
    data = request.get_json()
    sid = data["sid"]
    token = data["token"]
    event_id = data["event_id"]
    event_title = data["event_title"]
    event_des = data["event_des"]
    event_date = data["event_date"]
    event_color = data["event_color"]
    ip = request.remote_addr
    msg, err = valid_sid(sid, sql)
    if err:
        return msg

    msg, err = valid_token(ip, sid, token, "edit event", sql)
    if err:
        return msg
    
    d = {
        'event_title': f"'{event_title}'",
        'event_des': f"'{event_des}'",
        'event_start': f"'{event_date[0].replace('T', ' ')}'",
        'event_end': f"'{event_date[1].replace('T', ' ')}'",
        'event_color': f"'{event_color}'"
    }
    result, err = sql.squpd(f"{sid}_events", d, f"id='{event_id}'")
    if err:
        return result

    result, err = sql.sqadd("logs", ["ip", "info"], [ip, f'edit event to user sid={sid} where id={event_id}'])
    if err:
        return result

    x = {
        "status_code": 200,
        "success": True,
        "message": "Edit event success"
    }
    sql.kill_connect()
    return jsonify(x)