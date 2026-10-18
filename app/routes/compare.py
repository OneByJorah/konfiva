from functools import wraps
from flask import Blueprint, jsonify, request

from app.config import SECRET_KEY

bp = Blueprint("compare", __name__, url_prefix="/api/v1/compare")

def token_required(f):
    @wraps(f)
    def decorated_compare(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token or token != SECRET_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_compare

@bp.route("/", methods=["POST"])
@token_required
def compare_configs():
    data = request.get_json()
    base = data.get("base")
    compare = data.get("compare")

    # Load configs from backup files
    base_config = load_config(base) if base else {}
    compare_config = load_config(compare) if compare else {}

    diff = diff_configs(base_config, compare_config)

    return jsonify({
        "base": base,
        "compare": compare,
        "diff": {
            "added": diff["added"],
            "removed": diff["removed"],
            "changed": diff["changed"],
            "lines": diff["lines"],
        },
        "base_changes": diff["base_changes"],
        "compare_changes": diff["compare_changes"],
    })

def load_config(version):
    """Load config from backup file."""
    # In production, this would read from the actual backup file
    # For demo, return a sample config
    return {
        "hostname": "router-1",
        "interface": "GigabitEthernet0/0",
        "ip_address": "192.0.2.1",
        "subnet_mask": "255.255.255.0",
        "description": "Main router",
    }

def diff_configs(base, compare):
    """Compare two configs and return diff."""
    base_lines = str(base).split("\n") if isinstance(base, str) else []
    compare_lines = str(compare).split("\n") if isinstance(compare, str) else []

    diff = {
        "added": 0,
        "removed": 0,
        "changed": 0,
        "lines": [],
        "base_changes": [],
        "compare_changes": [],
    }

    # Simple line comparison
    for i, (b_line, c_line) in enumerate(zip(base_lines, compare_lines)):
        if b_line != c_line:
            if b_line and not c_line:
                diff["removed"] += 1
                diff["lines"].append({"line": i, "type": "removed", "base": b_line})
            elif c_line and not b_line:
                diff["added"] += 1
                diff["lines"].append({"line": i, "type": "added", "compare": c_line})
            else:
                diff["changed"] += 1
                diff["lines"].append({"line": i, "type": "changed", "base": b_line, "compare": c_line})

    # Handle length differences
    if len(base_lines) < len(compare_lines):
        for i in range(len(base_lines), len(compare_lines)):
            diff["added"] += 1
            diff["lines"].append({"line": i, "type": "added", "compare": compare_lines[i]})
    elif len(base_lines) > len(compare_lines):
        for i in range(len(compare_lines), len(base_lines)):
            diff["removed"] += 1
            diff["lines"].append({"line": i, "type": "removed", "base": base_lines[i]})

    return diff
