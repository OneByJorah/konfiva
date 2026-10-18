# INTENT.md — J1-PIPELINE Phase -1 (ORACLE)

**Repository:** `OneByJorah/konfiva`
**Analysis Date:** 2026-07-05
**Analyst:** J1-PIPELINE ORACLE (read-only)
**Status:** Intent Reconstructed

---

## What This System Does

### Technical Role

**konfiva** (package name: `j1-konfiva`, v1.0.0) is a **Network Backup & Asset Management Dashboard** — a Flask-based web application and REST API that serves as a centralized Network Operations Center (NOC) console for managing network device configurations across an enterprise infrastructure.

**Core capabilities:**

| Capability | Description |
|---|---|
| **Device Inventory** | CRUD management of network devices (routers, switches, firewalls, APs) with hostname, IP, OS type, protocol, credentials |
| **Backup Scheduling** | Trigger on-demand or scheduled configuration backups via SSH/SFTP/FTP/TFTP; tracks version, checksum, size, status |
| **Snapshot Comparison** | Line-by-line diff between backup versions with added/removed/changed tracking |
| **Data Restoration** | Restore a device configuration from a specific backup version/commit |
| **Alert Tracking** | Timeline-based alert system with severity levels (info/warning/critical), webhook notifications (Slack, Teams, Discord, Email) |
| **Cloud Sync** | rclone-powered sync to remote storage (S3, Google Drive, OneDrive, Backblaze B2) |
| **Git Integration** | Oxidized-backed config versioning in a local Git repository with commit tracking per device |
| **REST API** | Full `v1` API with token-based auth covering all operations |

### Operational Role

konfiva is the **centralized backup and observability layer** for network infrastructure within the JorahOne ecosystem. It replaces ad-hoc, per-device backup scripts with a unified dashboard that provides:

- **Single pane of glass** for all network device configurations
- **Automated backup lifecycle** — schedule, execute, verify, store, version
- **Change detection** — diff-based alerting when configurations drift
- **Disaster recovery** — one-click restore of known-good configurations
- **Off-site redundancy** — cloud sync for backup portability

---

## Why This Was Built

### The Real Problem

Network engineers managing fleets of heterogeneous devices (Cisco IOS-XE, Juniper JunOS, Arista EOS, Fortinet FortiOS, MikroTik RouterOS, Cisco NX-OS) face a persistent operational challenge:

1. **No single source of truth** — device configs live on individual boxes, scattered across SSH sessions
2. **Manual backup processes** — engineers resort to ad-hoc scripts (`scp`, `expect`, cron jobs) that are fragile, unmonitored, and unaccountable
3. **No change tracking** — when a config changes (intentionally or accidentally), there's no audit trail or diff to identify what changed
4. **Recovery is slow** — restoring a device after failure means finding the last known-good configuration from personal archives or backups
5. **Alerting is absent** — backup failures, config drifts, and certificate expirations go unnoticed until they cause outages

### Why Existing Tools Were Insufficient

| Tool | Limitation |
|---|---|
| **RANCID** | Legacy, Perl-based, no modern web UI, no REST API, complex setup |
| **Oxidized (standalone)** | CLI-only, no dashboard, no alerting, no cloud sync, no multi-protocol backup orchestration |
| **Ansible + cron** | No centralized UI, no diff viewer, no alert timeline, no restore workflow |
| **Vendor-specific tools** (Cisco Prime, Juniper Space) | Single-vendor lock-in, expensive licensing |
| **Commercial NMS** (SolarWinds, PRTG) | Expensive, overkill for config backup, proprietary |

konfiva fills the gap between **heavy commercial NMS** and **fragile shell scripts** — a lightweight, open-source, multi-vendor NOC dashboard purpose-built for configuration backup and recovery.

### What Triggered Development

The initial commit (`accd36b`, 2026-06-15) is titled *"Initial commit: Build complete konfiva NOC platform"* — a **greenfield project** that shipped 27 files and 2,450 lines of code in a single commit. The original README (604 lines) was far more detailed than the current one, including:

- Full Mermaid architecture diagrams showing the system topology
- Detailed setup instructions for FTP (vsftpd), SFTP (OpenSSH), TFTP (tftpd-hpa), and Oxidized
- A complete API reference with 20+ endpoints
- Monitoring and logging instructions
- Security documentation (network security, authentication, encryption)

