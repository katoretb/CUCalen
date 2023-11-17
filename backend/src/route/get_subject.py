from route.func.errmaker import errmaker
from route.func.mysql import sqry
from flask import request, jsonify
from route.func.validation import valid_sc
import json

def main():
    try:
        sql = sqry()
        data = request.get_json()
        sc = data["secret_code"]
        ip = request.remote_addr

        result, err = valid_sc(sc)
        if err:
            return result
        
        resul, err = sql.sqadd("logs", ["ip", "info"], [ip, f'get user secret_code={sc} subjects'])
        if err:
            return resul
        
        subjs = []
        temp = json.loads(result[0][0])
        if len(temp) > 0:
            for k, v in temp.items():
                e = {
                    "courseno": k,
                    "year": v["year"],
                    "semester": v["semester"],
                    "studyProgram": v["studyProgram"],
                    "section": v["section"]
                }
                subjs.append(e)

        x = {
            "status_code": 200,
            "success": True,
            "message": "Get user subjects success",
            "data": {
                "subjects": subjs
            }
        }
        sql.kill_connect()
        return jsonify(x)
    except Exception as error:
        print("An exception occurred:", error)
        return errmaker(400, "Bad Request")
