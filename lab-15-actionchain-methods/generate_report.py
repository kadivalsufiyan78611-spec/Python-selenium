from datetime import datetime
from pathlib import Path


def analyze(path):
    file_path = Path(path)
    if not file_path.exists():
        return f"{path}: log not found; run its test script first."
    lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    info = sum(" INFO " in line for line in lines)
    warnings = sum(" WARNING " in line for line in lines)
    errors = sum(" ERROR " in line for line in lines)
    return f"{path}: {len(lines)} entries | INFO {info} | WARNING {warnings} | ERROR {errors}"


def main():
    report = ["ACTIONCHAIN LAB EXECUTION REPORT", f"Generated: {datetime.now().isoformat(timespec='seconds')}", ""]
    report.extend(analyze(name) for name in ["actionchain_methods.log", "extended_actionchain.log"])
    report.append("")
    report.append("Log counts are not proof that every browser assertion passed. Review console output and test failures.")
    output = "\n".join(report)
    Path("actionchain_lab_report.txt").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
