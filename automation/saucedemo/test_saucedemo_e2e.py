from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os


# --- Setup the driver ---
@pytest.fixture
def driver(request):
    service = Service(ChromeDriverManager().install())
    options = Options()
    if os.environ.get("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(service=service, options=options)
    browser.get("https://www.saucedemo.com/")

    yield browser

    # If the test failed, save a screenshot before quitting
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        name = request.node.name.replace("[", "_").replace("]", "").replace(" ", "_")
        browser.save_screenshot(f"failure_{name}.png")

    browser.quit()


# --- Helper: click an element via JavaScript (reliable in headless CI) ---
def js_click(driver, wait, locator):
    element = wait.until(EC.presence_of_element_located(locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)


def test_valid_login(driver):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
    js_click(driver, wait, (By.ID, "login-button"))

    wait.until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", \
        f"Expected to land on inventory page instead of {driver.current_url}"


def test_invalid_login(driver):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("wrong_user")
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("wrong_pass")
    js_click(driver, wait, (By.ID, "login-button"))

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
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
    js_click(driver, wait, (By.ID, "login-button"))

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

    add_to_cart_button = target_item.find_element(By.CSS_SELECTOR, '[data-test^="add-to-cart"]')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
    driver.execute_script("arguments[0].click();", add_to_cart_button)

    js_click(driver, wait, (By.CLASS_NAME, "shopping_cart_link"))
    wait.until(EC.url_to_be("https://www.saucedemo.com/cart.html"))
    assert driver.current_url == "https://www.saucedemo.com/cart.html", \
        f"Landed on {driver.current_url}, although it was expected to land on cart.html"

    cart_item = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name")))
    assert cart_item.text == target_item_name, \
        f"Expected to find {target_item_name} in the cart. Instead, found {cart_item.text}"

    js_click(driver, wait, (By.ID, "checkout"))
    wait.until(EC.url_to_be("https://www.saucedemo.com/checkout-step-one.html"))
    assert driver.current_url == "https://www.saucedemo.com/checkout-step-one.html", \
        f"Landed on {driver.current_url}, although it was expected to land on checkout-step-one.html"

    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("First")
    wait.until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys("Last")
    wait.until(EC.presence_of_element_located((By.ID, "postal-code"))).send_keys("12345")
    js_click(driver, wait, (By.ID, "continue"))

    wait.until(EC.url_to_be("https://www.saucedemo.com/checkout-step-two.html"))
    assert driver.current_url == "https://www.saucedemo.com/checkout-step-two.html", \
        f"Landed on {driver.current_url}, although it was expected to land on checkout-step-two.html"

    js_click(driver, wait, (By.ID, "finish"))

    confirmation_message = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert confirmation_message.text == "Thank you for your order!", \
        f"Expected 'Thank you for your order!', but instead found {confirmation_message.text}"