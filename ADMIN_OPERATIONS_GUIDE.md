# Admin Operations Guide — VSCode Stimulator Enterprise

This guide explains how to operate the enterprise features using free tools.

## 1. Enable login protection

Set this environment variable:

```text
IDE_PASSWORD=your-strong-password
```

Also set:

```text
SECRET_KEY=your-long-random-secret
```

If `IDE_PASSWORD` is not set, the IDE remains open. This is useful for local tablet use but not recommended for public Render deployment.

## 2. Enterprise policy

Open the Enterprise Center inside the IDE and edit the policy JSON.

Default enforced policy fields:

```json
{
  "allow_terminal": true,
  "allow_pip_install": true,
  "allow_git_push": true,
  "max_upload_mb": 25,
  "allowed_upload_extensions": [".py", ".md", ".txt", ".csv", ".json", ".html", ".css", ".js", ".sql", ".sh", ".png", ".jpg", ".jpeg", ".svg"]
}
```

## 3. What policy controls

### `allow_terminal`

If false, browser terminal commands are blocked.

### `allow_pip_install`

If false, `pip install` commands are blocked from the terminal.

### `allow_git_push`

If false, Git push is blocked.

### `max_upload_mb`

Maximum allowed upload size per file.

### `allowed_upload_extensions`

Allowed file extensions for upload. Empty list means no extension restriction.

## 4. Audit log

Audit log path:

```text
workspace/.audit_log.jsonl
```

View it from:

```text
Enterprise Center → Audit
```

Or endpoint:

```text
/api/enterprise/audit?limit=100
```

## 5. Backup

Use:

```text
Enterprise Center → Backup
```

Or endpoint:

```text
/api/enterprise/backup
```

## 6. Health monitoring

Use:

```text
/api/enterprise/health
```

For metrics:

```text
/api/enterprise/metrics
```

The metrics format is compatible with free Prometheus-style monitoring tools.

## 7. Recommended public deployment settings

For Render:

```text
SECRET_KEY=generate-a-long-random-secret
IDE_PASSWORD=choose-a-strong-password
WORKSPACE_ROOT=/opt/render/project/src/workspace
```

## 8. Incident response

If a token or password is exposed:

1. Rotate it immediately.
2. Remove it from Git history if committed.
3. Change `IDE_PASSWORD`.
4. Check the audit log.
5. Redeploy.

## 9. No AI API requirement

No admin operation requires paid AI APIs. The platform remains cost-effective.
