# Contributing to VSCode Stimulator

Thank you for considering a contribution.

## Principles

1. Preserve all existing features unless a change is clearly necessary.
2. Keep the platform free-tool friendly.
3. Do not introduce paid AI API dependencies.
4. Keep tablet/mobile usability in mind.
5. Document every major feature clearly.
6. Prefer simple, understandable code over unnecessary complexity.

## Development Setup

```bash
git clone https://github.com/cssadewale/vscode-stimulator.git
cd vscode-stimulator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python backend/app.py
```

Open `http://localhost:5000`.

## Pull Request Checklist

- [ ] Feature is documented in `README.md` or `FEATURES.md`.
- [ ] No paid API key is required.
- [ ] Existing UI features still work.
- [ ] No private credentials are committed.
- [ ] Mobile/tablet layout is considered.

## Contact

Adewale Samson Adeagbo  
GitHub: <https://github.com/cssadewale>  
LinkedIn: <https://linkedin.com/in/adewalesamsonadeagbo>
