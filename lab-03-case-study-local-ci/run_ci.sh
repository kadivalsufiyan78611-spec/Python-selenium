#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

printf '%s\n' '=== Local Selenium CI ==='
python_bin="${PYTHON:-python3}"
if ! command -v "$python_bin" >/dev/null 2>&1; then
  printf 'Python executable not found: %s\n' "$python_bin" >&2
  exit 127
fi
"$python_bin" --version

if ! "$python_bin" -m pip show pytest >/dev/null 2>&1; then
  printf '%s\n' 'Dependencies are missing. Activate your virtual environment and run: python -m pip install -r requirements.txt' >&2
  exit 2
fi

printf '%s\n' 'Checking Python syntax...'
if ! "$python_bin" -m compileall -q pages tests conftest.py run_tests.py; then
  printf '%s\n' 'Syntax check failed.' >&2
  exit 1
fi

printf '%s\n' 'Running browser tests and generating reports...'
"$python_bin" run_tests.py
status=$?
printf 'CI finished with exit code %s\n' "$status"
exit "$status"
