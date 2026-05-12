from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # 현재 패키지(app) 내에서 가져오기 위해 점(.) 사용
        from .services.mqtt_service import init_mqtt
        from .routes.device_routes import device_bp
        
        init_mqtt(app)
        app.register_blueprint(device_bp, url_prefix='/api')
        
        db.create_all()

    return app
