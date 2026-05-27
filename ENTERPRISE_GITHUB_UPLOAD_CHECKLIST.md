# Enterprise GitHub Upload Checklist

Use this checklist before uploading the `enterprise` folder to GitHub or any deployment platform.

## 1. Files that must be uploaded

Upload the full folder contents, not only `index.html`.

Required files/folders:

```text
index.html
backend/
workspace/
README.md
FEATURES.md
DEPLOYMENT.md
ENTERPRISE_FEATURES.md
ENTERPRISE_GITHUB_UPLOAD_CHECKLIST.md
ADMIN_OPERATIONS_GUIDE.md
FREE_TOOLS_ARCHITECTURE.md
TABLET_GITHUB_UPLOAD.md
VS_CODE_MIMICRY.md
SECURITY.md
CONTRIBUTING.md
requirements.txt
Procfile
render.yaml
runtime.txt
manifest.json
service-worker.js
Dockerfile
docker-compose.yml
.env.example
.github/
.nojekyll
LICENSE
.gitignore
start.sh
termux_setup.sh
```

## 2. Files that should not contain real secrets

Before pushing to GitHub, confirm that these files do not contain real passwords, tokens or private keys:

```text
.env
.env.example
render.yaml
docker-compose.yml
README.md
DEPLOYMENT.md
```

Use placeholders in the repo and set real values only inside Render, Termux or your server environment.

## 3. Recommended GitHub repository settings

1. Repository name: `vscode-stimulator-enterprise` or `vscode-stimulator`.
2. Description:

```text
Enterprise-ready tablet-first VS Code-like Python/data-science IDE built with free tools. No paid AI API.
```

3. Add topics:

```text
vscode-like
python
flask
edtech
data-science
termux
code-editor
no-ai-api
```

## 4. Recommended branch protection

For serious use:

1. Go to GitHub repository settings.
2. Open **Branches**.
3. Add branch protection rule for `main`.
4. Enable pull request review if working with collaborators.
5. Enable the included GitHub Actions static check.

## 5. Final command from Termux

```bash
git init
git add .
git commit -m "Enterprise VSCode Stimulator release"
git branch -M main
git remote add origin https://github.com/cssadewale/vscode-stimulator.git
git push -u origin main
```
