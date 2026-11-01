import json
from pathlib import Path

def main():
    base=Path(__file__).resolve().parent
    for name in ("ai_vs_traditional.log","google_search_results.json","ai_comparison_results.json"):
        path=base/name
        print(f"{name}: {'created' if path.exists() else 'not created'}")
    comparison=base/"ai_comparison_results.json"
    if comparison.exists():
        data=json.loads(comparison.read_text(encoding="utf-8"))
        for group in ("ai_results","traditional_results"):
            items=data.get(group,[])
            print(f"{group}: {sum(x.get('success',False) for x in items)}/{len(items)} successful")
    search=base/"google_search_results.json"
    if search.exists():
        data=json.loads(search.read_text(encoding="utf-8"))
        print("Search query:",data.get("search_query"),"Results:",data.get("results_count",0))

if __name__=="__main__":
    main()
