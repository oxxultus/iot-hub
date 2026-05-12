import json
from datetime import datetime
from flask_mqtt import Mqtt
from ..models.device import ZigbeeDevice # app.models.device 대신 상대 경로 사용
from .. import db # app 대신 상대 경로 사용

mqtt = Mqtt()

def init_mqtt(app):
    mqtt.init_app(app)

    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        # Zigbee2MQTT의 모든 토픽 구독
        mqtt.subscribe('zigbee2mqtt/#')
        print("Connected to MQTT Broker and subscribed to Zigbee2MQTT")

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        topic = message.topic
        payload = message.payload.decode()
        
        # 브릿지 메시지나 set 명령 토픽은 무시
        if 'bridge' in topic or '/set' in topic:
            return

        # 토픽에서 장치 이름 추출
        friendly_name = topic.replace('zigbee2mqtt/', '')
        
        # Flask 컨텍스트를 사용하여 DB 업데이트
        with app.app_context():
            try:
                # payload가 JSON인 경우만 처리
                data = json.loads(payload)
                
                device = ZigbeeDevice.query.filter_by(friendly_name=friendly_name).first()
                if not device:
                    device = ZigbeeDevice(friendly_name=friendly_name)
                    db.session.add(device)
                
                device.state = payload
                device.last_seen = datetime.utcnow()
                db.session.commit()
                print(f"[{datetime.now()}] Updated {friendly_name} state in DB")
            except Exception as e:
                # 단순 문자열 payload 처리 또는 에러 로그
                print(f"Message on {topic}: {payload} (Non-JSON or Error: {e})")

def send_zigbee_command(device_friendly_name, command):
    """
    지그비 장치에 명령을 내립니다.
    command 예시: {"state": "ON"}
    """
    topic = f'zigbee2mqtt/{device_friendly_name}/set'
    mqtt.publish(topic, json.dumps(command))
