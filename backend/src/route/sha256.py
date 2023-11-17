from route.func.encrypt import encrypt_string
from flask import request, jsonify

def main():
    x = {
        "status_code": 200,
        "success": True,
        "message": "hash success",
        "data": {
            "hash": encrypt_string(request.get_json()['str'])
        }
    }
    return jsonify(x)