"""VSCode Stimulator backend.
Free/open-source Flask + Socket.IO server for the browser IDE.
No AI API is used.
"""
from __future__ import annotations

import base64
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_file, send_from_directory, session, redirect, Response
from flask_socketio import SocketIO, emit

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(os.environ.get("WORKSPACE_ROOT", ROOT / "workspace")).resolve()
HISTORY = WORKSPACE / ".history"
SNIPPETS_FILE = WORKSPACE / ".snippets.json"
DOTENV_FILE = WORKSPACE / ".env"
RUN_HISTORY_FILE = WORKSPACE / ".run_history.json"
AUDIT_FILE = WORKSPACE / ".audit_log.jsonl"
POLICY_FILE = WORKSPACE / ".enterprise_policy.json"

for d in [WORKSPACE, HISTORY, WORKSPACE / "projects", WORKSPACE / "datasets", WORKSPACE / "exports"]:
    d.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=str(ROOT), static_url_path="")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

EXCLUDE = {".git", "__pycache__", ".history", ".venv", "node_modules"}

def safe_path(rel: str | None = "") -> Path:
    rel = rel or ""
    p = (WORKSPACE / rel).resolve()
    if p != WORKSPACE and WORKSPACE not in p.parents:
        raise ValueError("Path escapes workspace")
    return p

def relpath(p: Path) -> str:
    return str(p.resolve().relative_to(WORKSPACE)).replace("\\", "/")

def load_json(path: Path, default: Any):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def save_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def log_event(action: str, target: str = "", status: str = "ok", extra: dict | None = None):
    """Append JSONL audit event. Free enterprise-style observability."""
    try:
        event = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "target": target,
            "status": status,
            "ip": request.headers.get("X-Forwarded-For", request.remote_addr or ""),
            "ua": (request.headers.get("User-Agent") or "")[:160],
            "extra": extra or {},
        }
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with AUDIT_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass

def enterprise_policy() -> dict:
    default = {
        "allow_terminal": True,
        "allow_pip_install": True,
        "allow_git_push": True,
        "max_upload_mb": 25,
        "allowed_upload_extensions": [".py", ".md", ".txt", ".csv", ".json", ".html", ".css", ".js", ".sql", ".sh", ".png", ".jpg", ".jpeg", ".svg"],
        "note": "Policy is enforced for upload size/extensions, terminal, pip install and git push."
    }
    saved = load_json(POLICY_FILE, {})
    default.update(saved if isinstance(saved, dict) else {})
    return default

def policy_allowed(key: str) -> bool:
    return bool(enterprise_policy().get(key, True))

@app.after_request
def enterprise_security_headers(response):
    # Free enterprise hardening headers. CSP is intentionally not strict because the single-file IDE uses inline scripts/styles and optional CDN libraries.
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    response.headers.setdefault("X-Workspace-App", "VSCode-Stimulator")
    return response

def snapshot(path: Path):
    if not path.exists() or not path.is_file():
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest_dir = HISTORY / relpath(path).replace("/", "__")
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest_dir / f"{stamp}__{path.name}")

def tree_node(path: Path):
    if path.name in EXCLUDE or path.name.startswith(".") and path.name not in {".env"}:
        return None
    if path.is_dir():
        children = []
        for child in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            n = tree_node(child)
            if n:
                children.append(n)
        return {"name": path.name, "path": relpath(path), "type": "directory", "children": children}
    return {"name": path.name, "path": relpath(path), "type": "file", "extension": path.suffix.lstrip(".")}

def run_cmd(cmd, cwd=WORKSPACE, timeout=120):
    try:
        cp = subprocess.run(cmd, cwd=str(cwd), shell=isinstance(cmd, str), text=True,
                            capture_output=True, timeout=timeout)
        return {"ok": cp.returncode == 0, "output": (cp.stdout or "") + (cp.stderr or ""), "returncode": cp.returncode}
    except Exception as e:
        return {"ok": False, "output": str(e), "returncode": 1}

def run_python_file(path: Path | None = None, code: str | None = None, args=None):
    args = args or []
    if code is not None:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
        tmp.write(code)
        tmp.close()
        cmd = [sys.executable, tmp.name] + args
    else:
        cmd = [sys.executable, str(path)] + args
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["MPLBACKEND"] = "Agg"
    return subprocess.Popen(cmd, cwd=str(WORKSPACE), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, bufsize=1, env=env)


