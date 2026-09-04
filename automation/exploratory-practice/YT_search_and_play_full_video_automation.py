from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Setup ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# --- Navigate and search ---
driver.get("https://www.youtube.com")

time.sleep(3)

search_bar = driver.find_element(
    By.XPATH,
    "//*[@class='ytSearchboxComponentInput yt-searchbox-input title' and @name='search_query']"
)
search_bar.send_keys("How to use Selenium")

time.sleep(3)

search_button = driver.find_element(By.CLASS_NAME, "ytSearchboxComponentSearchButton")
search_button.click()

print("Search results URL:", driver.current_url)

# --- Define the waiting time ---
wait = WebDriverWait(driver, 10)

# --- Click the first video result ---
first_result = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "yt-lockup-view-model a.ytLockupMetadataViewModelTitle"))
)
first_result.click()

print("Video URL:", driver.current_url)

# --- Wait for any ad to finish ---
def ad_has_ended(driver):
    ad_elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Sponsored']")
    return len(ad_elements) == 0

ad_wait = WebDriverWait(driver, 60)    # I can improve it further by clicking the skip button instead of waiting for 60s
ad_wait.until(ad_has_ended)
print("No ad detected (either it finished, or there was none).")

# --- Wait for the real video duration to be available ---
def player_duration_ready(driver):
    try:
        duration = driver.execute_script(
            "return document.getElementById('movie_player').getDuration()"
        )
        if duration and duration > 0:
            return duration
    except Exception:
        pass
    return False

duration_wait = WebDriverWait(driver, 10)
duration = duration_wait.until(player_duration_ready)
print("Total video seconds:", duration)

# --- Wait for the video to finish playing, then close ---
time.sleep(duration + 3)

driver.quit()