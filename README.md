<div align="center">

![konfiva banner](docs/assets/banner.svg)

# konfiva

**Formerly ConfigVault.**  
*The self-hosted network configuration backup and asset manager for small NOC teams — inventory devices, schedule backups, diff snapshots, and sync to cloud storage.*

<a href="https://github.com/OneByJorah/konfiva/stargazers"><img src="https://img.shields.io/github/stars/OneByJorah/konfiva?style=flat-square" alt="Stars"></a>
<a href="https://github.com/OneByJorah/konfiva/commits"><img src="https://img.shields.io/github/last-commit/OneByJorah/konfiva?style=flat-square" alt="Last commit"></a>
<a href="https://github.com/OneByJorah/konfiva/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/OneByJorah/konfiva/ci.yml?branch=main&style=flat-square" alt="CI"></a>
<a href="https://github.com/OneByJorah/konfiva/pkgs/container/konfiva"><img src="https://img.shields.io/badge/GHCR-ghcr.io%2Fonebyjorah%2Fkonfiva%3Alatest-blue?style=flat-square" alt="GHCR image"></a>
<img src="https://img.shields.io/github/license/OneByJorah/konfiva?style=flat-square" alt="License">
<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+">
<img src="https://img.shields.io/badge/Flask-3-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask 3">
<img src="https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat-square" alt="SQLAlchemy 2.0">

</div>

![konfiva dashboard](docs/screenshots/dashboard.png)

## Why This Exists

konfiva gives small network teams a lightweight, self-hosted alternative to heavyweight NMS suites for one job done well: keeping router, switch, firewall, and AP configurations backed up and auditable. It inventories devices, stores every snapshot with a checksum, and shows side-by-side diffs between versions.

Everything runs from a single Flask process with SQLite by default — no database server, no cloud lock-in, and optional rclone sync to S3, Google Drive, OneDrive, B2, or Dropbox. The demo data below is fake; all screenshots were captured from a local stack with placeholder devices.

## Quick Start

```bash
git clone https://github.com/OneByJorah/konfiva.git
cd konfiva
cp .env.example .env      # set SECRET_KEY before production use
docker compose up -d --build
```

Open **http://127.0.0.1:8103**.

> [!NOTE]
> `docker compose` mounts `./instance` for the SQLite database and `./configs` for git-backed history. To run without Docker, use `./install.sh` then `python app.py`.

## Features

- **Device inventory** — track routers, switches, firewalls, and APs with hostname, IP, OS type, protocol, and port.
- **Scheduled & on-demand backups** — trigger backups per device or list/create schedules through the API; history is git-backed.
- **Snapshot diff** — compare any two config versions to see added, removed, and changed lines.
- **Config restore** — roll a device back to a historical backup commit.
- **Alert engine** — Slack, Microsoft Teams, Discord, and email webhook notifications.
- **Optional cloud sync** — rclone integration for S3, Google Drive, OneDrive, B2, and Dropbox (off by default).
- **Protocol integrations** — FTP, SFTP, TFTP, and Oxidized hooks (all disabled by default for safer deployments).
- **Dark NOC UI** — Jinja2 templates with a responsive dashboard for devices, backups, restores, compares, alerts, and cloud sync.

## Screenshots

| Dashboard | Devices | Backup |
|---|---|---|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Devices](docs/screenshots/devices.png) | ![Backup](docs/screenshots/backup.png) |

More captures live in [`docs/screenshots/`](docs/screenshots/).

## Architecture

```mermaid
flowchart LR
    Browser -->|HTTP :8103| Flask["Flask NOC UI\nPort 8103"]
    Flask -->|SQLAlchemy| DB[("SQLite / PostgreSQL")]
    Flask -->|Paramiko| SSH["SSH/SFTP\nNetwork devices"]
    Flask -->|rclone| Cloud["S3 / GDrive / B2 / O365"]
    Flask --> Webhooks["Slack / Teams / Discord / Email"]
```

## Configuration

konfiva reads environment variables first, then falls back to `config/default.conf`.

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///instance/konfiva.db` | SQLAlchemy database URI |
| `SERVER_NAME` | `konfiva.local` | Server hostname |
| `SECRET_KEY` | `<set-value>` | Flask secret + API bearer token — **change this** |
| `FTP_ENABLED` | `false` | Enable FTP backup target |
| `SFTP_ENABLED` | `false` | Enable SFTP backup target |
| `TFTP_ENABLED` | `false` | Enable TFTP backup target |
| `OXIDIZED_ENABLED` | `false` | Enable Oxidized integration |
| `GIT_ENABLED` | `true` | Git-backed config history |
| `CLOUD_SYNC` | `false` | Enable rclone cloud sync |
| `SLACK_WEBHOOK` / `TEAMS_WEBHOOK` / `DISCORD_WEBHOOK` | — | Notification webhooks |
| `EMAIL_ENABLED` / `EMAIL_SERVER` | `false` / — | Email notification settings |

> [!WARNING]
> Write endpoints are protected by a shared bearer token equal to `SECRET_KEY`. Set a strong value and never commit real credentials to git.

## API Endpoints

All routes are prefixed `/api/v1`. Write operations require an `Authorization: Bearer <SECRET_KEY>` header.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/config` | GET | App configuration summary |
| `/api/v1/devices` | GET/POST | List / add devices |
| `/api/v1/devices/{id}` | GET/PUT/DELETE | Read, update, or remove a device |
| `/api/v1/devices/{id}/backup` | POST | Trigger a device backup |
| `/api/v1/backup` | POST | Start a backup run |
| `/api/v1/backup/schedule` | GET/POST | List or create schedules |
| `/api/v1/backup/schedule/{id}` | DELETE | Remove a schedule |
| `/api/v1/restore` | POST | Restore a config version |
| `/api/v1/restore/{commit_id}` | GET | Inspect a restore commit |
| `/api/v1/compare` | POST | Diff two snapshots |
| `/api/v1/alerts` | GET/POST | List or create alerts |
| `/api/v1/alerts/{id}` | GET/DELETE | Read or delete an alert |
| `/api/v1/sync` | POST | Push backups to cloud storage |
| `/api/v1/sync/status` | GET | Cloud sync status |

## Use Cases

1. **Small NOCs** — replace ad-hoc TFTP/FTP backup scripts with a tracked, auditable inventory.
2. **MSPs** — keep per-client device configs versioned and diffable before change windows.
3. **Compliance** — retain restore points with checksums and push them off-box to cloud storage.

## Tech Stack

Python 3.11, Flask 3, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS, Paramiko, PyYAML, SQLite/PostgreSQL, rclone, Docker Compose.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). [Open an issue](https://github.com/OneByJorah/konfiva/issues) to report a bug or request a feature.

## Security

See [SECURITY.md](SECURITY.md). If you discover a sensitive issue, please open a private advisory rather than a public issue.

## License

MIT — see [LICENSE](LICENSE).

## Connect

- [jorahone.com](https://jorahone.com)
- [GitHub Org](https://github.com/OneByJorah)
- [info@jorahone.com](mailto:info@jorahone.com)
