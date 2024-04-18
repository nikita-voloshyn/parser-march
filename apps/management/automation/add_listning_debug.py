import os
import django
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Set up logging for requests
requests_logger = logging.getLogger('requests')
requests_logger.setLevel(logging.INFO)
requests_handler = logging.FileHandler('requests.log')
requests_formatter = logging.Formatter('%(asctime)s - %(message)s')
requests_handler.setFormatter(requests_formatter)
requests_logger.addHandler(requests_handler)

# Set up logging for errors
errors_logger = logging.getLogger('errors')
errors_logger.setLevel(logging.ERROR)
errors_handler = logging.FileHandler('errors.log')
errors_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
errors_handler.setFormatter(errors_formatter)
errors_logger.addHandler(errors_handler)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Initialize Django
django.setup()

from apps.models import Product, Variant

def wait_and_click(driver, locator, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
    except TimeoutException:
        errors_logger.error("Timed out waiting for element to be clickable")
    except NoSuchElementException:
        errors_logger.error("Element not found")

def fill_pre_form_details(driver):
    # Pre-form details
    wait_and_click(driver, (By.XPATH, '//*[@id="core-details-overlay"]/div/fieldset/div[2]/fieldset/div[1]/label'))
    wait_and_click(driver, (By.XPATH, '//*[@id="core-details-overlay"]/div/fieldset/div[3]/fieldset/div[1]/label'))
    wait_and_click(driver, (By.XPATH, '//*[@id="when-made-select"]/optgroup[2]/option[1]'))
    wait_and_click(driver, (By.XPATH, '//*[@id="core-details-overlay"]/div/div[2]/div/div[2]/button'))

def fill_other_details(driver):
    try:
        element_category_input = driver.find_element(By.XPATH, '//*[@id="category-field-search"]')
        element_category_input.send_keys("Boot")
        time.sleep(2)
        element_category_2 = driver.find_element(By.XPATH, '//*[@id="category-search-option-1513"]/div/p[1]')
        element_category_2.click()

        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 4000);")
        time.sleep(5)
        element_shipping_profile = driver.find_element(By.XPATH, '//*[@id="field-sourceShippingProfileId"]/button')
        element_shipping_profile.click()
        time.sleep(10)
        element_shipping_profile_2 = driver.find_element(By.XPATH, '//*[@id="shipping-profile-overlay"]/div/div[2]/ul/li/div/div/div/div[2]/div[1]/button')
        element_shipping_profile_2.click()
    except NoSuchElementException:
        errors_logger.error("Element not found")

def save_listing(driver):
    wait_and_click(driver, (By.XPATH, '//*[@id="form-footer"]/div/div/button[2]'))

def fill_product_fields(driver, product_data):
    fill_pre_form_details(driver)

    # Fill in the actual form fields
    try:
        element_listing_title_input = driver.find_element(By.XPATH, '//*[@id="listing-title-input"]')
        element_listing_title_input.send_keys(product_data['title'])

        element_listing_description_textarea = driver.find_element(By.XPATH, '//*[@id="listing-description-textarea"]')
        element_listing_description_textarea.send_keys(product_data['description'])

        element_listing_quantity_input = driver.find_element(By.XPATH, '//*[@id="listing-quantity-input"]')
        element_listing_quantity_input.send_keys(str(product_data['quantity']))

        element_listing_price_input = driver.find_element(By.XPATH, '//*[@id="listing-price-input"]')
        element_listing_price_input.send_keys(str(product_data['price']))
    except NoSuchElementException:
        errors_logger.error("Element not found")

def next_listing(driver):
    wait_and_click(driver, (By.XPATH, '//*[@id="page-region"]/div/div/div[1]/header/div[1]/div/div[3]/div/div/a'))

def load_items(driver, num_items, delay):
    for variant in Variant.objects.all()[:num_items]:
        product_data = {
            'title': variant.name,  # Assuming url as title for now
            'description': variant.item_detail,  # Provide description if available
            'quantity': 1,  # Provide quantity if available
            'price': variant.price,  # Provide price if available
        }
        try:
            fill_product_fields(driver, product_data)
            requests_logger.info("fill_product_fields done")
            fill_other_details(driver)
            requests_logger.info("fill_other_details done")
            save_listing(driver)
            requests_logger.info("save_listing done")
            next_listing(driver)
        except Exception as e:
            errors_logger.error(f"An error occurred: {e}")
        time.sleep(delay)

site = "https://www.etsy.com/"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--lang=en-US")
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
chrome_options.add_argument("--referer=https://www.etsy.com/signin")
# chrome_options.add_argument("--disable-javascript") # Commented out to enable JavaScript
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get(site)

with open("www.etsy.com_15-04-2024.json", "r") as file:
    cookies = json.load(file)

for cookie in cookies:
    driver.add_cookie(cookie)

time.sleep(10)
driver.refresh()
time.sleep(5)

try:
    element_shop_manager = driver.find_element(By.XPATH, '//*[@id="gnav-header-inner"]/div[4]/nav/ul/li[3]/span/a/span[1]')
    element_shop_manager.click()
    time.sleep(5)

    element_listings = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[1]/div[2]/ul/li[3]/a')
    element_listings.click()
    time.sleep(5)

    element_add_listing = driver.find_element(By.XPATH, '//*[@id="page-region"]/div/div/div[1]/header/div[1]/div/div[3]/div/div/a')
    element_add_listing.click()
    time.sleep(5)

    load_items(driver, num_items=20, delay=5)  # Example: Load 20 items with a delay of 5 seconds

    requests_logger.info("All done")
except Exception as e:
    errors_logger.error(f"An error occurred: {e}")
finally:
    driver.quit()
