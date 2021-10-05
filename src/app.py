from flask import Flask
from services.RutasPlayer import rutas_player
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(rutas_player)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
