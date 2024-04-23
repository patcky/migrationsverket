# Import selenium webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from PIL import Image

def main():
    # Change this list to get the availability for other cities
    cities = (
        "stockholm",
        "uppsala",
    )

    for city_name in cities:
        print("City: ", city_name)
        if check_migration_agency_website(city_name):
            print(f"There are available time slots in {city_name}")


def check_migration_agency_website(city_name):
    """
    Check if there are available time slots for appointments on the migration agency website.

    Args:
        city_name (str): The name of the city.
        city_xpath (str): The XPath of the city option element.

    Returns:
        bool: True if there are available time slots, False otherwise.
    """
    short_sleep = 0.5

    # Set up Chrome options
    options = Options()
    options.add_argument("--headless") # Ensure GUI is off
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set the location of the webdriver
    webdriver_path = '/usr/bin/chromedriver'
    # Create a driver object
    driver = Chrome(service=Service(webdriver_path), options=options)
    wait = WebDriverWait(driver, 10)

    # Go to the page
    driver.get("https://www.migrationsverket.se/English/Contact-us/Book-change-or-cancel-appointments-for-visits.html")

    # click the cookie banner first
    cookie_banner = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/form')
    cookie_banner.click()
    time.sleep(short_sleep)

    # Find the element for the radio button and click it
    radio_button = wait.until(EC.element_to_be_clickable((By.ID, "fingeravtryck_foto")))
    driver.execute_script("arguments[0].click();", radio_button)
    time.sleep(short_sleep)

    # Find the element for the location select and click it
    location_select = driver.find_element(By.ID,"enhet")
    location_select.click()

    # Find the option for the city
    city_option = None

    options = Select(location_select).options

    # Find the option that matches the city
    for option in options:
        if city_name in option.text.lower():
            city_option = option
            break

    print("Searching for slots in ", city_option.text.strip())
    city_option.click()
    time.sleep(short_sleep)

    # Find the element for the number of persons select and click it
    persons_select = driver.find_element(By.ID,"sokande")
    persons_select.click()

    # Find the option for 1 and click it
    actions = ActionChains(driver)
    actions.send_keys(keys.DOWN).perform()
    actions.send_keys(keys.ENTER).perform()

    # Find the element for the checkbox and click it
    checkbox = driver.find_element(By.XPATH,'//*[@id="godkannId1"]')
    driver.execute_script("arguments[0].click();", checkbox)

    # Find the element for the submit button and click it
    submit_button = driver.find_element(By.ID, "bokaSubmit")
    submit_button.click()

    # Wait for the page to load
    wait.until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(short_sleep)

    # Check if the specified text is present
    try:
        alert = driver.find_element(By.CSS_SELECTOR, '.feedbackPanel')
        print("No available time slots. Message: " + alert.text)
        return False
    except Exception as e:
        #logging.error(e)
        print("No alert found. Checking if there are available time slots.")

    calendar = driver.find_element(By.CLASS_NAME, "calendar")
    if calendar:
        print(f"It seems that there are available time slots in {city_name}. Please check the page manually.")
        file_path = f'{city_name}-timeslots.png'
        # take screenshot of the page
        calendar.screenshot(file_path)
        screenshot = Image.open(file_path)
        screenshot.show()
        return True

if __name__ == "__main__":
    main()
