from selenium.webdriver.common.by import By

from Python_Pytest.PageObject.checkout_confirmation import CheckoutConfirmation


class ShopPage:

    def __init__(self,driver):
        self.driver = driver
        self.shop_button = (By.LINK_TEXT, "Shop")
        self.select_product = (By.XPATH, "//div[@class='card h-100']")
        self.check_out_Button = (By.CSS_SELECTOR, "a[class*='btn-primary']")


    def add_product_to_cart(self,product_name):
        # 1. Check shop button is clickable
        self.driver.find_element(*self.shop_button).click()

        # 2. Select product from list
        mobile_product = self.driver.find_elements(*self.select_product)
        for mobile in mobile_product:
            mobile_name = mobile.find_element(By.XPATH, "div/h4/a").text
            print(f"Mobile Names:{mobile_name}")
            if mobile_name == product_name:
                mobile.find_element(By.XPATH, "div/button").click()

    def goToCart(self):
        # 3. Click on Checkout button
        checkout_button = self.driver.find_element(*self.check_out_Button)
        print("Background-color", checkout_button.value_of_css_property("background-color"))
        print("Color", checkout_button.value_of_css_property("color"))
        print("Font-size", checkout_button.value_of_css_property("font-size"))
        print(checkout_button.text)
        assert checkout_button.is_displayed()
        if checkout_button.is_displayed():
            checkout_button.click()

        checkout_confirmation = CheckoutConfirmation(self.driver)
        return checkout_confirmation

