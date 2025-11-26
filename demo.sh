#!/usr/bin/env bash
set -euo pipefail

# Optional: activate virtualenv if present
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

python3 generate_data.py
python3 test_agent.py
