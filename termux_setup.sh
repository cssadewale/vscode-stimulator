#!/usr/bin/env bash
set -e

echo "========================================"
echo " VSCode Stimulator — Termux Setup"
echo "========================================"

pkg update -y
pkg upgrade -y
pkg install python git -y

python -m pip install --upgrade pip
pip install Flask Flask-SocketIO python-socketio python-engineio gunicorn simple-websocket psutil

# Scientific packages can be heavy on Android. Try them, but do not fail the setup if they are unavailable.
pip install numpy pandas matplotlib scikit-learn || true

mkdir -p workspace/projects workspace/datasets workspace/exports workspace/.history

cat > "$HOME/start_vscode_stimulator.sh" <<'EOF'
#!/usr/bin/env bash
cd "$(pwd)"
python backend/app.py
EOF
chmod +x "$HOME/start_vscode_stimulator.sh"

echo ""
echo "Setup complete."
echo "Start the IDE with:"
echo "  python backend/app.py"
echo "Then open:"
echo "  http://127.0.0.1:5000"
