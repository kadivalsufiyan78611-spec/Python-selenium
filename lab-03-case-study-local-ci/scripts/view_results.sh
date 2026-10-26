#!/usr/bin/env bash
set -u
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
REPORTS="$ROOT/reports"

if [[ ! -d "$REPORTS" ]]; then
  printf '%s\n' 'No reports directory found. Run the test suite first.'
  exit 1
fi

printf '%s\n' '=== Available test artifacts ==='
find "$REPORTS" -maxdepth 1 -type f \( -name 'junit-*.xml' -o -name 'report-*.html' -o -name 'screenshot-*.png' \) -printf '%f\n' 2>/dev/null | sort
latest="$(find "$REPORTS" -maxdepth 1 -type f -name 'junit-*.xml' -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)"
if [[ -n "$latest" ]]; then
  printf 'Latest JUnit XML: %s\n' "$latest"
  if command -v python3 >/dev/null 2>&1; then
    python3 - "$latest" <<'PYCODE'
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
path = Path(sys.argv[1])
root = ET.parse(path).getroot()
suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
keys = ("tests", "failures", "errors", "skipped")
summary = {key: sum(int(suite.attrib.get(key, 0)) for suite in suites) for key in keys}
print("Summary: " + ", ".join(f"{key}={value}" for key, value in summary.items()))
PYCODE
  fi
fi
