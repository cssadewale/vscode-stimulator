# VSCode Stimulator

**A tablet-first, VS Code-like Python and data-science workspace built by Adewale Samson Adeagbo.**

VSCode Stimulator is a browser-based IDE designed for people who do serious coding, teaching, data analysis and EdTech building without always having access to a laptop. It keeps the familiar VS Code workflow—file explorer, tabs, syntax highlighting, terminal, Git controls, runner, output panels, snippets and project tools—but is intentionally built around free and open tools.

> **No paid AI API is required.** The platform uses normal Python execution, Flask, Socket.IO, CodeMirror, Chart.js, marked.js, Git, GitHub and free-tier hosting options.

---

## Creator

**Adewale Samson Adeagbo**  
**Data Scientist | EdTech Builder | Virtual Tutor | AI-Augmented Solutions Developer**

- Portfolio: <https://cssadewale.pages.dev>
- LinkedIn: <https://linkedin.com/in/adewalesamsonadeagbo>
- GitHub: <https://github.com/cssadewale>
- HMG Academy: <https://hmgacademy.pages.dev>
- HMG Concepts: <https://hmgconcepts.pages.dev>
- WhatsApp / Phone: **+234 810 086 6322**
- Alternative phone: **+234 809 448 1488**

Adewale is a Nigerian educator, data scientist and EdTech builder with **15+ years of classroom teaching experience** across nursery, primary and secondary education in Lagos and Ogun State. He founded **HMG Concepts** in 2015 and leads work across virtual education, CBT systems, data-science training, ML-powered EdTech tools and educational media. His public work includes CBT Pro, Student Performance Tracker, CBT Question Bank Manager, Fake News Detector, insurance claim prediction, churn prediction, burnout prediction, delivery-delay prediction and student-risk modelling.

---

For a direct VS Code feature comparison, see [`VS_CODE_MIMICRY.md`](VS_CODE_MIMICRY.md).

---

## Why This Exists

Adewale worked mostly on an Android tablet and rarely had access to a full computer. Instead of waiting for perfect conditions, he built a system that mimics much of the VS Code workflow in the browser:

- edit code from a tablet;
- run Python through a free backend;
- inspect data and variables;
- manage GitHub projects;
- write Markdown documentation;
- view CSV files;
- build charts;
- teach and demonstrate code clearly;
- deploy with free tools.

The project reflects the same philosophy behind HMG Concepts: **Learning Deliberately. Teaching Authentically.**

---

## Major Features

### 1. VS Code-like Interface

The UI includes a title bar, activity bar, command palette, sidebar, tabbed editor, breadcrumb, bottom panel, status bar, modals, context menus, keyboard shortcuts, outline view, run/debug view and extension-like panels. It is designed to feel familiar to anyone who has used VS Code while remaining usable on tablets.

### 2. File Explorer

Create, rename, delete, upload, download and open files inside a safe workspace directory. The file tree recognises common file types such as Python, Markdown, CSV, JSON, SQL, R, images and shell scripts.

### 3. Code Editor

The editor uses **CodeMirror 5** and supports:

- Python, Markdown, SQL, JavaScript, R and shell highlighting;
- line numbers;
- active-line highlight;
- bracket matching;
- auto-close brackets;
- code folding;
- comments;
- find/replace;
- font-size settings;
- tab-size settings;
- word wrap.

### 4. Python Runner

Run the active Python file using the Flask backend. Output streams live to the browser through Socket.IO.

Shortcut: **F5**

### 5. Run Selection

Highlight a block of Python code and run only that selection. This is useful for teaching, debugging and experimenting.

### 6. Terminal

Run shell commands from the browser when the backend server is active. It supports command history and multiple visual terminal tabs.

### 7. Output Panel

Displays standard output and error messages from executed scripts.

### 8. Problems Panel

Performs basic syntax checking and shows errors with line numbers. Clicking a problem moves the cursor to the relevant line.

### 9. Plot Capture

Runs Python scripts configured for Matplotlib and displays generated PNG charts from the `workspace/exports` folder. This is useful for data-science reports, teaching and quick visual checks.

Shortcut: **F6**

### 10. Variable Inspector

