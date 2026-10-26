import pytest

from pages.login_page import LoginPage


class TestLogin:
    VALID_USERNAME = "tomsmith"
    VALID_PASSWORD = "SuperSecretPassword!"
    INVALID_USERNAME = "invaliduser"
    INVALID_PASSWORD = "wrongpassword"

    @pytest.mark.smoke
    def test_valid_login(self, driver):
        page = LoginPage(driver).open().login(self.VALID_USERNAME, self.VALID_PASSWORD)
        assert page.is_success(), "Valid credentials should open the secure area"
        assert "You logged into a secure area!" in page.get_success_message()

    @pytest.mark.smoke
    def test_invalid_login(self, driver):
        page = LoginPage(driver).open().login(self.INVALID_USERNAME, self.INVALID_PASSWORD)
        assert page.is_error(), "Invalid credentials should show an error"
        assert "Your username is invalid!" in page.get_error_message()

    @pytest.mark.regression
    def test_empty_credentials(self, driver):
        page = LoginPage(driver).open().login("", "")
        assert page.is_error(), "Empty credentials should be rejected"

    @pytest.mark.regression
    def test_invalid_username_valid_password(self, driver):
        page = LoginPage(driver).open().login(self.INVALID_USERNAME, self.VALID_PASSWORD)
        assert page.is_error()
        assert "Your username is invalid!" in page.get_error_message()

    @pytest.mark.regression
    def test_valid_username_invalid_password(self, driver):
        page = LoginPage(driver).open().login(self.VALID_USERNAME, self.INVALID_PASSWORD)
        assert page.is_error()
        assert "Your password is invalid!" in page.get_error_message()
