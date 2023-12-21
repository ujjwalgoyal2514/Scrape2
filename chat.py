import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


    # @staticmethod
def init_driver(browser_name: str):
    def set_properties(browser_option):
        ua = UserAgent().random
        browser_option.add_argument('--headless')
        browser_option.add_argument('--disable-extensions')
        browser_option.add_argument('--incognito')
        browser_option.add_argument('--disable-gpu')
        browser_option.add_argument('--log-level=3')
        browser_option.add_argument(f'user-agent={ua}')
        browser_option.add_argument('--disable-notifications')
        browser_option.add_argument('--disable-popup-blocking')
        return browser_option

    try:
            browser_name = browser_name.strip().lower()

            if browser_name == 'chrome':
                browser_option = ChromeOptions()
                set_properties(browser_option)
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=browser_option)
            elif browser_name == "firefox":
                browser_option = FirefoxOptions()
                set_properties(browser_option)
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=browser_option)
            else:
                raise ValueError("Browser not supported")
            return driver
    except Exception as ex:
            print(ex)
            return None
def scrape_twitter_profile(username):
    driver = init_driver('chrome')  # You can change 'chrome' to 'firefox' if needed

    if not driver:
        return "Failed to initialize web driver."

    try:
        # Load Twitter profile
        driver.get(f'https://twitter.com/{username}')
        time.sleep(5)  # Allow time for the page to load

        # Extract profile details using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Finding relevant elements
        bio = soup.find('div', {'data-testid': 'UserDescription'})
        following_count = soup.find( 'div', {'class':'css-175oi2r r-1mf7evn'})
        location = soup.find('div', {'data-testid': 'UserProfileHeader_Items'})  # Adjust this according to the actual page structure
        div_element = soup.find('div', {'a': 'UserDescription'})
        if div_element:
            a_element = div_element.find('a')
            span_elements = div_element.find_all('span')
            if a_element and span_elements:
                # Access the desired information
                # For example:
                a_text = a_element.get_text().strip()
                span_texts = [span.get_text().strip() for span in span_elements]
                span_class = span_elements[0].get('class')  # Assuming you want the class of the first span
                print(f"Text from 'a': {a_text}")
                print(f"Texts from 'span': {span_texts}")
                print(f"Class of the first 'span': {span_class}")



        followers_count_span = soup.find('span', class_='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3')  # Replace 'your-span-class' with the actual class name
        followers_count_text = followers_count_span.get_text().strip() if followers_count_span else ''

        # Extract text from elements
        bio_text = bio.get_text().strip() if bio else ''
        following_count_text = following_count.find('span').get_text().strip() if following_count else ''
        location_text = location.get_text().strip() if location else ''
        # followers_count_text = followers_count.find('span').get_text().strip() if followers_count else ''


        # Close the WebDriver
        driver.quit()

        # Return data
        return {
            'Username': username,
            'Bio': bio_text,
            'Following Count': following_count_text,
            'Followers Count': followers_count_text,
            'Location':location_text,
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        driver.quit()
        return None

# Example usage
username_to_scrape = 'whatsapp'
profile_data = scrape_twitter_profile(username_to_scrape)

if profile_data:
    # Create DataFrame
    df = pd.DataFrame([profile_data])

    # Save to CSV
    df.to_csv('twitter_profiles.csv', index=False)
