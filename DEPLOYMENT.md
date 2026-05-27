# Deployment Guide — VSCode Stimulator

## Which Deployment Should I Choose?

- **Use Termux/local deployment** if you want the full IDE on your own device for free.
- **Use Render free tier** if you want a public URL with backend execution.
- **Use GitHub Pages or Cloudflare Pages** only for a static interface demo.
- **Do not use paid AI APIs**; the system does not require them.


This guide gives clear deployment paths for static preview, local use and full backend hosting.

## Uploading from itel Vista Tab 30s

For the clearest tablet upload workflow, read:

```text
TABLET_GITHUB_UPLOAD.md
```

Summary:

1. Keep all files in the `vscode-stimulator` folder.
2. Upload the full folder contents to GitHub, not only `index.html`.
3. Use GitHub Pages for static preview only.
4. Use Render free tier for full backend features.
5. Use Termux Git commands for easier future updates.

## 1. Local Deployment

```bash
git clone https://github.com/cssadewale/vscode-stimulator.git
cd vscode-stimulator
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py
```

Open:

```text
http://localhost:5000
```

## 2. Android / Termux Deployment

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/cssadewale/vscode-stimulator.git
cd vscode-stimulator
pip install -r requirements.txt
python backend/app.py
```

Open in Android browser:

```text
http://127.0.0.1:5000
```

If heavy scientific packages fail, install the core server first:

```bash
pip install Flask Flask-SocketIO python-socketio python-engineio gunicorn simple-websocket psutil
```

Then install Pandas, NumPy, Matplotlib and Scikit-learn only if the device supports them.

## 3. GitHub Pages Static Preview

Use this only for UI demonstration.

1. Push repository to GitHub.
2. Open repository **Settings**.
3. Go to **Pages**.
4. Source: **Deploy from branch**.
5. Branch: `main`.
6. Folder: `/root`.
7. Save.

Limitations: no backend, no terminal, no Python execution, no Git operations.

## 4. Render Free-Tier Full Deployment

1. Push repository to GitHub.
2. Go to <https://render.com>.
3. Create a new **Web Service**.
4. Connect the GitHub repository.
5. Use:

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn --worker-class gthread --threads 8 -w 1 backend.app:app --bind 0.0.0.0:$PORT --timeout 180
Plan: Free
```

6. Add environment variables:

```text
SECRET_KEY = generate-a-long-random-secret
WORKSPACE_ROOT = /opt/render/project/src/workspace
```

7. Click **Deploy**.
8. Open your Render URL.

## 5. Cloudflare Pages Static Deployment

1. Push repository to GitHub.
2. Open Cloudflare Pages.
3. Create a new Pages project.
4. Select GitHub repo.
5. Build command: blank.
6. Output directory: `/`.
7. Deploy.

This is static only. Use Render or local Termux for backend features.

## 6. Recommended Production Hardening

Before making a public backend instance widely available:

- add login/authentication;
- disable arbitrary terminal commands for guests;
- restrict package installation;
- never commit `.env` or tokens;
- use a private workspace;
- use GitHub tokens only when necessary;
- rotate tokens if they are exposed.

## 7. No AI API Deployment

No API key is required. Do not add paid AI runtime dependencies unless a future version explicitly needs them.


## Expert Deployment Checklist

Before uploading from the itel Vista Tab 30s, confirm that these files exist:

```text
index.html
backend/app.py
requirements.txt
Procfile
render.yaml
runtime.txt
manifest.json
service-worker.js
README.md
FEATURES.md
DEPLOYMENT.md
TABLET_GITHUB_UPLOAD.md
VS_CODE_MIMICRY.md
SECURITY.md
LICENSE
```

### Static deployment checklist

Use GitHub Pages or Cloudflare Pages when you only need:

- UI preview;
- documentation;
- static editor interface;
- PWA/static caching.

### Full backend deployment checklist

Use Render free tier or Termux when you need:

- Python execution;
- terminal;
- Git operations;
- package management;
- file save/load through backend;
- plot capture;
- inspector;
- profiler;
- TODO workspace scanner;
- workspace zip export.

### No AI API checklist

Do not add OpenAI, Gemini, Claude or other AI API keys. The system is intentionally designed to run without paid AI APIs.


## Docker Deployment

If you have access to a computer or server with Docker, run:

```bash
docker compose up --build
```

Open:

```text
http://localhost:5000
```

The provided `docker-compose.yml` sets:

```text
IDE_PASSWORD=change-this-password
SECRET_KEY=change-this-secret
WORKSPACE_ROOT=/app/workspace
```

Change these before serious use.

## Enterprise Render Deployment

For a protected public Render deployment:

1. Push the repository to GitHub.
2. Create a Render Web Service.
3. Build command:

```bash
pip install -r requirements.txt
```

4. Start command:

```bash
gunicorn --worker-class gthread --threads 8 -w 1 backend.app:app --bind 0.0.0.0:$PORT --timeout 180
```

5. Add environment variables:

```text
SECRET_KEY=generate-a-long-random-secret
IDE_PASSWORD=choose-a-strong-password
WORKSPACE_ROOT=/opt/render/project/src/workspace
```

6. Deploy.
7. Visit the Render URL and sign in with `IDE_PASSWORD`.


## Netlify Static Preview

The `enterprise` folder includes `netlify.toml` for static preview deployments.

Steps:

1. Push the repository to GitHub.
2. Log in to Netlify.
3. Create a new site from GitHub.
4. Select the repository.
5. Build command: leave blank.
6. Publish directory: `.`
7. Deploy.

Netlify static preview does not run the Flask backend. Use Render, Termux or Docker for backend features.
