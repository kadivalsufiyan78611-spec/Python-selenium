import json
import os
import time
from pathlib import Path
from seleniumbase import BaseCase

class LocatorComparison(BaseCase):
    def run_form(self,use_ai):
        result={"approach":"AI" if use_ai else "Traditional","success":False,"duration_seconds":0,"error":None}
        started=time.perf_counter()
        try:
            self.open("https://the-internet.herokuapp.com/login")
            if use_ai:
                self.ai_type("username input field","tomsmith")
                self.ai_type("password input field","SuperSecretPassword!")
                self.ai_click("login button")
            else:
                self.type("#username","tomsmith")
                self.type("#password","SuperSecretPassword!")
                self.click("button[type='submit']")
            self.assert_text("You logged into a secure area!")
            result["success"]=True
        except Exception as exc:
            result["error"]=str(exc)
        result["duration_seconds"]=time.perf_counter()-started
        return result

    def test_compare_login_locators(self):
        traditional=self.run_form(False)
        ai=self.run_form(True) if os.getenv("OPENAI_API_KEY") else {"approach":"AI","success":False,"duration_seconds":0,"error":"OPENAI_API_KEY not configured"}
        data={"traditional_results":[traditional],"ai_results":[ai]}
        Path("ai_comparison_results.json").write_text(json.dumps(data,indent=2),encoding="utf-8")
        print(json.dumps(data,indent=2))

if __name__=="__main__":
    from seleniumbase import pytest
    pytest.main([__file__,"-v","-s"])
