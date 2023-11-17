from route.func.mysql import sqry
from flask import request, jsonify
from route.func.validation import valid_sc
from route.func.gsi import gsi
import json

def main():
    sql = sqry()
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
    temporary = json.loads(result[0][0])
    if len(temporary) > 0:
        for k, v in temporary.items():
            class_list = []
            section = v["section"]
            hell = gsi(k, v["year"], v["semester"], v["studyProgram"])

            # Since ["LECT"] contains a list, we'll need to loop through them
            #if len(hell["class"][section]["LECT"]) > 0:
            for lect in range(0, len(hell["class"][section]["LECT"])):
                # Since ["day"] contains a list, we'll need to loop through them
                for day in hell["class"][section]["LECT"][lect]["day"]:
                    class_each = []
                    class_each.append(day)
                    class_each.append("LECT")
                    class_each.append([hell["class"][section]["LECT"][lect]["building"], hell["class"][section]["LECT"][lect]["Room"]])
                    class_each.append(hell["class"][section]["LECT"][lect]["time"])
                    class_list.append(class_each)

            # Since ["LAB"] contains a list, we'll need to loop through them
            #if len(hell["class"][section]["LAB"]) > 0:
            for lab in range(0, len(hell["class"][section]["LAB"])):
                # Since ["day"] contains a list, we'll need to loop through them
                for day in hell["class"][section]["lab"][lab]["day"]:
                    class_each = []
                    class_each.append(day)
                    class_each.append("LAB")
                    class_each.append([hell["class"][section]["LAB"][lab]["building"], hell["class"][section]["LAB"][lab]["Room"]])
                    class_each.append(hell["class"][section]["LAB"][lab]["time"])
                    class_list.append(class_each)

            # Prepare the dictionary to be appended
            pain = {
                "subject_id": hell["subject_id"],
                "subject_name": hell["subject_name"],
                "midterm_exam": hell["midterm_exam"],
                "final_exam": hell["final_exam"],
                "class": class_list
            }

            sub_list.append(pain)

    x = {
        "status_code": 200,
        "success": True,
        "message": "Get user calendar success",
        "data": {
            "sub_list": sub_list,
            "event_list": event_list
        }
    }
    sql.kill_connect()
    return jsonify(x)
