from functools import wraps
from flask import Blueprint, jsonify, request

from app.config import SECRET_KEY

bp = Blueprint("api", __name__, url_prefix="/api/v1")

def token_required(f):
    @wraps(f)
    def decorated_api(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token or token != SECRET_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_api

@bp.route("/")
@token_required
def api_root():
    return jsonify({
        "service": "konfiva NOC API",
        "version": "1.0.0",
        "endpoints": {
            "devices": "/api/v1/devices",
            "backup": "/api/v1/backup",
            "restore": "/api/v1/restore",
            "compare": "/api/v1/compare",
            "alerts": "/api/v1/alerts",
            "sync": "/api/v1/sync",
        },
    })

@bp.route("/health")
def health():
    return jsonify({"status": "healthy"})

@bp.route("/config", methods=["GET"])
@token_required
def get_config():
    from app import config as config_module
    return jsonify({
        "server_name": config_module.SERVER_NAME,
        "ftp_enabled": config_module.FTP_ENABLED,
        "sftp_enabled": config_module.SFTP_ENABLED,
        "tftp_enabled": config_module.TFTP_ENABLED,
        "oxidized_enabled": config_module.OXIDIZED_ENABLED,
        "git_enabled": config_module.GIT_ENABLED,
        "cloud_sync": config_module.CLOUD_SYNC,
    })
