import json
import pytest
from Python_Pytest.PageObject.login import LoginPage

test_data_path = 'Python_Pytest/data/test_e2eTestFramework.json'

with open(test_data_path) as f:
    test_data = json.load(f)
    test_list = test_data["data"]

@pytest.mark.parametrize("test_item_list",test_list)
def test_e2e_testing(browserInstance,test_item_list):

    driver = browserInstance

    login_page = LoginPage(driver)
    print("Login Page Title : ",login_page.getPageTitle())

    shop_page = login_page.login(test_item_list["username"],test_item_list["password"])
    shop_page.add_product_to_cart(test_item_list["productName"])

    checkout_confirmation = shop_page.goToCart()
    checkout_confirmation.checkout()
    checkout_confirmation.enter_delivery_address("Ind")
    checkout_confirmation.validate_order()


