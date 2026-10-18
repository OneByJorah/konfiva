"""Configuration settings for konfiva NOC."""

import os

# Server
SERVER_NAME = os.getenv("SERVER_NAME", "konfiva.local")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///konfiva.db")

# FTP
FTP_ENABLED = os.getenv("FTP_ENABLED", "true").lower() == "true"
FTP_HOST = os.getenv("FTP_HOST", "127.0.0.1")
FTP_PORT = int(os.getenv("FTP_PORT", "21"))
FTP_USER = os.getenv("FTP_USER", "konfiva")
FTP_PASS = os.getenv("FTP_PASS", "")
FTP_SSL = os.getenv("FTP_SSL", "true").lower() == "true"

# SFTP
SFTP_ENABLED = os.getenv("SFTP_ENABLED", "true").lower() == "true"
SFTP_HOST = os.getenv("SFTP_HOST", "127.0.0.1")
SFTP_PORT = int(os.getenv("SFTP_PORT", "22"))

# TFTP
TFTP_ENABLED = os.getenv("TFTP_ENABLED", "true").lower() == "true"
TFTP_HOST = os.getenv("TFTP_HOST", "127.0.0.1")
TFTP_PORT = int(os.getenv("TFTP_PORT", "69"))
TFTP_ROOT = os.getenv("TFTP_ROOT", "/var/lib/konfiva/tftp")

# Oxidized
OXIDIZED_ENABLED = os.getenv("OXIDIZED_ENABLED", "true").lower() == "true"
OXIDIZED_URL = os.getenv("OXIDIZED_URL", "http://localhost:8080")
OXIDIZED_API_KEY = os.getenv("OXIDIZED_API_KEY", "")

# Git
GIT_ENABLED = os.getenv("GIT_ENABLED", "true").lower() == "true"
GIT_REPO = os.getenv("GIT_REPO", "/var/lib/konfiva/configs")
GIT_BRANCH = os.getenv("GIT_BRANCH", "main")

# Cloud Sync
CLOUD_SYNC = os.getenv("CLOUD_SYNC", "false").lower() == "true"
RCLONE_CONFIG = os.getenv("RCLONE_CONFIG", "/etc/konfiva/rclone.conf")

# Notifications
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "")
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK", "")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
EMAIL_SERVER = os.getenv("EMAIL_SERVER", "")
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASS = os.getenv("EMAIL_PASS", "")
