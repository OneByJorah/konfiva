from datetime import datetime
from functools import wraps
from flask import Blueprint, jsonify, request

from app import db
from app.config import SECRET_KEY
from app.models import Backup, Device

bp = Blueprint("backup", __name__, url_prefix="/api/v1/backup")

def token_required(f):
    @wraps(f)
    def decorated_backup(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token or token != SECRET_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_backup

@bp.route("/", methods=["POST"])
@token_required
def trigger_backup():
    data = request.get_json()
    device_name = data.get("device")
    mode = data.get("mode", "full")

    device = Device.query.filter_by(name=device_name).first_or_404()

    if mode == "full":
        config = f"/var/lib/konfiva/backup/{device.name}_running.conf"
    else:
        config = f"/var/lib/konfiva/backup/{device.name}_startup.conf"

    backup = Backup(
        device_id=device.id,
        version=f"{mode}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        config_file=config,
        size=0,
        checksum="",
        status="running",
    )
    device.backup_count = (device.backup_count or 0) + 1
    device.last_backup = datetime.now()
    db.session.add(backup)
    db.session.commit()

    return jsonify({"message": f"Backup initiated for {device.name}", "version": backup.version}), 201

@bp.route("/schedule", methods=["GET"])
@token_required
def list_schedules():
    return jsonify({
        "schedules": [
            {"name": "daily", "interval": "24h", "enabled": True},
            {"name": "weekly", "interval": "7d", "enabled": True},
            {"name": "monthly", "interval": "30d", "enabled": False},
        ],
    })

@bp.route("/schedule", methods=["POST"])
@token_required
def create_schedule():
    data = request.get_json()
    name = data.get("name")
    interval = data.get("interval")
    enabled = data.get("enabled", True)

    return jsonify({
        "message": f"Schedule {name} created",
        "name": name,
        "interval": interval,
        "enabled": enabled,
    }), 201

@bp.route("/schedule/<int:schedule_id>", methods=["DELETE"])
@token_required
def delete_schedule(schedule_id):
    return jsonify({"message": f"Schedule {schedule_id} deleted"}), 200
