from flask_sqlalchemy import SQLAlchemy
import app.config as config

db = None


def init_database(app):
    global db
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{config.SQL_USERNAME}:{config.SQL_PASSWORD}@"
        f"{config.SQL_HOST}:{config.SQL_PORT}/{config.SQL_DB_NAME}"
    )
    db = SQLAlchemy(app)
    return db
