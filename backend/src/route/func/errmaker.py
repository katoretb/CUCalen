from flask import jsonify

def errmaker(code, msg):
    x = {
        "status_code": code,
        "success": False,
        "message": msg,
        "data": {}
    }
    return jsonify(x)