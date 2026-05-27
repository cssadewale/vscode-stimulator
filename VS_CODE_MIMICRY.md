# VS Code Mimicry Map — VSCode Stimulator

VSCode Stimulator is not Microsoft VS Code and does not use VS Code source code. It is a free, browser-based system designed to mimic the practical layout, workflow and developer experience of VS Code for tablet-first coding and data science.

## Layout Equivalence

| VS Code Concept | VSCode Stimulator Implementation |
|---|---|
| Title Bar | Top application bar with brand, File/Edit/Run controls and quick actions |
| Activity Bar | Left vertical icon bar for Explorer, Search, Source Control, Run/Debug, Extensions and tools |
| Side Bar | Context panel that changes based on Activity Bar selection |
| Explorer | Workspace file tree with create, upload, rename, delete and download controls |
| Search | Search and replace interface for open files |
| Source Control | Git status, commit, diff, branch, stash, push and pull controls |
| Run and Debug | Run configurations, start/stop, plot run, inspector run, profiler run and lightweight breakpoints |
| Extensions | Local built-in feature packs instead of paid/external marketplace plugins |
| Editor Tabs | Multi-file tab bar with modified-file indicators |
| Breadcrumbs | Current file path display above editor |
| Editor | CodeMirror editor with syntax highlighting, line numbers and shortcuts |
| Split Editor | Secondary editor pane for side-by-side code viewing |
| Command Palette | Ctrl+Shift+P command launcher |
| Problems | Syntax/lint issue display |
| Output | Script output panel |
| Terminal | Browser terminal connected to Flask backend |
| Status Bar | Branch, Python, run state, CPU/RAM, cursor, language and encoding indicators |
| Settings | Modal settings interface |
| Keyboard Shortcuts | Dedicated keyboard shortcut reference |
| Markdown Preview | README/Markdown preview panel |
| Live Preview | HTML/SVG/Markdown/text live preview iframe |
| REST Client | Free API-testing panel similar to VS Code REST extensions |
| TODO Scanner | Workspace marker scanner for TODO, FIXME, BUG, HACK and NOTE |

## Functional Equivalence

### Coding
- Create and open files.
- Edit multiple files in tabs.
- Syntax highlight common languages.
- Use find/replace.
- Save files through backend.
- Download files and workspace content.

### Python/Data Science
- Run Python files.
- Run selected code.
- Capture Matplotlib plots.
- Inspect variables after execution.
- Profile scripts.
- Preview CSV files.
- Use notebook-like cells.

### Project Management
- Git operations.
- Tasks.
- TODO scanner.
- Snippets.
- Workspace statistics.
- File history snapshots.

### Web Development
- HTML live preview.
- Markdown preview.
- Chart builder.
- REST client.

### Deployment
- Static demo via GitHub Pages or Cloudflare Pages.
- Full backend via Render free tier.
- Local/tablet backend via Termux.

## Free Tool Policy

The platform uses free/open tools:

- HTML, CSS and JavaScript
- CodeMirror
- Chart.js
- marked.js
- Flask
- Flask-SocketIO
- Python
- Git
- GitHub
- Render free tier
- GitHub Pages
- Cloudflare Pages
- Termux

No paid AI API is required or used.