Runs a Python script and shows user-created variables with their type and value representation. This helps learners understand what their code produced.

Shortcut: **F7**

### 11. Profiler

Uses Python profiling to reveal slow functions, call counts, total time and cumulative time.

Shortcut: **F8**

### 12. CSV Data Viewer

Open and preview CSV files in a scrollable, searchable table. This helps with quick dataset inspection before modelling.

### 13. Git Tools

The Source Control sidebar supports:

- `git init`;
- status view;
- commit;
- remote configuration;
- push;
- pull;
- diff viewer;
- branch manager;
- stash and pop.

### 14. Package Manager

Lists installed Python packages and can run `pip install` through the backend terminal. It also checks outdated packages.

### 15. Snippet Library

Save selected code or complete files as reusable snippets with name, description, language and tags. Insert snippets back into the editor later.

### 16. Notebook Panel

A lightweight notebook-style panel for code and Markdown cells. It supports:

- code cells;
- Markdown cells;
- run one cell;
- run all cells;
- clear outputs;
- export code cells as `.py`.

### 17. Markdown Preview

Render active `.md` files as formatted HTML inside the IDE. This is useful when writing `README.md`, lesson notes, deployment guides and documentation.

### 18. Chart Builder

Build simple charts without writing Python. Supports bar, line, pie, doughnut and scatter-style data entry through Chart.js. Download chart output as PNG.

### 19. Task Manager

Local browser task manager with priorities and filters. Useful for lesson planning, project milestones, deployment checklists and GitHub upload preparation.

### 20. Pomodoro Timer

A built-in work/break timer for focused coding sessions on mobile devices.

### 21. Calculator

A safe quick calculator for simple arithmetic expressions.

### 22. Workspace Statistics

Shows number of files, size distribution, file types and recent files.

### 23. Environment Manager

Create and manage `.env` variables that can be used by scripts and commands.

### 24. File Version Snapshots

Every file save can create a snapshot in `workspace/.history`, allowing restoration of previous versions.

### 25. Offline / Preview Mode

The UI can open as a static file for preview, but Python execution, terminal commands, Git and filesystem actions require the Flask backend.

### 26. Command Palette

A VS Code-style **Ctrl+Shift+P** command launcher is included. It allows users to start actions such as Run File, Run Selection, Markdown Preview, Chart Builder, Toggle Theme, Focus Mode, Git panel, Extensions panel and Feature Guide without searching through menus.

### 27. Outline Panel

The Outline panel scans the active file and lists functions, classes, imports, JavaScript functions and Markdown headings. Clicking an outline item jumps directly to the relevant line, similar to VS Code's Outline view.

### 28. Run and Debug Panel

The Run and Debug panel gives a VS Code-like execution area with launch configurations for:

- Python current file;
- Python selection;
- plot capture;
- variable inspection;
- profiling.

It also includes lightweight browser breakpoints for planning/debugging lessons. The actual execution still uses the free Flask backend.

### 29. Local Extension Packs

The Extensions panel mimics VS Code's extension workflow without depending on a paid marketplace. Built-in free packs include Python Essentials, Data Science Pack, Markdown Writer, GitHub Workflow, Notebook Lite, Teaching Toolkit and Tablet Productivity.

### 30. Tablet Upload & Deployment Center

A dedicated in-app deployment center explains how to upload the project from an **itel Vista Tab 30s** to GitHub using either GitHub web upload or Termux Git commands. It also explains when to use GitHub Pages, Cloudflare Pages and Render free tier.

### 31. PWA / Installable Web App Support

The project includes `manifest.json`, `service-worker.js` and `.nojekyll` so the interface can be installed or cached where supported by Android browsers and GitHub Pages.


### 32. Live Preview Panel

Preview active HTML, Markdown, SVG or text files directly inside the IDE. This mimics VS Code-style live preview workflows and is useful for front-end pages, documentation, demos and lesson materials.

### 33. REST Client Panel

A free built-in API testing panel inspired by VS Code REST Client extensions. It supports method selection, URL entry, JSON headers, request body, response status, timing and formatted JSON output. Browser CORS rules still apply.

### 34. TODO Scanner

