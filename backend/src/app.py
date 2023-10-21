from flask import *
app = Flask(__name__)

@app.route('/')
def index():
    return Response("I'm not a teapot so I sent 418 error.", status=418, mimetype='application/json')

@app.route('/test', methods = ['POST'])
def test():
    print(request.form)
    return "request.form"


if __name__ == "__main__":
    app.run(debug=True, port=3000)