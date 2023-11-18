from flask import request, jsonify
import json
import sys

from route.func.errmaker import errmaker
from route.func.mysql import sqry
from route.func.validation import valid_sid, valid_token
from route.func.gsi import gsi

def main():
    try:
        sql = sqry()
        data = request.get_json()
        sid = data["sid"]
        token = data["token"]
        subjects = data["subjects"]
        ip = request.remote_addr
        msg, err = valid_sid(sid)
        if err:
            return msg

        msg, err = valid_token(ip, sid, token, "edit subject", sql)
        if err:
            return msg
        
        subjs = {}
        if len(subjects) > 0:
            for i in subjects:
                d, err = gsi(i["courseno"], int(i["year"]), int(i["semester"]), i["studyProgram"])
                if err:
                    return errmaker(400, f"{i['courseno']} not found or reg cu server down")
                if len(d['class'] < int(i["section"])):
                    return errmaker(400, f"{i['courseno']} doesn't have section {i['section']}")
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
        sql.kill_connect()
        return jsonify(x)
    except Exception as error:
        print(error, file=sys.stderr)
        return errmaker(500, f'Please contact owner')