from flask import jsonify

def errmaker(code, msg):
    x = {
        "status_code": code,
        "success": False,
        "message": msg,
        "data": {}
    }
    x = jsonify(x)
    x.headers.add('Access-Control-Allow-Origin', '*')
    return x