#!/usr/bin/env bash
set -u
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
REPORTS="$ROOT/reports"
mkdir -p "$REPORTS"
RESULTS="$REPORTS/ci-results.txt"
now="$(date '+%Y-%m-%d %H:%M:%S %z')"
latest="$(find "$REPORTS" -maxdepth 1 -type f -name 'junit-*.xml' -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)"
if [[ -z "$latest" ]]; then
  printf '[%s] ERROR - No JUnit report found\n' "$now" | tee -a "$RESULTS"
  exit 1
fi
if python3 - "$latest" <<'PYCODE'
import sys
import xml.etree.ElementTree as ET
root = ET.parse(sys.argv[1]).getroot()
suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
failed = sum(int(s.attrib.get("failures", 0)) + int(s.attrib.get("errors", 0)) for s in suites)
raise SystemExit(0 if failed == 0 else 1)
PYCODE
then
  printf '[%s] SUCCESS - No test failures recorded in %s\n' "$now" "$(basename "$latest")" | tee -a "$RESULTS"
else
  printf '[%s] FAILURE - Test failures recorded in %s\n' "$now" "$(basename "$latest")" | tee -a "$RESULTS"
  exit 1
fi
