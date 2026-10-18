import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    from flask import Flask, render_template
    from flask_cors import CORS

    CORS()

    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(
        __name__,
        template_folder=os.path.join(_root, "templates"),
        static_folder=os.path.join(_root, "static"),
    )

    config_file = os.path.join(_root, "config", "default.conf")
    if os.path.exists(config_file):
        import yaml
        with open(config_file) as f:
            config = yaml.safe_load(f)
    else:
        config = {
            "SERVER_NAME": "konfiva.local",
            "SECRET_KEY": "dev-secret-key",
            "DATABASE_URL": "sqlite:///konfiva.db",
            "FTP_ENABLED": True,
            "SFTP_ENABLED": True,
            "TFTP_ENABLED": True,
            "OXIDIZED_ENABLED": True,
            "GIT_ENABLED": True,
            "CLOUD_SYNC": False,
        }

    app.config.update({
        "SECRET_KEY": config.get("SECRET_KEY", "dev-secret-key"),
        "DATABASE_URL": config.get("DATABASE_URL", "sqlite:///konfiva.db"),
        "SQLALCHEMY_DATABASE_URI": config.get("DATABASE_URL", "sqlite:///konfiva.db"),
        "SERVER_NAME": config.get("SERVER_NAME", "konfiva.local"),
    })

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import alerts, api, backup, compare, devices, restore, sync
    app.register_blueprint(devices.bp)
    app.register_blueprint(backup.bp)
    app.register_blueprint(restore.bp)
    app.register_blueprint(compare.bp)
    app.register_blueprint(alerts.bp)
    app.register_blueprint(sync.bp)
    app.register_blueprint(api.bp)

    @app.route("/")
    def dashboard():
        return render_template("index.html")

    @app.route("/devices")
    def devices_page():
        return render_template("devices.html")

    @app.route("/backup")
    def backup_page():
        return render_template("backup.html")

    @app.route("/restore")
    def restore_page():
        return render_template("restore.html")

    @app.route("/compare")
    def compare_page():
        return render_template("compare.html")

    @app.route("/alerts")
    def alerts_page():
        return render_template("alerts.html")

    @app.route("/cloud")
    def sync_page():
        return render_template("cloud.html")

    return app
