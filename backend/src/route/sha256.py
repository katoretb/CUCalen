from route.func.errmaker import errmaker
from route.func.encrypt import encrypt_string
from flask import request, jsonify
import sys

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
        print(error, file=sys.stderr)
        return errmaker(500, f'Please contact owner')