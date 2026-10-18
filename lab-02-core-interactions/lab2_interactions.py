from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    return driver


def test_login_form(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    )
    assert "You logged into a secure area!" in message.text
    print("Login form test passed.")
    driver.find_element(By.CSS_SELECTOR, "a[href='/logout']").click()


def test_dropdown_select(driver):
    driver.get("https://the-internet.herokuapp.com/dropdown")
    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    dropdown.select_by_visible_text("Option 1")
    assert dropdown.first_selected_option.text == "Option 1"
    dropdown.select_by_value("2")
    assert dropdown.first_selected_option.text == "Option 2"
    print("Dropdown test passed.")


def test_checkbox_toggle(driver):
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    assert len(checkboxes) == 2
    for checkbox in checkboxes:
        checkbox.click()
    assert all(box.is_selected() for box in checkboxes)
    print("Checkbox test passed.")


def test_javascript_alerts(driver):
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    driver.find_element(By.CSS_SELECTOR, "button[onclick='jsAlert()']").click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "I am a JS Alert"
    alert.accept()
    assert "You successfully clicked an alert" in driver.find_element(By.ID, "result").text

    driver.find_element(By.CSS_SELECTOR, "button[onclick='jsConfirm()']").click()
    confirm = WebDriverWait(driver, 5).until(EC.alert_is_present())
    confirm.dismiss()
    assert "You clicked: Cancel" in driver.find_element(By.ID, "result").text
    print("JavaScript alert tests passed.")


def test_dynamic_element_wait(driver):
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    driver.find_element(By.CSS_SELECTOR, "div#start button").click()
    message = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div#finish h4"))
    )
    assert message.text == "Hello World!"
    print("Dynamic loading test passed.")


def main():
    driver = create_driver()
    try:
        test_login_form(driver)
        test_dropdown_select(driver)
        test_checkbox_toggle(driver)
        test_javascript_alerts(driver)
        test_dynamic_element_wait(driver)
        driver.get("https://the-internet.herokuapp.com/")
        output = Path("lab2_result.png")
        driver.save_screenshot(str(output))
        print(f"Screenshot saved: {output.resolve()}")
        print("All Lab 2 checks passed.")
    except TimeoutException as exc:
        print(f"A page element did not become ready in time: {exc}")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
