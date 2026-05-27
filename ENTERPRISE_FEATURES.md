# Enterprise Features — VSCode Stimulator

VSCode Stimulator now includes enterprise-style features built with free/open-source tools and no paid AI API.

> Legal/practical note: this project is designed to mimic VS Code's layout, workflow and functionality as closely as practical, but it does not copy Microsoft VS Code source code, proprietary icons, trademarks, marketplace assets or licensed branding.

## 1. Optional Password Gate

Set an environment variable to protect the whole IDE:

```text
IDE_PASSWORD=your-strong-password
```

When `IDE_PASSWORD` is set, users must sign in before accessing the workbench. When it is not set, the system remains open for local/tablet use.

## 2. Enterprise Center UI

A new Activity Bar panel called **Enterprise Center** provides:

- system health;
- audit log viewer;
- enterprise policy editor;
- full project backup download;
- security explanation;
- metrics explanation.

## 3. Audit Log

The backend writes important events to:

```text
workspace/.audit_log.jsonl
```

Logged events include examples such as:

- login success/failure;
- logout;
- file write;
- file create;
- file delete;
- file rename;
- Git commit;
- policy update;
- project backup.

Audit endpoint:

```text
GET /api/enterprise/audit?limit=100
```

## 4. System Health Endpoint

Endpoint:

```text
GET /api/enterprise/health
```

Returns:

- app name;
- Python version;
- workspace path;
- file count;
- workspace size;
- authentication status;
- timestamp.

## 5. Enterprise Policy JSON

Policy endpoint:

```text
GET /api/enterprise/policy
POST /api/enterprise/policy
```

Example policy:

```json
{
  "allow_terminal": true,
  "allow_pip_install": true,
  "allow_git_push": true,
  "max_upload_mb": 25,
  "note": "Policy is advisory unless extended in backend hooks."
}
```

## 6. Full Project Backup

Endpoint:

```text
GET /api/enterprise/backup
```

Downloads a zip backup of the project excluding common unnecessary folders such as `.git`, `.venv`, `node_modules` and `__pycache__`.

## 7. Prometheus-Style Metrics

Endpoint:

```text
GET /api/enterprise/metrics
```

Returns text metrics suitable for free monitoring tools:

```text
vscode_stimulator_workspace_files
vscode_stimulator_workspace_bytes
```

## 8. Free Deployment Compatibility

Enterprise features work with:

- local Python server;
- Termux on Android;
- Render free tier;
- Docker on any free/local machine.

## 9. Recommended Enterprise Environment Variables

```text
SECRET_KEY=replace-with-long-random-secret
IDE_PASSWORD=replace-with-strong-password
WORKSPACE_ROOT=/opt/render/project/src/workspace
```

## 10. No AI API Requirement

No enterprise feature requires OpenAI, Gemini, Claude or any paid AI service. This keeps the platform cost-effective.


## 11. Enforced Policy Controls

The policy system now enforces:

- `allow_terminal`: blocks browser terminal commands when false.
- `allow_pip_install`: blocks pip install commands when false.
- `allow_git_push`: blocks Git push when false.
- `max_upload_mb`: blocks oversized uploads.
- `allowed_upload_extensions`: blocks upload extensions not in the allow-list.

## 12. Security Headers

The Flask backend adds free enterprise hardening headers:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy` restrictions

## 13. Extra Platform Files

The enterprise folder includes:

- Dockerfile
- docker-compose.yml
- .dockerignore
- GitHub Actions workflow
- netlify.toml for static preview
- .env.example
- platform and admin guides
