from route.func.errmaker import errmaker
from route.func.mysql import sql
from flask import request, jsonify
from route.func.validation import valid_sid, valid_token
import json

def main():
    # try:
    data = request.get_json()
    sid = data["sid"]
    token = data["token"]
    subjects = data["subjects"]
    ip = request.remote_addr
    msg, err = valid_sid(sid)
    if err:
        return msg

    msg, err = valid_token(ip, sid, token, "edit subject")
    if err:
        return msg
    
    subjs = {}
    if len(subjects) > 0:
        for i in subjects:
            subjs[int(i["courseno"])] = {
                "year": int(i["year"]),
                "semester": int(i["semester"]),
                "studyProgram": i["studyProgram"],
                "section": int(i["section"])
            }

    result, err = sql.squpd("users", {"subjects": f"'{json.dumps(subjs)}'"}, f"sid='{sid}'")
    if err:
        return result
    
    msg, err = sql.sqadd("logs", ["ip", "info"], [ip, f'edit user sid={sid} subjects'])
    if err:
        return msg
    

    x = {
        "status_code": 200,
        "success": True,
        "message": "Edit user dubjects success"
    }
    return jsonify(x)
    # except Exception as error:
    #     print("An exception occurred:", error)
    #     return errmaker(400, "Bad Request")