The original README branded it as **"konfiva NOC"** and described it as *"a comprehensive, open-source Linux-based platform for network configuration backup, file transfer, and device management."* The repo was later renamed from an earlier name to simply "konfiva" and standardized to J1 portfolio conventions.

### JorahOne Ecosystem Fit

konfiva is one of several infrastructure-management tools in the **OneByJorah** organization. It provides the network backup and observability layer for the JorahOne operational tooling stack.

```
JorahOne Ecosystem
├── konfiva          ← Network backup & asset management (this repo)
├── [Other J1 repos]  ← Infrastructure, monitoring, security, automation
```

- **Package name**: `j1-konfiva` (v1.0.0)
- **License**: MIT (originally GPL v3 in initial commit, changed during J1 standardization)
- **J1 standards**: Follows J1 repo template conventions (README, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, GitHub workflows, Dependabot, issue/PR templates)

---

## Operational Classification

**Classification: PRODUCTION**

| Criterion | Assessment |
|---|---|
| **Purpose** | Operational NOC tool for managing network device backups |
| **Maturity** | v1.0.0 — complete feature set with CI, CodeQL, Dependabot, issue templates |
| **Deployment** | Flask app with SQLite (dev) / configurable DB (prod), YAML config, rclone integration |
| **Security** | Token-based API auth, SECURITY.md with disclosure policy, CodeQL scanning, security audit commit in history |
| **CI/CD** | GitHub Actions (test, push, CodeQL), Dependabot (pip/npm/docker/actions) |
| **Documentation** | README, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, issue/PR templates |
| **Risk** | Low — manages backup data, not production traffic; no direct device write access in current code |

**Evidence:**
- v1.0.0 tagged in `setup.py`
- CI pipeline with test, push, and CodeQL workflows
- Dependabot configured for 4 ecosystems
- Security audit commit (`2e1cb37`) sanitizing email references
- Complete community files (CODE_OF_CONDUCT, CONTRIBUTING, SECURITY)
- Issue and PR templates
- `.gitignore` with standard Python/IDE/OS patterns

---

## Key Architectural Decisions

1. **Flask + SQLAlchemy** — Lightweight Python web framework chosen over Django for simplicity; SQLAlchemy provides DB-agnostic storage (SQLite for dev, configurable for prod)

2. **Blueprint-based API structure** — Each domain (devices, backup, restore, compare, alerts, sync) gets its own Flask Blueprint under `/api/v1/`, keeping the codebase modular and testable

3. **YAML configuration** — External `config/default.conf` loaded at startup, with environment variable overrides in `app/config.py` — follows the 12-factor app pattern

4. **Token-based API auth** — Simple Bearer token authentication using the configured `SECRET_KEY`; no session management, no OAuth — appropriate for an internal NOC tool

5. **rclone for cloud sync** — Rather than implementing cloud storage adapters directly, konfiva shells out to `rclone` — a battle-tested tool supporting 40+ storage providers

6. **Oxidized integration** — Rather than building a multi-vendor config parser, konfiva integrates with Oxidized (the de facto standard open-source config collector) via its REST API

7. **Multi-protocol transport** — Supports SSH (paramiko/fabric), FTP/FTPS, SFTP, and TFTP — covering the full range of device access methods found in enterprise networks

8. **Static demo data in templates** — The Jinja2 templates contain hardcoded sample data (device names, backup history, alerts) rather than rendering from the database — indicating this is a functional prototype that needs frontend-backend wiring

---

## Repository Structure

