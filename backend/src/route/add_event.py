from route.func.mysql import cursor, db
from flask import request, jsonify
from route.func.valid_sid import valid_sid
from route.func.errmaker import errmaker

def main():
    try:
        data = request.get_json()
        sid = data["sid"]
        event_title = data["event_title"]
        event_des = data["event_des"]
        event_date = data["event_date"]
        event_color = data["event_color"]
        ip = request.remote_addr
        _, err = valid_sid(sid)
        if err:
            return errmaker(400, "Sid in invalid")
        
        time_start, time_end = event_date[0],event_date[1]
        
        event_start = (f"{time_start[2]}-{time_start[1]:02d}-{time_start[0]:02d} {time_start[3]:02d}:{time_start[4]:02d}:00")
        event_end = (f"{time_end[2]}-{time_end[1]:02d}-{time_end[0]:02d} {time_end[3]:02d}:{time_end[4]:02d}:00")
        
        cursor.execute(f"INSERT INTO {sid}_events (event_title, event_des, event_start, event_end, event_color) VALUES ('{event_title}', '{event_des}', '{event_start}', '{event_end}', '{event_color}')")
        db.commit
        cursor.execute(f"INSERT INTO logs (ip, info) VALUES ('{ip}', 'add event to user sid={sid}')")
        db.commit()

        x = {
                "status_code": 200,
                "success": True,
                "message": "Add event success"
            }
        return jsonify(x)
    except:
        return errmaker(500, "Process error")