Scans the workspace or open tabs for development markers such as `TODO`, `FIXME`, `BUG`, `HACK` and `NOTE`. This helps the platform behave like a project-management-aware code editor.

### 35. Workspace ZIP Export

Downloads the current workspace as a zip file from the Flask backend. This is useful for tablet users who want to back up project work before uploading to GitHub.

### 36. Keyboard Shortcuts Reference

A dedicated shortcuts window lists the VS Code-inspired keyboard commands available in the system.

### 37. Enterprise Center

The Enterprise Center adds optional password protection, audit logs, project health, policy JSON, Prometheus-style metrics and full-project backup while remaining free and API-key-free. See [`ENTERPRISE_FEATURES.md`](ENTERPRISE_FEATURES.md).

### 38. Docker / Container Deployment

The project includes `Dockerfile` and `docker-compose.yml` for local enterprise-style deployment on any machine that supports Docker. This is optional and free if run on your own hardware.


---

## Technology Stack

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- CodeMirror 5
- Chart.js
- marked.js
- Socket.IO client

### Backend

- Python
- Flask
- Flask-SocketIO
- Gunicorn
- Python subprocess execution
- Git CLI
- Optional libraries: Pandas, NumPy, Matplotlib, Scikit-learn, psutil

### Free Deployment / Workflow Tools

- GitHub
- GitHub Pages for static preview
- Render free tier for backend hosting
- Cloudflare Pages for static frontend preview
- Termux for Android local use
- Acode or any mobile code editor

---

## Project Structure

```text
vscode-stimulator/
├── index.html              # Main browser IDE interface
├── backend/
│   ├── __init__.py
│   └── app.py              # Flask + Socket.IO backend
├── workspace/
│   ├── projects/           # User Python projects
│   ├── datasets/           # CSV and data files
│   ├── exports/            # Generated plots/images
│   └── .history/           # Auto snapshots
├── requirements.txt        # Python dependencies
├── Procfile                # Render/Heroku-style start command
├── render.yaml             # Render blueprint
├── runtime.txt             # Python version hint
├── .gitignore
├── SECURITY.md
├── TABLET_GITHUB_UPLOAD.md
├── VS_CODE_MIMICRY.md
├── manifest.json
├── service-worker.js
├── .nojekyll
├── termux_setup.sh
├── start.sh
├── LICENSE
└── README.md
```

---

## Local Installation on a Computer

### Step 1 — Clone the repository

```bash
git clone https://github.com/cssadewale/vscode-stimulator.git
cd vscode-stimulator
```

### Step 2 — Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Start the backend

```bash
python backend/app.py
```

### Step 5 — Open the IDE

Visit:

```text
http://localhost:5000
```

---

## Android / Tablet Installation with Termux

This is the recommended route for a tablet-first workflow. For tablet-specific GitHub upload instructions, also read [`TABLET_GITHUB_UPLOAD.md`](TABLET_GITHUB_UPLOAD.md).

### Step 1 — Install Termux

Install Termux from **F-Droid**, not the outdated Play Store version.

### Step 2 — Update packages

```bash
pkg update && pkg upgrade -y
```

### Step 3 — Install Python and Git

```bash
pkg install python git -y
```

### Step 4 — Clone your repository

```bash
git clone https://github.com/cssadewale/vscode-stimulator.git
cd vscode-stimulator
```

### Step 5 — Install Python requirements

```bash
pip install -r requirements.txt
```

If heavy packages fail on Android, install the core packages first:

```bash
pip install Flask Flask-SocketIO python-socketio python-engineio gunicorn simple-websocket psutil
```

Then add data-science packages only when your device can handle them.

### Step 6 — Run the backend

```bash
python backend/app.py
```

### Step 7 — Open in your tablet browser

```text
http://127.0.0.1:5000
```

---

## Deployment Option A — Static Preview on GitHub Pages

Use this if you only want people to see the interface.

### What works

- UI preview
- editor interface
- modals
- static interactions
- feature guide
- documentation viewing if loaded in browser

### What will not work

- Python execution
- terminal commands
- Git operations
- package installation
- backend file operations

### Steps

1. Push the repository to GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the `main` branch.
5. Select `/root` as the folder.
6. Save.
7. Open the GitHub Pages URL after deployment completes.

