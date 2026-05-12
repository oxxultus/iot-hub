import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'it-is-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///iot_hub.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MQTT Settings
    MQTT_BROKER_URL = 'localhost'
    MQTT_BROKER_PORT = 1883
    MQTT_KEEPALIVE = 5
    MQTT_TLS_ENABLED = False
