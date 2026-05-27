# VSCode Stimulator — Feature Guide

This document explains the platform features in clear terms for users, recruiters, schools, collaborators and GitHub visitors.

## 1. Explorer
The Explorer is the file-management centre of the system. It allows the user to create files, create folders, open files, rename items, delete items, upload datasets and download files. This gives a tablet user a project workspace similar to VS Code.

## 2. Editor
The editor is powered by CodeMirror. It supports syntax highlighting, line numbers, active-line highlighting, bracket matching, auto-closing brackets, folding and configurable font size. It supports Python, Markdown, SQL, JavaScript, R, JSON and shell-like scripts.

## 3. Python Execution
The Run button sends the active Python file to the Flask backend. The backend executes it with the local Python interpreter and streams output back to the browser using Socket.IO. This keeps the tool free because no paid cloud notebook or AI API is required.

## 4. Run Selection
The user can highlight a portion of code and run only that selection. This is useful for tutoring, live debugging and quick experimentation.

## 5. Terminal
The terminal lets the user run shell commands through the backend. This is helpful for Git commands, package installation, file checks and project automation.

## 6. Output
The Output panel shows results from executed Python scripts. It separates normal workflow from terminal commands.

## 7. Problems
The Problems panel performs basic Python syntax checking and reports line numbers. It is designed as a lightweight beginner-friendly debugging aid.

## 8. Plots
The Plots panel helps data scientists and students view generated Matplotlib charts. Generated PNG files can be displayed and downloaded.

## 9. Inspector
The Inspector runs a script and returns variable names, types and values. This is useful for teaching Python because learners can see what each object becomes after execution.

## 10. Profiler
The Profiler uses Python's cProfile functionality to show function calls and runtime bottlenecks. It supports performance thinking without needing a separate profiling tool.

## 11. CSV Data Viewer
The CSV viewer previews dataset rows and columns in the browser. It includes search/filter functionality, making it useful for quick data inspection.

## 12. Source Control
The Git sidebar supports common GitHub workflows: initialise repository, view changes, commit, set remote, push, pull, branch, stash and view diffs.

## 13. Package Manager
The Package Manager lists installed packages, checks outdated packages and can call pip install through the backend terminal.

## 14. Snippets
Snippets allow repeated code patterns to be saved with name, language, description and tags. This is ideal for Pandas templates, ML pipelines and teaching examples.

## 15. Notebook
The notebook panel provides simple code and Markdown cells. It is not a full Jupyter replacement, but it is useful for quick lessons and experiments.

## 16. Markdown Preview
The Markdown panel renders documentation inside the platform. This helps when writing README files, lesson notes and deployment instructions.

## 17. Chart Builder
The Chart Builder creates charts through a form. It helps users produce quick visuals without writing Python code.

## 18. Task Manager
The task manager stores project tasks locally in the browser with priority levels and filters.

## 19. Pomodoro Timer
A built-in timer supports focused study and development sessions.

## 20. Calculator
A quick calculator supports arithmetic expressions during analysis or teaching.

## 21. Workspace Stats
Workspace statistics show total files, file sizes, extension distribution and recent changes.

## 22. Environment Manager
The environment manager creates and edits `.env` variables for scripts and backend commands.

## 23. File History
Each save can generate a snapshot so older versions can be restored.

## 24. Offline Preview
When the backend is not running, the interface still opens for preview. Backend features such as Python execution and Git require the server.

## 25. Free-Tool Philosophy
The system is intentionally built with free/open tools: Flask, Socket.IO, CodeMirror, Chart.js, marked.js, GitHub, Render free tier, Cloudflare Pages/GitHub Pages and Termux. It avoids paid AI APIs at runtime.

## 26. Command Palette
VSCode Stimulator includes a VS Code-like command palette opened with `Ctrl+Shift+P`. It centralises common commands such as running files, opening panels, switching themes, starting tools and accessing the feature guide.

## 27. Outline Panel
The Outline panel parses the active editor content and displays symbols such as Python classes, Python functions, imports, JavaScript functions and Markdown headings. This helps users navigate long files quickly.

## 28. Run and Debug Panel
The Run and Debug panel mimics VS Code's run configuration workflow. It provides launch options for normal Python execution, selected-code execution, plot capture, variable inspection and profiling. It also includes lightweight browser breakpoints for teaching and planning.

## 29. Extensions Panel
The Extensions panel mimics the VS Code extension experience using local built-in extension packs. It avoids paid APIs and external marketplace dependency while still letting users personalise the environment.

## 30. VS Code Layout Matching
The system now more closely follows VS Code by combining: Activity Bar, Side Bar, Explorer, Search, Source Control, Run and Debug, Extensions, Editor Groups, Tabs, Breadcrumbs, Problems, Output, Terminal, Status Bar, Command Palette and Settings.

## 31. Tablet Upload & Deployment Center
A dedicated deployment panel explains how to upload the complete project from an itel Vista Tab 30s to GitHub. It includes GitHub web upload steps, Termux Git commands, static deployment guidance and Render backend deployment guidance.

## 32. PWA Support
The project includes a web app manifest and service worker. This improves Android browser installation and static caching where supported.

## 33. Live Preview Panel
The Live Preview panel displays active HTML, Markdown, SVG or text files inside an iframe. It supports quick front-end preview without paid services.

## 34. REST Client Panel
The REST Client panel allows free API testing from the browser using fetch. Users can choose request method, enter URL, add JSON headers, send a body and inspect the response.

## 35. TODO Scanner
The TODO scanner searches for TODO, FIXME, BUG, HACK and NOTE comments across the workspace through the backend or across open tabs in offline mode.

## 36. Workspace ZIP Export
The workspace ZIP export downloads the current workspace as a zip file, helping tablet users back up and transfer work before GitHub upload.

## 37. Keyboard Shortcuts Reference
A dedicated shortcuts modal lists the most important VS Code-like keyboard commands.

## 38. Expert-Level VS Code Mimicry
At this level, the system includes Activity Bar, Explorer, Search, Source Control, Run and Debug, Extensions, Command Palette, Outline, Tabs, Breadcrumbs, Split View, Problems, Output, Terminal, Status Bar, Settings, Shortcuts, Live Preview, Markdown Preview, REST Client and TODO Scanner.

## 39. Enterprise Center
The Enterprise Center provides optional password protection, audit logs, project health, enterprise policy JSON, Prometheus-style metrics and full-project backup. These features are implemented with free Flask/Python tooling and require no AI API.

## 40. Optional Docker Deployment
Dockerfile and docker-compose support are included for local or self-hosted deployment. This gives a more enterprise-style deployment workflow without paid services.

## 41. GitHub Actions Static Checks
A free GitHub Actions workflow validates backend Python syntax and manifest JSON on push or pull request.