def auth_required() -> bool:
    return bool(os.environ.get("IDE_PASSWORD"))

@app.before_request
def enterprise_auth_gate():
    """Optional free authentication gate. Disabled unless IDE_PASSWORD is set."""
    if not auth_required():
        return None
    public = {"/login", "/manifest.json", "/service-worker.js"}
    if request.path in public or request.path.startswith("/static"):
        return None
    if session.get("authenticated"):
        return None
    if request.path.startswith("/api"):
        return jsonify(ok=False, error="Authentication required"), 401
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def enterprise_login():
    if not auth_required():
        return redirect("/")
    error = ""
    if request.method == "POST":
        if request.form.get("password") == os.environ.get("IDE_PASSWORD"):
            session["authenticated"] = True
            log_event("auth.login", "", "ok")
            return redirect("/")
        error = "Invalid password"
        log_event("auth.login", "", "failed")
    html = f"""<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>VSCode Stimulator Login</title><style>body{{margin:0;background:#0d1117;color:#e6edf3;font-family:system-ui;display:grid;place-items:center;min-height:100vh}}form{{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:24px;width:min(360px,92vw);box-shadow:0 20px 60px #0008}}input,button{{width:100%;box-sizing:border-box;padding:12px;border-radius:8px;border:1px solid #30363d;background:#21262d;color:#e6edf3;margin-top:10px}}button{{background:#238636;cursor:pointer;font-weight:700}}.err{{color:#f85149;font-size:13px;margin-top:10px}}</style></head><body><form method='post'><h2>VSCode Stimulator</h2><p>Enterprise access is protected. Enter IDE password.</p><input type='password' name='password' placeholder='Password' autofocus><button>Sign in</button><div class='err'>{error}</div><p style='font-size:12px;color:#8b949e;line-height:1.6'>Set or remove IDE_PASSWORD in your environment variables to enable/disable this gate.</p></form></body></html>"""
    return Response(html, mimetype="text/html")

@app.get("/logout")
def enterprise_logout():
    session.clear()
    log_event("auth.logout", "", "ok")
    return redirect("/login" if auth_required() else "/")

@app.route("/")
def home():
    return send_from_directory(str(ROOT), "index.html")

@app.get("/api/fs/tree")
def fs_tree():
    nodes = []
    for p in sorted(WORKSPACE.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
        n = tree_node(p)
        if n:
            nodes.append(n)
    return jsonify(ok=True, tree=nodes)

@app.get("/api/fs/read")
def fs_read():
    try:
        p = safe_path(request.args.get("path"))
        return jsonify(ok=True, content=p.read_text(encoding="utf-8"))
    except Exception as e:
        return jsonify(ok=False, error=str(e))

@app.post("/api/fs/write")
def fs_write():
    data = request.get_json() or {}
    try:
        p = safe_path(data.get("path"))
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            snapshot(p)
        p.write_text(data.get("content", ""), encoding="utf-8")
        log_event("fs.write", relpath(p), "ok")
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e))

@app.post("/api/fs/create")
def fs_create():
    data = request.get_json() or {}
    try:
        p = safe_path(data.get("path"))
        if data.get("type") == "directory":
            p.mkdir(parents=True, exist_ok=True)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch(exist_ok=True)
        log_event("fs.create", relpath(p), "ok", {"type": data.get("type")})
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e))

@app.delete("/api/fs/delete")
def fs_delete():
    try:
        p = safe_path(request.args.get("path"))
        if p.is_dir(): shutil.rmtree(p)
        elif p.exists(): p.unlink()
        log_event("fs.delete", request.args.get("path") or "", "ok")
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e))

@app.post("/api/fs/rename")
def fs_rename():
    data = request.get_json() or {}
    try:
        src, dst = safe_path(data.get("src")), safe_path(data.get("dst"))
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        log_event("fs.rename", data.get("src", ""), "ok", {"dst": data.get("dst", "")})
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e))

@app.get("/api/fs/download")
def fs_download():
    p = safe_path(request.args.get("path"))
    return send_file(p, as_attachment=True, download_name=p.name)

