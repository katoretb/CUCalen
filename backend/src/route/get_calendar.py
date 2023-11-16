from route.func.errmaker import errmaker
from route.func.mysql import sql
from flask import request, jsonify
from route.func.validation import valid_sc
from route.func.gsi import gsi
import json

def main():
    try:
        data = request.get_json()
        sc = data["secret_code"]
        ip = request.remote_addr

        result, err = valid_sc(sc)
        if err:
            return result

        sid = result[0][1]
        
        resul, err = sql.sqadd("logs", ["ip", "info"], [ip, f'get user secret_code={sc} calendar'])
        if err:
            return resul

        result_event, err = sql.sqsel(f"{sid}_events", ["id", "event_title", "event_des", "event_start", "event_end", "event_color"])
        if err:
            return result_event

        # get_event operations will happen here
        event_list = []
        if len(result_event) > 0:
            for i in result_event:
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
                event_list.append(e)
        
        # get_subject operations will happen here
        sub_list = []
        subname_list = []
        temporary = json.loads(result[0][0])
        if len(temporary) > 0:
            for k, v in temporary.items():
                e = {
                    "courseno": k,
                    "year": v["year"],
                    "semester": v["semester"],
                    "studyProgram": v["studyProgram"],
                    "section": v["section"]
                }
                subname_list.append(e)
                section = v["section"]
                result_gsi = gsi(k, v["year"], v["semester"], v["studyprogram"])

        x = {
            "status_code": 200,
            "success": True,
            "message": "Get user calendar success",
            "data": {
                "sub_list": sub_list,
                "event_list": event_list
            }
        }
        return jsonify(x)
    except Exception as error:
        print("An exception occurred:", error)
        return errmaker(400, "Bad Request")
