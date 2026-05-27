# Free Tools Architecture — VSCode Stimulator Enterprise

This document explains the free/open-source architecture.

## 1. Frontend

| Layer | Tool | Cost |
|---|---|---|
| UI | HTML/CSS/Vanilla JavaScript | Free |
| Code editor | CodeMirror 5 | Free/open-source |
| Charts | Chart.js | Free/open-source |
| Markdown rendering | marked.js | Free/open-source |
| Realtime client | Socket.IO client | Free/open-source |
| PWA | manifest + service worker | Free |

## 2. Backend

| Layer | Tool | Cost |
|---|---|---|
| Web server | Flask | Free/open-source |
| Realtime execution | Flask-SocketIO | Free/open-source |
| Production server | Gunicorn gthread | Free/open-source |
| Python execution | Local Python subprocess | Free |
| Git workflow | Git CLI | Free/open-source |
| Audit log | JSONL file | Free |
| Policy | JSON file | Free |
| Metrics | Plain text endpoint | Free |

## 3. Deployment options

| Platform | Use | Cost |
|---|---|---|
| Termux | Full local tablet backend | Free |
| GitHub | Source hosting | Free tier |
| GitHub Pages | Static preview | Free |
| Cloudflare Pages | Static preview | Free tier |
| Render | Full backend deployment | Free tier available |
| Docker | Local/server deployment | Free if self-hosted |
| GitHub Actions | Static checks | Free tier |

## 4. No AI API

The system does not depend on:

- OpenAI API;
- Gemini API;
- Claude API;
- paid inference APIs;
- paid Copilot-style runtime services.

This is intentional because paid AI APIs are not cost-effective for the stated use case.

## 5. Enterprise architecture summary

```text
Browser UI
  ↓ HTTP / WebSocket
Flask + Flask-SocketIO Backend
  ↓
Workspace Files + Python Runtime + Git CLI
  ↓
Audit Log / Policy JSON / Metrics / Backups
```

## 6. Security model

- Optional password gate via `IDE_PASSWORD`.
- Session secret via `SECRET_KEY`.
- Safe workspace path resolution.
- Upload policy enforcement.
- Terminal and pip policy enforcement.
- Git push policy enforcement.
- Audit logs for key events.
- Security headers.

## 7. Limitation

This is a free-tool architecture. It is powerful but should not be exposed publicly without authentication and careful policy settings.
