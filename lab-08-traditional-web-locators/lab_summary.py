import json
from pathlib import Path

base=Path(__file__).resolve().parent
print("LAB 8 - TRADITIONAL WEB ELEMENT LOCATORS")
for name in ("table_data.json","performance_comparison.json","locator_methods.json","locator_performance.log","performance_report.md"):
    path=base/name
    print(f"{name}: {'created' if path.exists() else 'missing'}")
table=base/"table_data.json"
if table.exists():
    data=json.loads(table.read_text(encoding="utf-8"))
    print("Headers:",len(data.get("headers",[])),"Data rows:",len(data.get("rows",[])))
comparison=base/"performance_comparison.json"
if comparison.exists():
    data=json.loads(comparison.read_text(encoding="utf-8"))
    print("Scenarios:",len(data),"Matching counts:",sum(x["counts_match"] for x in data))
