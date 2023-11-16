from route.func.errmaker import errmaker
from route.func.mysql import sql
from flask import request, jsonify
from route.func.validation import valid_sc
import json

def main():
    try:
        data = request.get_json()
        sc = data["secret_code"]
        ip = request.remote_addr

        result, err = valid_sc(sc)
        if err:
            return result
        
        resul, err = sql.sqadd("logs", ["ip", "info"], [ip, f'get user secret_code={sc} calendar'])
        if err:
            return resul
        
        calendar = []
        # get_calendar operations will start here

        x = {
            "status_code": 200,
            "success": True,
            "message": "Get user calendar success",
            "data": {
                "calendar": calendar
            }
        }
        return jsonify(x)
    except Exception as error:
        print("An exception occurred:", error)
        return errmaker(400, "Bad Request")
