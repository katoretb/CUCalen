from route.func.errmaker import errmaker
from route.func.mysql import sql
from flask import request, jsonify
from route.func.validation import valid_sc

def main():
    try:
        data = request.get_json()
        sc = data["secret_code"]
        ip = request.remote_addr

        result, err = valid_sc(sc)
        if err:
            return result
        
        sid = result[0][1]

        resul, err = sql.sqadd("logs", ["ip", "info"], [ip, f'get user sid={sid} event'])
        if err:
            return resul
        
        result, err = sql.sqsel(f"{sid}_events", ["id", "event_title", "event_des", "event_start", "event_end", "event_color"])
        if err:
            return result
        
        el = []

        if len(result) > 0:
            for i in result:
                e = {
                    "event_id": int(i[0]),
                    "event_title": i[1],
                    "event_des": i[2],
                    "event_date": [
                        str(i[3]).replace(" ", "T"),
                        str(i[4]).replace(" ", "T")
                    ],
                    "event_color": i[5]
                }
                el.append(e)

        x = {
            "status_code": 200,
            "success": True,
            "message": "Get user dubjects success",
            "data": {
                "subjects": el
            }
        }
        x = jsonify(x)
        x.headers.add('Access-Control-Allow-Origin', '*')
        return x
    except:
        return errmaker(400, "Bad Request")