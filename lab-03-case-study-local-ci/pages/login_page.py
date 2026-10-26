from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages import BasePage


class LoginPage(BasePage):
    LOGIN_URL = "https://the-internet.herokuapp.com/login"
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#flash.success, .flash.success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "#flash.error, .flash.error")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a[href='/logout']")

    def open(self):
        self.driver.get(self.LOGIN_URL)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        return self

    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        return self

    def is_success(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            self.wait.until(EC.visibility_of_element_located(self.LOGOUT_BUTTON))
            return True
        except Exception:
            return False

    def is_error(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return True
        except Exception:
            return False

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