@app.post("/api/fs/upload")
def fs_upload():
    pol = enterprise_policy()
    max_bytes = int(pol.get("max_upload_mb", 25)) * 1024 * 1024
    allowed_ext = set(pol.get("allowed_upload_extensions", []))
    dest = safe_path(request.form.get("dir", "datasets"))
    dest.mkdir(parents=True, exist_ok=True)
    saved=[]
    for f in request.files.getlist("files"):
        filename = Path(f.filename).name
        ext = Path(filename).suffix.lower()
        if allowed_ext and ext not in allowed_ext:
            log_event("fs.upload", filename, "blocked", {"reason": "extension", "ext": ext})
            return jsonify(ok=False, error=f"Upload blocked by policy: {ext} not allowed"), 400
        data = f.read()
        if len(data) > max_bytes:
            log_event("fs.upload", filename, "blocked", {"reason": "size", "bytes": len(data)})
            return jsonify(ok=False, error=f"Upload blocked by policy: file larger than {pol.get('max_upload_mb',25)} MB"), 400
        out = dest / filename
        out.write_bytes(data)
        saved.append(relpath(out))
        log_event("fs.upload", relpath(out), "ok", {"bytes": len(data)})
    return jsonify(ok=True, saved=saved)

@app.get("/api/fs/csv_preview")
def csv_preview():
    try:
        p = safe_path(request.args.get("path"))
        limit = int(request.args.get("limit", 500))
        with p.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows=[]
            for i,row in enumerate(reader):
                if i >= limit: break
                rows.append(row)
            return jsonify(ok=True, columns=reader.fieldnames or [], rows=rows, count=len(rows), truncated=len(rows)>=limit)
    except Exception as e:
        return jsonify(ok=False, error=str(e))

@app.get("/api/fs/stats")
def fs_stats():
    files=[]
    for p in WORKSPACE.rglob("*"):
        if any(part in EXCLUDE for part in p.parts):
            continue
        if p.is_file():
            st=p.stat(); files.append((p,st.st_size,st.st_mtime))
    by={}
    for p,size,_ in files:
        ext=p.suffix.lstrip(".") or "no-ext"
        by.setdefault(ext,{"ext":ext,"count":0,"size":0})
        by[ext]["count"]+=1; by[ext]["size"]+=size
    recent=sorted(files,key=lambda x:x[2],reverse=True)[:10]
    return jsonify(total_files=len(files), total_size=sum(x[1] for x in files),
                   by_extension=sorted(by.values(), key=lambda x:x["count"], reverse=True),
                   recent=[{"path":relpath(p),"size":s,"mtime":m} for p,s,m in recent])

@app.get("/api/fs/history")
def fs_history():
    path = request.args.get("path", "").replace("/", "__")
    d = HISTORY / path
    snaps=[]
    if d.exists():
        for p in sorted(d.iterdir(), reverse=True):
            snaps.append({"name": p.name, "timestamp": p.name.split("__")[0], "size": p.stat().st_size})
    return jsonify(ok=True, snapshots=snaps)

@app.post("/api/fs/history/restore")
def fs_history_restore():
    data=request.get_json() or {}
    try:
        target=safe_path(data.get("path")); snapshot(target)
        snap=HISTORY / data.get("path","").replace("/","__") / data.get("snapshot","")
        shutil.copy2(snap,target)
        return jsonify(ok=True)
    except Exception as e: return jsonify(ok=False,error=str(e))


@app.get("/api/fs/todos")
def fs_todos():
    import re
    rx = re.compile(r"\b(TODO|FIXME|BUG|HACK|NOTE)\b[:\-]?\s*(.*)", re.I)
    todos = []
    allowed = {".py", ".js", ".ts", ".html", ".css", ".md", ".txt", ".json", ".sql", ".sh", ".r"}
    for p in WORKSPACE.rglob("*"):
        if any(part in EXCLUDE for part in p.parts) or not p.is_file() or p.suffix.lower() not in allowed:
            continue
        try:
            for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                m = rx.search(line)
                if m:
                    todos.append({"path": relpath(p), "line": i, "tag": m.group(1).upper(), "text": (m.group(2) or line.strip())[:240]})
        except Exception:
            pass
    return jsonify(ok=True, todos=todos[:500])

