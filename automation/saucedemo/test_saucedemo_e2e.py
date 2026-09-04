from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup the driver
@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service = service)

    #Open the login page
    browser.get("https://www.saucedemo.com/")

    yield browser

    browser.quit()


def test_valid_login(driver):
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(
        EC.presence_of_element_located((By.ID,"user-name"))
    )
    username_field.send_keys("standard_user")
    password_field = wait.until(
        EC.presence_of_element_located((By.ID,"password"))
    )
    password_field.send_keys("secret_sauce")
    login_button = wait.until(
        EC.presence_of_element_located((By.ID,"login-button"))
    )
    login_button.click()
    current_url = driver.current_url
    assert current_url == "https://www.saucedemo.com/inventory.html" , f"Expected to land on inventory page instead of {current_url}"

def test_invalid_login(driver):
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(
        EC.presence_of_element_located((By.ID,"user-name"))
    )
    username_field.send_keys("wrong_user")
    password_field = wait.until(
        EC.presence_of_element_located((By.ID,"password"))
    )
    password_field.send_keys("wrong_pass")
    login_button = wait.until(
        EC.presence_of_element_located((By.ID,"login-button"))
    )
    login_button.click()
    error_message = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="error"]'))
    )
    assert "Username and password do not match any user in this service" in error_message.text, 'An error messages saying "Username and password do not match any user in this service" should have appeared'


@pytest.mark.parametrize("target_item_name",[
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket"
])
def test_add_to_cart_and_checkout(driver, target_item_name):
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(
        EC.presence_of_element_located((By.ID,"user-name"))
    )
    username_field.send_keys("standard_user")
    password_field = wait.until(
        EC.presence_of_element_located((By.ID,"password"))
    )
    password_field.send_keys("secret_sauce")
    login_button = wait.until(
        EC.presence_of_element_located((By.ID,"login-button"))
    )
    login_button.click()
    current_url = driver.current_url
    assert current_url == "https://www.saucedemo.com/inventory.html" , f"Expected to land on inventory page instead of {current_url}"

    items = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME,"inventory_item"))
    )

    target_item = None
    for item in items:
        item_name = item.find_element(By.CLASS_NAME, "inventory_item_name ")
        if item_name.text == target_item_name:
            target_item = item
            break
    add_to_cart_button = target_item.find_element(By.CSS_SELECTOR, '[data-test^="add-to-cart"]')
    add_to_cart_button.click()

    shopping_cart = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    shopping_cart.click()

    current_url = driver.current_url
    assert current_url == "https://www.saucedemo.com/cart.html" , f"Landed on {current_url}, although it was expected to land on https://www.saucedemo.com/cart.html"

    cart_item = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    )
    cart_item_name = cart_item.text
    assert cart_item_name == target_item_name , f"Expected to find {target_item_name} in the cart. Instead, foun {cart_item_name}"

    checkout_button = driver.find_element(By.ID, "checkout")
    checkout_button.click()

    current_url = driver.current_url
    assert current_url == "https://www.saucedemo.com/checkout-step-one.html" , f"Landed on {current_url}, although it was expected to land on https://www.saucedemo.com/checkout-step-one.html"

    first_name_field = wait.until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )
    first_name_field.send_keys("First")
    last_name_field = wait.until(
        EC.presence_of_element_located((By.ID, "last-name"))
    )
    last_name_field.send_keys("Last")
    zip_code_field = wait.until(
        EC.presence_of_element_located((By.ID, "postal-code"))
    )
    zip_code_field.send_keys("12345")

    continue_button = wait.until(
        EC.presence_of_element_located((By.ID, "continue"))
    )
    continue_button.click()

    current_url = driver.current_url
    assert current_url == "https://www.saucedemo.com/checkout-step-two.html" , f"Landed on {current_url}, although it was expected to land on https://www.saucedemo.com/checkout-step-two.html"

    finish_button = wait.until(
        EC.presence_of_element_located((By.ID,"finish"))
    )
    finish_button.click()

    confirmation_messgae = None
    confirmation_messgae = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME,"complete-header"))
    )

    confirmation_message_text = confirmation_messgae.text
    assert confirmation_message_text == "Thank you for your order!" , f"expected to find a message saying 'Thank you for your order!, but instead found {confirmation_message_text}"

