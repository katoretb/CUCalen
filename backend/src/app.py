from flask import app, Flask, Response
from flask_cors import CORS
from os import listdir
from importlib import import_module

#list route file
list_route = [i.replace(".py", "") for i in listdir('route') if i.endswith(".py")]

#loop import route
gbl = globals()
for i in list_route:
    gbl["route."+i] = import_module("route."+i)

#init api server
app = Flask(__name__)
CORS(app)

#add route to /
@app.route('/')
def index():
    return Response("I'm a teapot so I sent 418 error.", status=418, mimetype='application/json')

#loop add route to api server
for i in gbl['list_route']:
    app.add_url_rule('/'+i, i, gbl["route." + i].main, methods=['POST'])
    print(i,"has been mounted to server")

#start api server
if __name__ == "__main__":
    app.run(debug=False, port=5000)

