import os

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_migrate import init as migrate_init
from flask_migrate import migrate as migrate_migrate
from flask_migrate import upgrade as migrate_upgrade
from flask_cors import CORS
import app.config as config
from app.repository.database import init_database
from app.custom_api import CustomApi
from prometheus_flask_exporter import RESTfulPrometheusMetrics


app = Flask(__name__)
app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


cors = CORS(app, resources={r"/*": {"origins": "localhost"}})

api = CustomApi(app)
db = init_database(app)
metrics = RESTfulPrometheusMetrics(app, api)

from app.rbac import rbac
rbac.setJWTManager(app)

@app.route('/')
def hello():
    return jsonify({'message': 'Hello world'})


migrate = Migrate(app, db)

from app.prometheus_metrics.prometheus_metrics import (
    init_metrics,
)

init_metrics()

@api.representation("application/octet-stream")
def output_stream(data, code, headers=None):
    """Makes a Flask response with a bytes body"""
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp

def db_migrate():
    with app.app_context():
        if not os.path.exists("./migrations"):
            migrate_init()
        migrate_migrate()
        migrate_upgrade()


def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