@app.get("/api/fs/workspace_zip")
def fs_workspace_zip():
    import zipfile
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as z:
        for p in WORKSPACE.rglob("*"):
            if any(part in EXCLUDE for part in p.parts) or p.is_dir():
                continue
            z.write(p, relpath(p))
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name="vscode-stimulator-workspace.zip", mimetype="application/zip")

@app.post("/api/lint")
def lint():
    code=(request.get_json() or {}).get("code","")
    issues=[]
    try: compile(code,"<editor>","exec")
    except SyntaxError as e: issues.append({"line":e.lineno or 1,"message":e.msg})
    return jsonify(ok=True, issues=issues)

@app.post("/api/format")
def fmt():
    code=(request.get_json() or {}).get("code","")
    return jsonify(ok=True, formatted=code, formatter="basic/no-op")

@app.get("/api/packages/list")
def packages_list():
    out=run_cmd([sys.executable,"-m","pip","list","--format=json"], timeout=60)
    try: packages=json.loads(out["output"])
    except Exception: packages=[]
    return jsonify(packages=packages)

@app.get("/api/packages/outdated")
def packages_outdated():
    out=run_cmd([sys.executable,"-m","pip","list","--outdated","--format=json"], timeout=90)
    try: outdated=json.loads(out["output"])
    except Exception: outdated=[]
    return jsonify(outdated=outdated)

@app.get("/api/snippets")
def snippets_get(): return jsonify(snippets=load_json(SNIPPETS_FILE, []))
@app.post("/api/snippets")
def snippets_post():
    data=request.get_json() or {}; items=load_json(SNIPPETS_FILE, [])
    data["id"]=str(int(time.time()*1000)); items.append(data); save_json(SNIPPETS_FILE, items)
    return jsonify(ok=True, id=data["id"])
@app.get("/api/snippets/<sid>")
def snippets_one(sid):
    for s in load_json(SNIPPETS_FILE, []):
        if s.get("id")==sid: return jsonify(s)
    return jsonify(error="Not found"),404
@app.delete("/api/snippets/<sid>")
def snippets_del(sid):
    items=[s for s in load_json(SNIPPETS_FILE, []) if s.get("id")!=sid]
    save_json(SNIPPETS_FILE, items); return jsonify(ok=True)

@app.get("/api/env/dotenv")
def env_get():
    vars={}
    if DOTENV_FILE.exists():
        for line in DOTENV_FILE.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k,v=line.split("=",1); vars[k.strip()]=v.strip()
    return jsonify(vars=vars)
@app.post("/api/env/dotenv")
def env_post():
    vars=(request.get_json() or {}).get("vars",{})
    DOTENV_FILE.write_text("\n".join(f"{k}={v}" for k,v in vars.items()), encoding="utf-8")
    return jsonify(ok=True, count=len(vars))
@app.get("/api/env/info")
def env_info(): return jsonify(python_version=sys.version)
@app.get("/api/env/system")
def env_system():
    try:
        import psutil
        return jsonify(cpu_percent=psutil.cpu_percent(), ram_percent=psutil.virtual_memory().percent)
    except Exception: return jsonify(cpu_percent=0, ram_percent=0)


@app.get("/api/enterprise/health")
def enterprise_health():
    total = 0
    size = 0
    for fp in WORKSPACE.rglob("*"):
        if fp.is_file() and not any(part in EXCLUDE for part in fp.parts):
            total += 1
            size += fp.stat().st_size
    return jsonify(ok=True, app="VSCode Stimulator", python=sys.version.split()[0], workspace=str(WORKSPACE), files=total, size=size,
                   auth_enabled=auth_required(), audit_log=AUDIT_FILE.exists(), timestamp=datetime.utcnow().isoformat()+"Z")

@app.get("/api/enterprise/audit")
def enterprise_audit():
    limit = int(request.args.get("limit", 100))
    rows = []
    if AUDIT_FILE.exists():
        lines = AUDIT_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()[-limit:]
        for line in lines:
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return jsonify(ok=True, events=list(reversed(rows)))

@app.get("/api/enterprise/policy")
def enterprise_policy_get():
    return jsonify(ok=True, policy=enterprise_policy())

