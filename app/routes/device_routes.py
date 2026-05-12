from flask import Blueprint, request, jsonify
from ..models.device import ZigbeeDevice
from ..services.mqtt_service import send_zigbee_command

device_bp = Blueprint('devices', __name__)

# 장치 리스트 및 최신 상태 조회
@device_bp.route('/list', methods=['GET'])
def get_devices():
    devices = ZigbeeDevice.query.all()
    output = []
    for d in devices:
        output.append({
            "name": d.friendly_name,
            "last_seen": d.last_seen.isoformat(),
            "state": json.loads(d.state) if d.state else {}
        })
    return jsonify(output)

# (기존의 /control 엔드포인트는 그대로 유지)

@device_bp.route('/control', methods=['POST'])
def control_device():
    data = request.json
    device_name = data.get('name')
    state = data.get('state') # ON or OFF
    
    if not device_name or not state:
        return jsonify({"error": "Missing parameters"}), 400
        
    send_zigbee_command(device_name, {"state": state})
    return jsonify({"status": "sent", "device": device_name, "command": state})
