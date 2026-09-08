from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from selenium.webdriver.chrome.options import Options
import os


# Set up the driver
@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    if os.environ.get("CI"):
        options.add_argument("--headless=new")
    browser = webdriver.Chrome(service=service, options=options)

    # Open the URL
    browser.get("https://the-internet.herokuapp.com/checkboxes")

    # Run the test functions
    yield browser

    # Quit the session after the tests run
    browser.quit()

# Define the parameters of tests 1 (Checking the checkboxes' default state)
@pytest.mark.parametrize("index, default_state",[
    (1, False),
    (2,True)
])

# Function to test default state of checkboxes
def test_default_checkbox_state(driver, index,default_state):
    checkbox = driver.find_element(By.XPATH, f'//*[@id="checkboxes"]/input[{index}]')
    assert checkbox.is_selected() == default_state, f"Test Case 1 has failed. Expected checkbox {index} to be {default_state}. Actual outcome for checlbox {index} was{checkbox}"

# Define the parameters of test 2 (Checking toggling the checkboxes)
@pytest.mark.parametrize("index",[
    1,
    2
])

# Function to test the toggle of the checkboxes
def test_checkbox_toggle(driver, index):
    checkbox = driver.find_element(By.XPATH, f'//*[@id="checkboxes"]/input[{index}]')
    state = "checked" if checkbox.is_selected() else "not checked"
    checkbox.click()
    new_state = "checked" if checkbox.is_selected() else "not checked"
    assert state != new_state, f"Test Case 2 has failed. After clicking checkbox {index}, it was {new_state}, although being {state} before getting clicked."
