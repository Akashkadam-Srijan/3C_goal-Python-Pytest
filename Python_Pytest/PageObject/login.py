from selenium.webdriver.common.by import By

from Python_Pytest.PageObject.shop import ShopPage
from Python_Pytest.utils.browserUtils import BrowserUtils


class LoginPage(BrowserUtils):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver= driver
        self.username = (By.ID, "username")
        self.password = (By.ID, "password")
        self.submit = (By.ID, "signInBtn")


    def login(self,username,password):
        self.driver.find_element(*self.username).send_keys(username)
        self.driver.find_element(*self.password ).send_keys(password)
        self.driver.find_element(*self.submit).click()

        shop_page = ShopPage(self.driver)
        return shop_page