@app.post("/api/enterprise/policy")
def enterprise_policy_post():
    data = request.get_json() or {}
    save_json(POLICY_FILE, data.get("policy", data))
    log_event("enterprise.policy.update", "policy", "ok")
    return jsonify(ok=True)

@app.get("/api/enterprise/backup")
def enterprise_backup():
    import zipfile
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as z:
        for fp in ROOT.rglob("*"):
            if any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in fp.parts) or fp.is_dir():
                continue
            z.write(fp, str(fp.relative_to(ROOT)))
    mem.seek(0)
    log_event("enterprise.backup", "project", "ok")
    return send_file(mem, as_attachment=True, download_name="vscode-stimulator-enterprise-backup.zip", mimetype="application/zip")

@app.get("/api/enterprise/metrics")
def enterprise_metrics():
    files = 0
    size = 0
    for fp in WORKSPACE.rglob("*"):
        if fp.is_file() and not any(part in EXCLUDE for part in fp.parts):
            files += 1
            size += fp.stat().st_size
    body = f"# HELP vscode_stimulator_workspace_files Workspace file count\n# TYPE vscode_stimulator_workspace_files gauge\nvscode_stimulator_workspace_files {files}\n# HELP vscode_stimulator_workspace_bytes Workspace size in bytes\n# TYPE vscode_stimulator_workspace_bytes gauge\nvscode_stimulator_workspace_bytes {size}\n"
    return Response(body, mimetype="text/plain")

# Git helpers
@app.get("/api/git/status")
def git_status(): return jsonify(status=run_cmd("git status --porcelain")["output"])
@app.get("/api/git/log")
def git_log(): return jsonify(log=run_cmd("git --no-pager log --oneline -8")["output"])
@app.get("/api/git/diff")
def git_diff(): return jsonify(diff=run_cmd("git --no-pager diff")["output"])
@app.get("/api/git/branches")
def git_branches():
    out=run_cmd("git branch")["output"]; branches=[]
    for line in out.splitlines(): branches.append({"name":line.replace("*","",1).strip(),"current":line.startswith("*")})
    return jsonify(branches=branches)
@app.post("/api/git/init")
def git_init(): return jsonify(run_cmd("git init"))
@app.post("/api/git/commit")
def git_commit():
    msg=(request.get_json() or {}).get("message","update")
    run_cmd("git add .")
    res = run_cmd(["git","commit","-m",msg])
    log_event("git.commit", msg, "ok" if res.get("ok") else "failed")
    return jsonify(res)
@app.post("/api/git/remote/set")
def git_remote():
    url=(request.get_json() or {}).get("url","")
    run_cmd("git remote remove origin")
    return jsonify(run_cmd(["git","remote","add","origin",url]))
@app.post("/api/git/config")
def git_config():
    d=request.get_json() or {}
    if d.get("name"): run_cmd(["git","config","user.name",d["name"]])
    if d.get("email"): run_cmd(["git","config","user.email",d["email"]])
    return jsonify(ok=True)
@app.post("/api/git/push")
def git_push():
    if not policy_allowed("allow_git_push"):
        log_event("git.push", "", "blocked")
        return jsonify(ok=False, output="Git push blocked by enterprise policy"), 403
    d=request.get_json() or {}; return jsonify(run_cmd(["git","push",d.get("remote","origin"),d.get("branch","main")], timeout=180))
@app.post("/api/git/pull")
def git_pull():
    d=request.get_json() or {}; return jsonify(run_cmd(["git","pull",d.get("remote","origin"),d.get("branch","main")], timeout=180))
@app.post("/api/git/checkout")
def git_checkout():
    d=request.get_json() or {}; cmd=["git","checkout"] + (["-b"] if d.get("create") else []) + [d.get("branch","main")]
    return jsonify(run_cmd(cmd))
@app.post("/api/git/stash")
def git_stash(): return jsonify(run_cmd(["git","stash",(request.get_json() or {}).get("action","push")]))

