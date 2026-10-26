import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    junit = REPORTS / f"junit-{timestamp}.xml"
    html = REPORTS / f"report-{timestamp}.html"
    command = [
        sys.executable,
        "-m",
        "pytest",
        "--junitxml",
        str(junit),
        "--html",
        str(html),
        "--self-contained-html",
    ]
    print(f"Running: {' '.join(command)}", flush=True)
    result = subprocess.run(command, cwd=ROOT, check=False)
    print(f"Pytest exit code: {result.returncode}")
    print(f"JUnit report: {junit}")
    print(f"HTML report: {html}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
