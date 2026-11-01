import json
import statistics
from pathlib import Path

base=Path(__file__).resolve().parent
path=base/"performance_comparison.json"
if not path.exists():
    raise SystemExit("Run lab8_traditional_locators.py first.")
data=json.loads(path.read_text(encoding="utf-8"))
lines=["# Locator Performance Report","","Timings are local observations, not universal rankings.","",f"Scenarios tested: {len(data)}",""]
for item in data:
    lines.extend([f"## {item['scenario']}",f"- CSS median: {item['css']['median_seconds']:.6f}s ({item['css']['elements_found']} elements)",f"- XPath median: {item['xpath']['median_seconds']:.6f}s ({item['xpath']['elements_found']} elements)",f"- Counts match: {item['counts_match']}",f"- Faster in this run: {item['faster_in_this_run']}",""])
for method in ("css","xpath"):
    values=[item[method]["median_seconds"] for item in data if item[method]["success"]]
    lines.append(f"{method.upper()} mean of scenario medians: {statistics.mean(values):.6f}s" if values else f"{method.upper()} measurements unavailable")
report="\n".join(lines)
(base/"performance_report.md").write_text(report,encoding="utf-8")
print(report)
