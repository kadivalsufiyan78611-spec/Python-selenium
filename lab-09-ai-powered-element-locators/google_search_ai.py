import json
import os
from datetime import datetime, timezone
from pathlib import Path
from seleniumbase import BaseCase

class GoogleSearchAI(BaseCase):
    def test_google_search_with_ai(self):
        if not os.getenv("OPENAI_API_KEY"):
            self.skipTest("Set OPENAI_API_KEY to enable AI locators.")
        query="artificial intelligence in web automation"
        self.open("https://www.google.com")
        self.ai_type("Google search input",query)
        self.press_keys("input[name='q']","\n")
        self.wait_for_element("h3",timeout=15)
        results=[]
        for heading in self.find_elements("h3")[:5]:
            title=heading.text.strip()
            if not title:
                continue
            try:
                link=heading.find_element("xpath","./ancestor::a[1]")
                url=link.get_attribute("href") or "N/A"
            except Exception:
                url="N/A"
            results.append({"rank":len(results)+1,"title":title,"url":url})
        payload={"search_query":query,"timestamp_utc":datetime.now(timezone.utc).isoformat(),"results_count":len(results),"results":results,"note":"Search markup and availability can change."}
        Path("google_search_results.json").write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding="utf-8")

if __name__=="__main__":
    from seleniumbase import pytest
    pytest.main([__file__,"-v","-s"])
