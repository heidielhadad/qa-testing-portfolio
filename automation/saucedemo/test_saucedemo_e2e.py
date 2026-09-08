from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os


# Setup the driver
@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    if os.environ.get("CI"):
        options.add_argument("--headless=new")
    browser = webdriver.Chrome(service=service, options=options)
    browser.get("https://www.saucedemo.com/")
    yield browser
    browser.quit()


def test_valid_login(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
    wait.until(EC.presence_of_element_located((By.ID, "login-button"))).click()

    wait.until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", \
        f"Expected to land on inventory page instead of {driver.current_url}"


def test_invalid_login(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("wrong_user")
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("wrong_pass")
    wait.until(EC.presence_of_element_located((By.ID, "login-button"))).click()

    error_message = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="error"]'))
    )
    assert "Username and password do not match any user in this service" in error_message.text, \
        'An error message saying "Username and password do not match any user in this service" should have appeared'


@pytest.mark.parametrize("target_item_name", [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket"
])
def test_add_to_cart_and_checkout(driver, target_item_name):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
    wait.until(EC.presence_of_element_located((By.ID, "login-button"))).click()

    wait.until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", \
        f"Expected to land on inventory page instead of {driver.current_url}"

    items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))

    target_item = None
    for item in items:
        item_name = item.find_element(By.CLASS_NAME, "inventory_item_name")
        if item_name.text == target_item_name:
            target_item = item
            break

    target_item.find_element(By.CSS_SELECTOR, '[data-test^="add-to-cart"]').click()

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    wait.until(EC.url_to_be("https://www.saucedemo.com/cart.html"))
    assert driver.current_url == "https://www.saucedemo.com/cart.html", \
        f"Landed on {driver.current_url}, although it was expected to land on cart.html"

    cart_item = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name")))
    assert cart_item.text == target_item_name, \
        f"Expected to find {target_item_name} in the cart. Instead, found {cart_item.text}"

    driver.find_element(By.ID, "checkout").click()
    wait.until(EC.url_to_be("https://www.saucedemo.com/checkout-step-one.html"))
    assert driver.current_url == "https://www.saucedemo.com/checkout-step-one.html", \
        f"Landed on {driver.current_url}, although it was expected to land on checkout-step-one.html"

    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("First")
    wait.until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys("Last")
    wait.until(EC.presence_of_element_located((By.ID, "postal-code"))).send_keys("12345")
    wait.until(EC.presence_of_element_located((By.ID, "continue"))).click()

    wait.until(EC.url_to_be("https://www.saucedemo.com/checkout-step-two.html"))
    assert driver.current_url == "https://www.saucedemo.com/checkout-step-two.html", \
        f"Landed on {driver.current_url}, although it was expected to land on checkout-step-two.html"

    wait.until(EC.presence_of_element_located((By.ID, "finish"))).click()

    confirmation_message = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert confirmation_message.text == "Thank you for your order!", \
        f"Expected 'Thank you for your order!', but instead found {confirmation_message.text}"