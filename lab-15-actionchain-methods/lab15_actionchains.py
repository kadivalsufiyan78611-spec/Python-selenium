import logging
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOG = Path("actionchain_methods.log")
logging.basicConfig(filename=LOG, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", filemode="w")

class ActionChainLab:
    def __init__(self):
        options = Options()
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def test_send_keys(self):
        self.driver.get("https://the-internet.herokuapp.com/key_presses")
        target = self.wait.until(EC.element_to_be_clickable((By.ID, "target")))
        actions = ActionChains(self.driver)
        for key, label in [(Keys.ENTER, "ENTER"), (Keys.SPACE, "SPACE"), (Keys.TAB, "TAB"), (Keys.ESCAPE, "ESCAPE"), ("A", "A"), ("1", "1")]:
            target.click()
            actions.send_keys(key).perform()
            result = self.wait.until(EC.visibility_of_element_located((By.ID, "result"))).text
            print(f"{label}: {result}")
            logging.info("Key %s produced %s", label, result)

    def test_drag_and_drop(self):
        self.driver.get("https://demoqa.com/dragabble")
        item = self.wait.until(EC.element_to_be_clickable((By.ID, "dragBox")))
        before = item.location
        ActionChains(self.driver).click_and_hold(item).move_by_offset(100, 50).release().perform()
        time.sleep(1)
        after = item.location
        print(f"Drag position: {before} -> {after}")
        logging.info("Drag position changed from %s to %s", before, after)
        ActionChains(self.driver).drag_and_drop_by_offset(item, -50, -25).perform()

    def test_ctrl_click(self):
        html = """<!doctype html><html><head><meta charset="utf-8"><title>Multi Select</title>
<style>.item{padding:12px;margin:6px;border:2px solid #aaa;cursor:pointer}.selected{background:#1769aa;color:white}</style>
<script>function toggleItem(el,event){if(event.ctrlKey||event.metaKey){el.classList.toggle('selected')}else{document.querySelectorAll('.item').forEach(x=>x.classList.remove('selected'));el.classList.add('selected')}}</script>
</head><body><h2>Multiple Selection Test</h2><p>Use CTRL or Command and click.</p>
<div class="item" onclick="toggleItem(this,event)">Item 1</div><div class="item" onclick="toggleItem(this,event)">Item 2</div>
<div class="item" onclick="toggleItem(this,event)">Item 3</div><div class="item" onclick="toggleItem(this,event)">Item 4</div>
<div class="item" onclick="toggleItem(this,event)">Item 5</div></body></html>"""
        page = Path("multiple_selection.html").resolve()
        page.write_text(html, encoding="utf-8")
        self.driver.get(page.as_uri())
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item")))
        actions = ActionChains(self.driver)
        actions.click(items[0]).key_down(Keys.CONTROL).click(items[1]).click(items[2]).click(items[4]).key_up(Keys.CONTROL).perform()
        selected = [element.text for element in self.driver.find_elements(By.CSS_SELECTOR, ".item.selected")]
        print("Selected items:", selected)
        logging.info("Selected items: %s", selected)
        assert len(selected) == 4, f"Expected 4 selected items, found {len(selected)}"

    def run(self):
        try:
            self.test_send_keys()
            self.test_drag_and_drop()
            self.test_ctrl_click()
            print("ActionChain scenarios finished. Review the log for details.")
        except Exception:
            logging.exception("ActionChain lab failed")
            raise
        finally:
            self.driver.quit()

if __name__ == "__main__":
    ActionChainLab().run()
