## Quick start

```bash
# 1) Create and activate a virtual environment
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

# 2) Install dev dependencies
python -m pip install --upgrade pip
pip install -r requirements-dev.txt

# 3) Open project in VS Code and select the .venv interpreter
code .

# (VS Code will also prompt to install the recommended extensions)

# 4) Verify tools
ruff check .
black --check .
