import logging
import os
import time
from seleniumbase import BaseCase

class AILocatorDemo(BaseCase):
    def setUp(self):
        super().setUp()
        logging.basicConfig(filename="ai_vs_traditional.log",level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
        self.logger=logging.getLogger(__name__)

    def test_ai_form_interaction(self):
        if not os.getenv("OPENAI_API_KEY"):
            self.skipTest("Set OPENAI_API_KEY to run AI locator tests.")
        self.open("https://the-internet.herokuapp.com/login")
        started=time.perf_counter()
        self.ai_type("the username input field","tomsmith")
        self.ai_type("the password input field","SuperSecretPassword!")
        self.ai_click("the login button")
        self.assert_text("You logged into a secure area!")
        self.logger.info("AI login passed in %.3fs",time.perf_counter()-started)

    def test_traditional_form_interaction(self):
        self.open("https://the-internet.herokuapp.com/login")
        started=time.perf_counter()
        self.type("#username","tomsmith")
        self.type("#password","SuperSecretPassword!")
        self.click("button[type='submit']")
        self.assert_text("You logged into a secure area!")
        self.logger.info("Traditional login passed in %.3fs",time.perf_counter()-started)

if __name__=="__main__":
    from seleniumbase import pytest
    pytest.main([__file__,"-v","-s"])
