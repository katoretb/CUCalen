from route.func.encrypt import encrypt_string
from route.func.errmaker import errmaker
from flask import request, jsonify

def main():
    try:
        x = {
            "status_code": 200,
            "success": True,
            "message": "hash success",
            "data": {
                "hash": encrypt_string(request.get_json()['str'])
            }
        }
        return jsonify(x)
    except Exception as error:
        print("An exception occurred:", error)
        return errmaker(400, "Bad Request")