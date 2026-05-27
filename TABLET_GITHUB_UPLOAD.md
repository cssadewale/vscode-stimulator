# Uploading VSCode Stimulator from itel Vista Tab 30s to GitHub

This guide is written for uploading the project from an Android tablet, especially the itel Vista Tab 30s.

## Important Rule

Do **not** upload only `index.html` if you want full deployment. Upload the complete project folder contents:

```text
index.html
backend/
workspace/
README.md
FEATURES.md
DEPLOYMENT.md
SECURITY.md
CONTRIBUTING.md
requirements.txt
Procfile
render.yaml
runtime.txt
manifest.json
service-worker.js
.nojekyll
LICENSE
.gitignore
```

## Option A — GitHub Web Upload from Chrome

This is the easiest method on a tablet.

### Step 1 — Prepare the folder

Make sure all files are inside one folder named:

```text
vscode-stimulator
```

If you are using a file manager, unzip `vscode-stimulator.zip` first.

### Step 2 — Open GitHub

Open Chrome and visit:

```text
https://github.com
```

Sign in to your account:

```text
https://github.com/cssadewale
```

### Step 3 — Create a new repository

1. Tap the `+` icon.
2. Choose **New repository**.
3. Repository name:

```text
vscode-stimulator
```

4. Add a description:

```text
Tablet-first VS Code-like Python and data-science IDE built with free tools. No paid AI API.
```

5. Choose Public or Private.
6. Tap **Create repository**.

### Step 4 — Upload files

1. Tap **Add file**.
2. Tap **Upload files**.
3. Use the Android file picker.
4. Select all files and folders from the project.
5. If GitHub web upload struggles with folders, upload in batches:
   - first root files;
   - then `backend` files;
   - then `workspace/projects/welcome.py`;
   - then docs.

### Step 5 — Commit upload

Use commit message:

```text
Initial VSCode Stimulator release
```

Tap **Commit changes**.

## Option B — Termux Git Upload

This is the professional method and is better for future updates.

### Step 1 — Install Termux from F-Droid

Use F-Droid, not the outdated Play Store version.

### Step 2 — Install Git and Python

```bash
pkg update && pkg upgrade -y
pkg install git python -y
```

### Step 3 — Move into the project folder

Example:

```bash
cd /sdcard/Download/vscode-stimulator
```

If storage permission is denied, run:

```bash
termux-setup-storage
```

Then approve permission.

### Step 4 — Configure Git identity

```bash
git config --global user.name "Adewale Samson Adeagbo"
git config --global user.email "your-email@example.com"
```

### Step 5 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial VSCode Stimulator release"
git branch -M main
git remote add origin https://github.com/cssadewale/vscode-stimulator.git
git push -u origin main
```

GitHub may ask for username and token. Use a GitHub Personal Access Token instead of your password.

## Static Deployment with GitHub Pages

Use this for interface preview only.

1. Open the repository on GitHub.
2. Go to **Settings**.
3. Go to **Pages**.
4. Source: **Deploy from a branch**.
5. Branch: `main`.
6. Folder: `/root`.
7. Save.

The static preview will not run Python or terminal commands.

## Full Deployment with Render Free Tier

Use this for Python execution and backend functionality.

1. Go to <https://render.com>.
2. Sign in with GitHub.
3. Click **New +**.
4. Choose **Web Service**.
5. Select the `vscode-stimulator` repository.
6. Use:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn --worker-class gthread --threads 8 -w 1 backend.app:app --bind 0.0.0.0:$PORT --timeout 180
```

7. Add environment variables:

```text
SECRET_KEY = any-long-random-string
WORKSPACE_ROOT = /opt/render/project/src/workspace
```

8. Click **Deploy**.

## Updating Later from Termux

After editing files:

```bash
git add .
git commit -m "Update VSCode Stimulator"
git push
```

## Cost Policy

This deployment workflow uses free tools. No paid AI API is required.
