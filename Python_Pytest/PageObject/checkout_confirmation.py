from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from Python_Pytest.utils.browserUtils import BrowserUtils


class CheckoutConfirmation:

    def __init__(self,driver):
        self.driver =  driver
        self.utils = BrowserUtils(driver)
        self.checkout_button = (By.XPATH, "//button[@class = 'btn btn-success']")
        self.enter_address = (By.XPATH, "//input[@id='country']")
        self.select_address = (By.XPATH, "//a[text()='India']")
        self.checkbox = (By.CSS_SELECTOR, "div[class='checkbox checkbox-primary']")
        self.click_submit_button = (By.CSS_SELECTOR, "input[class*='success btn-lg']")
        self.check_success_msg = (By.CSS_SELECTOR, "div[class*='alert-success']")


    def checkout(self):
        # Click on Checkout for confirm order
        confirm_checkout = self.driver.find_element(*self.checkout_button)
        print("Background-color", confirm_checkout.value_of_css_property("background-color"))
        print("Color", confirm_checkout.value_of_css_property("color"))
        print("Font-size", confirm_checkout.value_of_css_property("font-size"))
        print("Font-size", confirm_checkout.value_of_css_property("font-weight"))
        if confirm_checkout.is_displayed():
            confirm_checkout.click()


    def enter_delivery_address(self,country):
        #  Select delivery location
        self.driver.find_element(*self.enter_address).send_keys(country)
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.presence_of_element_located(self.select_address))
        self.driver.find_element(*self.select_address).click()

        #  Click on Purchase
        self.driver.find_element(*self.checkbox).click()
        submit_Button = self.driver.find_element(*self.click_submit_button)
        # print("Background-color", submit_Button.value_of_css_property("background-color"))
        # print("Color", submit_Button.value_of_css_property("color"))
        # print("Font-size", submit_Button.value_of_css_property("font-size"))
        # print("Font-size", submit_Button.value_of_css_property("font-weight"))
        self.utils.print_css_properties(submit_Button)
        print("**********", submit_Button.text)
        assert submit_Button.is_displayed()
        if submit_Button.is_displayed():
            submit_Button.click()

    def validate_order(self):
        # Verify success MSG
        success_msg = self.driver.find_element(*self.check_success_msg).text
        print(success_msg)
        assert "Success! Thank you!" in success_msg
