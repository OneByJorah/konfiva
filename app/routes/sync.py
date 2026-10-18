import subprocess

from functools import wraps
from flask import Blueprint, jsonify, request

from app.config import CLOUD_SYNC, RCLONE_CONFIG, SECRET_KEY

# Allowed cloud types for rclone sync
ALLOWED_CLOUD_TYPES = {"s3", "gdrive", "onedrive", "b2", "dropbox"}

bp = Blueprint("sync", __name__, url_prefix="/api/v1/sync")

def token_required(f):
    @wraps(f)
    def decorated_sync(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token or token != SECRET_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_sync

@bp.route("/", methods=["POST"])
@token_required
def trigger_sync():
    if not CLOUD_SYNC:
        return jsonify({"error": "Cloud sync is disabled"}), 503

    data = request.get_json() or {}
    remote_path = data.get("remote_path", "/var/lib/konfiva/backup")
    cloud_type = data.get("cloud_type", "s3")
    cloud_path = data.get("cloud_path", "")

    # Validate cloud_type against allowed list to prevent command injection
    if cloud_type not in ALLOWED_CLOUD_TYPES:
        return jsonify({"error": f"Invalid cloud type: {cloud_type}"}), 400

    # Validate cloud_path: only allow safe characters
    if not all(c.isalnum() or c in "/_-." for c in cloud_path):
        return jsonify({"error": "Invalid cloud path characters"}), 400

    # Validate remote_path: only allow safe characters
    if not all(c.isalnum() or c in "/_-." for c in remote_path):
        return jsonify({"error": "Invalid remote path characters"}), 400

    try:
        # Run rclone sync
        cmd = [
            "rclone",
            "sync",
            remote_path,
            f"{cloud_type}:{cloud_path}",
            "--progress",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            return jsonify({
                "message": "Cloud sync completed successfully",
                "remote_path": remote_path,
                "cloud_type": cloud_type,
                "cloud_path": cloud_path,
            }), 200
        else:
            return jsonify({
                "error": "Cloud sync failed",
                "details": result.stderr,
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Cloud sync timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/status", methods=["GET"])
@token_required
def get_sync_status():
    # In production, check rclone status
    return jsonify({
        "status": "ready",
        "config": RCLONE_CONFIG,
        "cloud_sync": CLOUD_SYNC,
    })