@app.post("/api/run/inspect")
def inspect_run():
    data=request.get_json() or {}; p=safe_path(data.get("path"))
    helper = f"""import runpy, json, reprlib\nns=runpy.run_path({str(p)!r})\nout={{}}\nfor k,v in ns.items():\n    if not k.startswith('__'):\n        out[k]={{'type':type(v).__name__,'value':reprlib.repr(v)}}\nprint('___VARS___'+json.dumps(out))\n"""
    cp=subprocess.run([sys.executable,"-c",helper], cwd=str(WORKSPACE), capture_output=True, text=True, timeout=120)
    vars={}; stdout=cp.stdout
    if "___VARS___" in stdout:
        before, js=stdout.rsplit("___VARS___",1); stdout=before
        try: vars=json.loads(js.strip().splitlines()[-1])
        except Exception: vars={}
    return jsonify(variables=vars, stdout=stdout, stderr=cp.stderr)

@app.post("/api/run/profile")
def profile_run():
    data=request.get_json() or {}; p=safe_path(data.get("path")); top=int(data.get("top",30))
    cmd=[sys.executable,"-m","cProfile","-s","cumtime",str(p)]
    cp=subprocess.run(cmd,cwd=str(WORKSPACE),capture_output=True,text=True,timeout=180)
    funcs=[]
    for line in cp.stdout.splitlines():
        parts=line.split(None,5)
        if len(parts)>=6 and parts[0].replace('/','').isdigit():
            try: funcs.append({"calls":parts[0],"tottime":float(parts[1]),"cumtime":float(parts[3]),"func":parts[5]})
            except Exception: pass
        if len(funcs)>=top: break
    return jsonify(top_funcs=funcs, error=cp.stderr if cp.returncode else "")

@app.get("/api/run/history")
def run_history(): return jsonify(history=load_json(RUN_HISTORY_FILE, []))
@app.post("/api/run/history/clear")
def run_history_clear(): save_json(RUN_HISTORY_FILE, []); return jsonify(ok=True)

def add_run_history(item):
    hist=load_json(RUN_HISTORY_FILE, []); hist.append(item); save_json(RUN_HISTORY_FILE, hist[-100:])

@socketio.on("run_script")
def sock_run(data):
    start=time.time(); label=data.get("path") or "selection"
    emit("run_start", {"label": label})
    try:
        proc=run_python_file(safe_path(data.get("path")) if data.get("path") else None, data.get("code"), data.get("args", []))
        for line in proc.stdout:
            emit("run_output", {"line": line})
        rc=proc.wait()
        add_run_history({"label":label,"returncode":rc,"duration":round(time.time()-start,2),"timestamp":datetime.utcnow().isoformat()})
        emit("run_done", {"returncode": rc})
    except Exception as e:
        emit("run_error", {"message": str(e)})

@socketio.on("capture_plots")
def sock_plots(data):
    before={p for p in (WORKSPACE/"exports").glob("*.png")}
    sock_run({"path": data.get("path"), "args": []})
    after=list((WORKSPACE/"exports").glob("*.png"))
    plots=[]
    for p in after:
        if p.exists(): plots.append({"path":relpath(p),"data":base64.b64encode(p.read_bytes()).decode()})
    emit("plots_ready", {"plots": plots, "count": len(plots)})

@socketio.on("terminal_cmd")
def sock_terminal(data):
    cmd=data.get("cmd","")
    low = cmd.strip().lower()
    if not policy_allowed("allow_terminal"):
        log_event("terminal.cmd", cmd[:120], "blocked", {"reason": "terminal_disabled"})
        emit("terminal_output", {"line": "Terminal blocked by enterprise policy\n", "type": "stderr"})
        emit("terminal_done", {"returncode": 403})
        return
    if (low.startswith("pip install") or " python -m pip install" in low or low.startswith("python -m pip install")) and not policy_allowed("allow_pip_install"):
        log_event("terminal.cmd", cmd[:120], "blocked", {"reason": "pip_disabled"})
        emit("terminal_output", {"line": "pip install blocked by enterprise policy\n", "type": "stderr"})
        emit("terminal_done", {"returncode": 403})
        return
    log_event("terminal.cmd", cmd[:120], "ok")
    proc=subprocess.Popen(cmd, cwd=str(WORKSPACE), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout: emit("terminal_output", {"line": line, "type": "stdout"})
    emit("terminal_done", {"returncode": proc.wait()})

@socketio.on("kill_process")
def sock_kill():
    emit("process_killed")

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=False)
