import os
from seleniumbase import BaseCase

class AdvancedAILocators(BaseCase):
    def test_contextual_button(self):
        if not os.getenv("OPENAI_API_KEY"):
            self.skipTest("Set OPENAI_API_KEY to run AI examples.")
        self.open("https://the-internet.herokuapp.com/challenging_dom")
        self.ai_click("the blue button")
        self.assert_element("table")

    def test_semantic_dropdown(self):
        if not os.getenv("OPENAI_API_KEY"):
            self.skipTest("Set OPENAI_API_KEY to run AI examples.")
        self.open("https://the-internet.herokuapp.com/dropdown")
        self.ai_select("the dropdown menu","Option 1")
        self.assert_selected_option("select","Option 1")

    def test_dynamic_control_wait(self):
        self.open("https://the-internet.herokuapp.com/dynamic_controls")
        self.click("button")
        self.wait_for_text("It's gone!",timeout=10)
        self.assert_text("It's gone!")

if __name__=="__main__":
    from seleniumbase import pytest
    pytest.main([__file__,"-v","-s"])
