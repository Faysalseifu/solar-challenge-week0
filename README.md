# solar-challenge-week0
10 Academy: Artificial Intelligence Mastery Solar Data Discovery: Week 0 Challenge

## Reproducing the environment

These instructions assume a Bash shell (the default here is `bash.exe` on Windows). Run the following from the repository root.

1. Create and activate a virtual environment (venv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Run tests (if added):

```bash
pytest -q
```

## Branching and PRs

Create a branch for this setup work and push to GitHub:

```bash
git checkout -b setup-task
git add .
git commit -m "init: add .gitignore"
git commit -m "chore: venv setup"
git commit -m "ci: add GitHub Actions workflow"
git push -u origin setup-task
```

Open a Pull Request on GitHub to merge `setup-task` into `main` and use the web UI to merge.

## Continuous Integration

This repository includes a minimal GitHub Actions workflow at `.github/workflows/ci.yml` that installs dependencies and prints the Python version. CI will run on pushes and PRs.

## Project layout

Suggested layout (some folders already present):

```
.vscode/
.github/
.gitignore
requirements.txt
README.md
src/
notebooks/
tests/
scripts/
```
