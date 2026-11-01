import json
import logging
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE=Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s",handlers=[logging.FileHandler(BASE/"locator_performance.log"),logging.StreamHandler()])
log=logging.getLogger(__name__)

class WebElementLocator:
    def __init__(self):
        self.driver=None
        self.performance_data=[]
    def setup_driver(self):
        options=Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1440,1000")
        self.driver=webdriver.Chrome(options=options)
    def navigate_to_tables_page(self):
        self.driver.get("https://the-internet.herokuapp.com/tables")
        WebDriverWait(self.driver,15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"table#table1")))
    def extract_table_rows_xpath(self):
        selector="//table[@id='table1']//tr"
        start=time.perf_counter()
        rows=self.driver.find_elements(By.XPATH,selector)
        self.performance_data.append({"method":"XPath","selector":selector,"elements_found":len(rows),"time_taken_seconds":time.perf_counter()-start})
        return rows
    def parse_table_data(self,rows):
        headers=[]
        parsed=[]
        for index,row in enumerate(rows):
            th=row.find_elements(By.TAG_NAME,"th")
            if th:
                headers=[cell.text.strip() for cell in th]
                continue
            cells=row.find_elements(By.TAG_NAME,"td")
            if cells:
                parsed.append({"row_index":index,"cells":[cell.text.strip() for cell in cells]})
        return {"headers":headers,"rows":parsed,"metadata":{"total_data_rows":len(parsed),"source_url":self.driver.current_url,"extraction_timestamp_utc":datetime.now(timezone.utc).isoformat()}}
    def locate_buttons_by_class_name(self):
        found=[]
        seen=set()
        for name in ("button","btn","link-button"):
            for element in self.driver.find_elements(By.CLASS_NAME,name):
                if element.id not in seen:
                    found.append(element)
                    seen.add(element.id)
        self.performance_data.append({"method":"CLASS_NAME","selector":["button","btn","link-button"],"elements_found":len(found)})
        return found
    def locate_buttons_by_link_text(self):
        found=[]
        for phrase in ("Home","Back","Next","Table","Sort"):
            matches=self.driver.find_elements(By.LINK_TEXT,phrase)
            if not matches:
                matches=self.driver.find_elements(By.PARTIAL_LINK_TEXT,phrase)
            found.extend(matches)
        self.performance_data.append({"method":"LINK_TEXT","selector":["Home","Back","Next","Table","Sort"],"elements_found":len(found)})
        return found
    def compare_css_vs_xpath_performance(self,repetitions=7):
        scenarios=[
            {"name":"Table headers","css":"table#table1 th","xpath":"//table[@id='table1']//th"},
            {"name":"Table cells","css":"table#table1 td","xpath":"//table[@id='table1']//td"},
            {"name":"All links","css":"a","xpath":"//a"},
            {"name":"Second table row","css":"table#table1 tr:nth-child(2)","xpath":"//table[@id='table1']//tr[2]"}]
        output=[]
        for scenario in scenarios:
            measured={}
            for method,by,key in (("css",By.CSS_SELECTOR,"css"),("xpath",By.XPATH,"xpath")):
                times=[]
                count=0
                success=True
                error=None
                for _ in range(repetitions):
                    start=time.perf_counter()
                    try:
                        count=len(self.driver.find_elements(by,scenario[key]))
                    except Exception as exc:
                        success=False
                        error=str(exc)
                    times.append(time.perf_counter()-start)
                measured[method]={"selector":scenario[key],"median_seconds":statistics.median(times),"mean_seconds":statistics.mean(times),"success":success,"elements_found":count,"error":error}
            same=measured["css"]["success"] and measured["xpath"]["success"] and measured["css"]["elements_found"]==measured["xpath"]["elements_found"]
            faster="CSS" if measured["css"]["median_seconds"]<measured["xpath"]["median_seconds"] else "XPath"
            output.append({"scenario":scenario["name"],"css":measured["css"],"xpath":measured["xpath"],"counts_match":same,"faster_in_this_run":faster if same else "Not comparable","repetitions":repetitions})
        return output
    def run_lab(self):
        try:
            self.setup_driver()
            self.navigate_to_tables_page()
            table=self.parse_table_data(self.extract_table_rows_xpath())
            (BASE/"table_data.json").write_text(json.dumps(table,indent=2),encoding="utf-8")
            self.locate_buttons_by_class_name()
            self.locate_buttons_by_link_text()
            comparison=self.compare_css_vs_xpath_performance()
            (BASE/"performance_comparison.json").write_text(json.dumps(comparison,indent=2),encoding="utf-8")
            (BASE/"locator_methods.json").write_text(json.dumps(self.performance_data,indent=2),encoding="utf-8")
            log.info("Extracted %s table rows; Lab 8 completed",len(table["rows"]))
        except Exception:
            log.exception("Lab 8 failed")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                log.info("WebDriver closed")

if __name__=="__main__":
    WebElementLocator().run_lab()
