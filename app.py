from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.auth import bp as auth_bp
from routes.region import bp as region_bp
from routes.deforestation import bp as deforestation_bp
from routes.youtube import youtube_bp
from routes.land import bp as land_bp
from db import db
from flask_smorest import Api
from flask_cors import CORS
from routes.threats import threats_bp
from routes.recommendations import recommendations_bp

def schema_name_resolver(schema):
    return schema.__class__.__name__
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["API_TITLE"] = "TDMMA API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config[
    "OPENAPI_SWAGGER_UI_URL"
] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deforestation.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1210'

db.init_app(app)
api=Api(app)
migrate=Migrate(app,db)

with app.app_context():
    db.create_all()
    print("Tables created successfully.")


api.register_blueprint(auth_bp)
api.register_blueprint(region_bp)
api.register_blueprint(deforestation_bp)
api.register_blueprint(land_bp)
app.register_blueprint(youtube_bp)
api.register_blueprint(threats_bp)
api.register_blueprint(recommendations_bp)

if __name__ == '__main__':
    app.run(debug=True)
