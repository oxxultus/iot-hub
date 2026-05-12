from .. import db
from datetime import datetime

class ZigbeeDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friendly_name = db.Column(db.String(100), unique=True, nullable=False) # Zigbee2MQTT에서 설정한 이름
    ieee_address = db.Column(db.String(50), unique=True) # 장치 고유 ID
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    state = db.Column(db.Text) # JSON 형태로 상태 저장 (온도, 배터리 등)

    def __repr__(self):
        return f'<Device {self.friendly_name}>'