```
konfiva/
├── app/                           # Flask application
│   ├── __init__.py                # App factory with YAML config loading
│   ├── config.py                  # Environment-based configuration (FTP, SFTP, TFTP, Oxidized, Git, Cloud, Notifications)
│   ├── models.py                  # SQLAlchemy models: Device, Backup, Commit, DeviceCommit, Alert
│   └── routes/                    # REST API blueprints (v1)
│       ├── __init__.py            # Blueprint definitions with URL prefixes
│       ├── api.py                 # Root endpoint, health check, config endpoint
│       ├── devices.py             # Device CRUD + per-device backup trigger
│       ├── backup.py              # Backup trigger, schedule management
│       ├── restore.py             # Config restore from backup version
│       ├── compare.py             # Config diff between versions
│       ├── alerts.py              # Alert CRUD + resolution
│       └── sync.py                # rclone cloud sync trigger + status
├── static/
│   └── styles.css                 # NOC-themed CSS (dark navy sidebar, card layout, diff viewer, timeline)
├── templates/                     # Jinja2 templates
│   ├── base.html                  # Layout with sidebar navigation
│   ├── index.html                 # Dashboard with stats cards, recent devices, recent alerts
│   ├── devices.html               # Device inventory table + add device form
│   ├── backup.html                # Backup trigger form + history table + schedules
│   ├── restore.html               # Restore form + restore history table
│   ├── compare.html               # Config diff viewer with summary stats
│   ├── alerts.html                # Alert timeline + webhook configuration
│   └── cloud.html                 # Cloud storage cards + manual sync + sync history
├── config/
│   └── default.conf               # YAML configuration file
├── docs/
│   └── dashboard.png              # Dashboard screenshot
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # CI pipeline (install deps, placeholder tests)
│   │   ├── test.yml               # Test runner (pytest with coverage)
│   │   ├── push.yml               # Auto-commit and push workflow
│   │   └── codeql.yml             # CodeQL security analysis (Python, JS, TS)
│   ├── dependabot.yml             # Dependabot for pip, npm, docker, github-actions
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md          # Bug report template
│   │   └── feature_request.md     # Feature request template
│   └── PULL_REQUEST_TEMPLATE.md   # PR template with checklist
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup (j1-konfiva v1.0.0)
├── README.md                      # Project documentation
├── LICENSE                        # MIT License
├── CODE_OF_CONDUCT.md             # Contributor Covenant v2.1
├── CONTRIBUTING.md                # Contribution guidelines
├── SECURITY.md                    # Security policy with disclosure process
├── .gitignore                     # Python/IDE/OS/DB ignores
└── INTENT.md                      # This file
```

### Data Model

- **Device** — network device with credentials, protocol, backup metadata
- **Backup** — configuration backup version linked to a device
- **Commit** — Git commit record (from Oxidized integration)
- **DeviceCommit** — many-to-many link between devices and commits with per-file diff stats
- **Alert** — event/notification with severity, webhook target, resolution status

### Transport Protocols

- **SSH** (paramiko/fabric) — primary device access
- **FTP** — with SSL support
- **SFTP** — secure file transfer
- **TFTP** — legacy/lightweight transfer
- **Oxidized** — external config collector integration
- **Git** — local version control of configs
- **rclone** — cloud sync (S3, Google Drive, OneDrive, Backblaze B2)

### Notification Channels

- Slack webhook
- Microsoft Teams webhook
- Discord webhook
- Email (SMTP)

---

## Notes

### Discrepancies & Findings

1. **No `app.py` entry point** — The README says `python3 app.py` to run, but no `app.py` exists. The app factory is in `app/__init__.py` via `create_app()`. A run script or `flask run` is needed.

2. **Dependabot ecosystem mismatch** — Dependabot is configured for `npm` and `docker` ecosystems, but there is no `package.json` or `Dockerfile` in the repo. This is a template vestige from the J1 repo template.

3. **CodeQL language mismatch** — CodeQL workflow scans for `javascript` and `typescript` languages, but there are no JS/TS files in the repo. Only Python is relevant.

4. **License change** — The initial commit used GPL v3; the current LICENSE is MIT. This was changed during J1 portfolio standardization.

5. **Repo rename** — The initial commit branded it as "konfiva NOC" with a repo URL referencing `konfiva-NOC`. It was later renamed to just `konfiva` and the README was simplified from 604 lines to 81 lines.

6. **Hardcoded demo data in templates** — All Jinja2 templates contain static sample data (device names, backup history, alert entries) rather than rendering from the database. The frontend is a static mockup that needs to be wired to the API.

7. **`compare.py` has demo fallback** — The `load_config()` function returns a hardcoded sample config with a comment "In production, this would read from the actual backup file. For demo, return a sample config." This is demo/placeholder code in a production-classified repo.

8. **`push.yml` workflow** — Contains a hardcoded email (`admin@konfiva.local`) and an auto-commit-and-push pattern that could cause issues. The latest commit (`2e1cb37`) sanitized email references.

9. **No test files found** — The `test.yml` workflow runs `pytest --cov=app`, but no test files exist in the repo. Tests would all pass with 0% coverage.

10. **No Dockerfile or compose file** — Despite Dependabot being configured for Docker, there are no containerization files. Deployment is bare-metal Python.

11. **No `j1.yaml`** — The J1-PIPELINE expects a `j1.yaml` at repo root for project classification and scoring metadata. This file is absent.

---

*This document was produced by J1-PIPELINE Phase -1 (ORACLE) — read-only analysis. No code was modified.*
