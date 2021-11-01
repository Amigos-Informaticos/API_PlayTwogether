from datetime import timedelta
from flask import Flask
from services.RutasPlayer import rutas_player
from flask_cors import CORS
from services.GameRoutes import game_routes

app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(rutas_player)
app.register_blueprint(game_routes)
app.config["SECRET_KEY"] = "beethoven"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=120)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