---

## Deployment Option B — Full Backend on Render Free Tier

Use this if you want Python execution, terminal, Git and filesystem features online.

### Step 1 — Push to GitHub

```bash
git add .
git commit -m "Initial VSCode Stimulator release"
git branch -M main
git remote add origin https://github.com/cssadewale/vscode-stimulator.git
git push -u origin main
```

### Step 2 — Create a Render account

Go to:

```text
https://render.com
```

Sign in with GitHub.

### Step 3 — Create a new Web Service

1. Click **New +**.
2. Choose **Web Service**.
3. Select the GitHub repository.
4. Use these settings:

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn --worker-class gthread --threads 8 -w 1 backend.app:app --bind 0.0.0.0:$PORT --timeout 180
Plan: Free
```

### Step 4 — Add environment variables

Add:

```text
SECRET_KEY = any-long-random-string
WORKSPACE_ROOT = /opt/render/project/src/workspace
```

### Step 5 — Deploy

Click **Create Web Service** and wait for the build to finish.

### Step 6 — Open your Render URL

Render will provide a URL like:

```text
https://vscode-stimulator.onrender.com
```

Open it in your browser.

### Important Render free-tier notes

- The free service may sleep when inactive.
- First load after sleep can be slow.
- Runtime file changes may not be permanent after redeployment.
- Do not expose private tokens in public demos.

---

## Deployment Option C — Cloudflare Pages Static UI

Cloudflare Pages is excellent for free static hosting, but it cannot run the Python backend by itself.

1. Push repository to GitHub.
2. Go to Cloudflare Pages.
3. Create a new project from GitHub.
4. Build command: leave blank.
5. Output folder: `/`.
6. Deploy.

Use Cloudflare Pages for a public UI demo and Render/Termux for actual backend execution.

---

## Security Notice

This application can execute Python and shell commands. Use it carefully.

Recommended safety rules:

1. Do not expose a public instance without authentication.
2. Do not run untrusted code.
3. Do not paste GitHub tokens into shared screenshots.
4. Use a private Render service or local Termux instance for sensitive work.
5. Keep the workspace separate from important system folders.

---

## No AI API Policy

This project does **not** depend on paid AI APIs. It is built to remain cost-effective and usable with free tools. If AI is used during development, it is treated as a human workflow assistant, not as a runtime dependency.

---

## Suggested Repository Description

> Tablet-first VS Code-like Python and data-science IDE by Adewale Samson Adeagbo. Built with free tools, Flask, Socket.IO, CodeMirror and GitHub workflow support. No paid AI API required.

---

## License

MIT License. See [`LICENSE`](LICENSE).

---

## Acknowledgement

Built from the practical need to code, teach, analyse data and deploy EdTech solutions from a tablet—proof that clear thinking, disciplined learning and free tools can produce useful systems even without perfect hardware.


## Enterprise / Protected Render Deployment

To enable the enterprise login gate on Render, add this environment variable:

```text
IDE_PASSWORD = choose-a-strong-password
```

Also set:

```text
SECRET_KEY = generate-a-long-random-secret
WORKSPACE_ROOT = /opt/render/project/src/workspace
```

If `IDE_PASSWORD` is not set, the IDE remains open. This is convenient for local/tablet testing but not recommended for a public backend.


## Additional Enterprise Enhancements in This Folder

This `enterprise` package includes extra production-style files and controls:

- `ADMIN_OPERATIONS_GUIDE.md` — admin usage and incident response.
- `FREE_TOOLS_ARCHITECTURE.md` — free/open-source architecture explanation.
- `PLATFORM_DEPLOYMENT_MATRIX.md` — comparison of Termux, Render, Docker, GitHub Pages and other platforms.
- `ENTERPRISE_GITHUB_UPLOAD_CHECKLIST.md` — checklist before uploading from tablet to GitHub.
- `.dockerignore` — safer Docker builds.
- `netlify.toml` — static preview support for Netlify.

### Enforced enterprise policy controls

The backend now enforces policy for:

- terminal access;
- pip install access;
- Git push access;
- upload maximum file size;
- allowed upload file extensions.

These controls are configured in the Enterprise Center policy JSON.
