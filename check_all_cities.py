from bs4 import BeautifulSoup
import requests
import time
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

def main():
    # Uncomment this to get the availability only for these cities
    # cities = [
    #     "stockholm (sundbyberg)",
    #     "uppsala",
    # ]
    options = Options()
    options.add_argument("--headless") # Ensure GUI is off
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Set the location of the webdriver
    webdriver_path = '/usr/bin/chromedriver'
    # Create a driver object
    driver = Chrome(service=Service(webdriver_path), options=options)

    migration_agency_website = MigrationAgencyWebsite()
    migration_agency_website.get_cities_and_codes()
    for city in migration_agency_website.cities:
        # if city.name.lower() not in cities:
        #     continue
        print("Searching for slots in ", city.name)
        result = city.get_availability(migration_agency_website.booking_type_code, driver)
        if result:
            print(city.calendar, "\n")

class City:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.availability = False
        self.calendar = {}

    def get_availability(self, booking_type_code, driver):
        url = f"""https://www.migrationsverket.se/ansokanbokning/valjtyp?sprak=en&bokningstyp={booking_type_code}&enhet={self.code.upper()}&sokande=1"""
        driver.get(url)
        time.sleep(1)
        alert = None
        try:
            alert = driver.find_element(By.CSS_SELECTOR, '.feedbackPanel')
        except Exception as e:
            pass

        if alert:
            print("No available time slots. Message: " + alert.text, "\n")
            return self.availability

        html_calendar = driver.find_element(By.CLASS_NAME, "calendar")
        if html_calendar:
            print(f"Found some time slots in {self.name}.")

        soup = BeautifulSoup(driver.page_source, 'lxml')

        days = []
        for day in soup.find_all('th', class_='fc-day-header'):
            days.append(day['data-date'])

        calendar_container = soup.find('div', class_='fc-content-skeleton')
        table_body = calendar_container.find('tbody')
        columns = table_body.find_all('td')
        for i, column in enumerate(columns):
            rows = column.find_all('div', class_='fc-time')
            if rows:
                self.calendar[days[i-1]] = []
                for row in rows:
                    self.calendar[days[i-1]].append(row['data-full'])

        if self.calendar:
            self.availability = True
            return self.availability

        return self.availability


class MigrationAgencyWebsite:
    def __init__(self):
        self.booking_type_code = 2
        self.initial_url = 'https://www.migrationsverket.se/English/Contact-us/Book-change-or-cancel-appointments-for-visits.html'
        self.cities = []

    def get_cities_and_codes(self):
        response = requests.get(self.initial_url)
        html_content = response.text

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html_content, 'lxml') # or 'html.parser'

        # Find all script tags
        scripts = soup.find_all('script')
        booking_type_pattern = r'(?:[\n ]*"code":[ ]")([0-9]*)(?:",[\n ]*"text": "Have your fingerprints and photograph taken")'
        beginning_of_json_pattern = "Where do you want to make an appointment?"
        end_of_json_pattern = r'"Number of persons"'
        codes_and_cities_pattern = r'(?:"(?:code)":[ ]")([a-z0-9]*)(?:", "text": ")([A-Za-z ()]*)(?:[", a-z:[()]*)(?:bokningstyp:1)*(?:[", a-z:[]*)(?:bokningstyp:2)'
        match = None
        # Iterate over script tags and get the content or the src attribute
        for script in scripts:
            # If script tag contains inline JavaScript
            if not script.string:
                continue
            match = re.search(booking_type_pattern, script.string)
            if match:
                self.booking_type_code = match.group(1)
                script_piece = re.split(beginning_of_json_pattern, script.string)[-1]
                script_piece = re.split(end_of_json_pattern, script_piece)[0].lower()
                normalized_script = self.normalize_text(script_piece)
                codes_and_cities = re.findall(codes_and_cities_pattern, normalized_script)
                for code, city in codes_and_cities:
                    self.cities.append(City(name=city, code=code))

        # data_url = f"https://www.migrationsverket.se/ansokanbokning/wicket/page?1-2.IBehaviorListener.1-form-kalender-kalender&start={current_date}T10:35&end={end_date}T17:35&_=1713813583952"


    def normalize_text(self, text):
        replacements = {
            'ö': 'o',
            'å': 'a',
            'ä': 'a',
        }
        # Create a regular expression from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: replacements[mo.group()], text)


if __name__ == "__main__":
    main()
