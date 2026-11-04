import csv
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler(BASE_DIR / "social_media.log", encoding="utf-8"),
                               logging.StreamHandler()])
logger = logging.getLogger(__name__)


class SocialMediaDemo:
    """Collect and annotate records on a public demo table; no real social account is used."""

    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1440,1000")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 12)
        self.records = []

    def simulate_profile_form(self):
        """Fill the public practice form with synthetic data; this is not account authentication."""
        url = "https://demo.seleniumeasy.com/input-form-demo.html"
        self.driver.get(url)
        fields = {
            "first_name": "Alex", "last_name": "Taylor", "email": "alex.taylor@example.test",
            "phone": "5551234567", "address": "100 Demo Street", "city": "Example City",
            "state": "CA", "zip": "90001"
        }
        for name, value in fields.items():
            element = self.wait.until(EC.visibility_of_element_located((By.NAME, name)))
            element.clear()
            element.send_keys(value)
        logger.info("Synthetic demo form populated; submit is intentionally skipped.")

    def collect_demo_posts(self, limit=5):
        """Treat rows in the training table as post-like records."""
        self.driver.get("https://demo.seleniumeasy.com/table-pagination-demo.html")
        table = self.wait.until(EC.presence_of_element_located((By.ID, "myTable")))
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows[:limit]:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 4:
                continue
            self.records.append({
                "title": cells[0].text.strip(),
                "author": cells[1].text.strip(),
                "content": cells[2].text.strip(),
                "location": cells[3].text.strip(),
                "captured_at_utc": datetime.now(timezone.utc).isoformat()
            })
        logger.info("Collected %d visible demo records.", len(self.records))

    def simulate_interactions(self):
        """Visually mark rows in the local browser; no likes, comments, or shares are submitted."""
        rows = self.driver.find_elements(By.CSS_SELECTOR, "#myTable tbody tr")
        for index, row in enumerate(rows[:min(5, len(rows))], start=1):
            self.driver.execute_script(
                "arguments[0].style.outline='2px solid #2b8a3e'; arguments[0].scrollIntoView({block:'center'});",
                row
            )
            logger.info("Marked demo row %d as an interaction simulation.", index)

    def scroll_page(self, attempts=3):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(attempts):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height <= last_height:
                break
            last_height = new_height
        self.driver.execute_script("window.scrollTo(0, 0)")

    def export_csv(self):
        path = OUTPUT_DIR / "demo_posts.csv"
        fields = ["title", "author", "content", "location", "captured_at_utc"]
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.records)
        logger.info("CSV written to %s", path)
        return path

    def run(self):
        try:
            self.simulate_profile_form()
            self.collect_demo_posts()
            self.simulate_interactions()
            self.scroll_page()
            return self.export_csv()
        finally:
            self.driver.quit()


if __name__ == "__main__":
    try:
        output = SocialMediaDemo().run()
        print(f"Completed. Output: {output}")
    except (TimeoutException, WebDriverException) as exc:
        logger.exception("Browser automation failed: %s", exc)
        raise
