import time
import json
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

site = "https://www.etsy.com/"
# email_address = "nikita.voloshyn.odessa@gmail.com"
# password = "Kartoshka?1"

# Function to get proxies from file
# def get_proxies(file_path):
#     with open(file_path, "r") as file:
#         proxies = file.readlines()
#     return proxies
#
# # Get proxies from file
# proxies = get_proxies("proxies.txt")
#
# # Function to check proxy availability
# def check_proxy(proxy):
#     try:
#         response = requests.get(site, proxies={"http": proxy, "https": proxy}, timeout=30)
#         if response.status_code == 200:
#             return response
#     except Exception as e:
#         print(f"Error occurred while checking proxy: {e}")
#     return None
#
# # Loop to select a working proxy
# proxy = None
# for _ in range(len(proxies)):
#     proxy = random.choice(proxies)
#     response = check_proxy(proxy.strip())
#     if response:
#         print("Proxy is working. Headers:")
#         print(response.headers)
#         print("Response text:")
#         print(response.text)
#         break
#     else:
#         print(f"Proxy {proxy.strip()} is not responding. Trying another one.")
proxy = "151.236.15.132:9800"
# Set up Chrome WebDriver with options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--lang=en-US")
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
chrome_options.add_argument("--referer=https://www.etsy.com/signin")
chrome_options.add_argument("--disable-javascript")

if proxy:
    chrome_options.add_argument(f"--proxy-server={proxy}")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the desired site
driver.get(site)

# Read cookies from file and add them to the WebDriver session
with open("www.etsy.com_15-04-2024.json", "r") as file:
    cookies = json.load(file)

for cookie in cookies:
    driver.add_cookie(cookie)

time.sleep(30)

driver.refresh()

time.sleep(5)

element_shop_manager = driver.find_element(By.XPATH, '//*[@id="gnav-header-inner"]/div[4]/nav/ul/li[3]/span/a/span[1]')
element_shop_manager.click()

time.sleep(5)

element_listings = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[1]/div[2]/ul/li[3]/a')
element_listings.click()

time.sleep(5)

element_add_listing = driver.find_element(By.XPATH, '//*[@id="page-region"]/div/div/div[1]/header/div[1]/div/div[3]/div/div/a')
element_add_listing.click()

time.sleep(5)

element_1 = driver.find_element(By.XPATH, '//*[@id="core-details-overlay"]/div/fieldset/div[2]/fieldset/div[1]/label')
element_1.click()

time.sleep(5)

element_2 = driver.find_element(By.XPATH, '//*[@id="core-details-overlay"]/div/fieldset/div[3]/fieldset/div[1]/label')
element_2.click()

time.sleep(5)

element_3 = driver.find_element(By.XPATH, '//*[@id="when-made-select"]/optgroup[2]/option[1]')
element_3.click()

time.sleep(5)

element_4 = driver.find_element(By.XPATH, '//*[@id="core-details-overlay"]/div/div[2]/div/div[2]/button')
element_4.click()

time.sleep(5)



element_listing_title_input = driver.find_element(By.XPATH, '//*[@id="listing-title-input"]')
element_listing_title_input.send_keys("This is a title")

time.sleep(5)

element_listing_description_textarea = driver.find_element(By.XPATH, '//*[@id="listing-description-textarea"]')
element_listing_description_textarea.send_keys("This is a description")

time.sleep(5)

element_listing_quantity_input = driver.find_element(By.XPATH, '//*[@id="listing-quantity-input"]')
element_listing_quantity_input.send_keys("5")

time.sleep(5)

element_listing_price_input = driver.find_element(By.XPATH, '//*[@id="listing-price-input"]')
element_listing_price_input.send_keys("100")

time.sleep(5)

element_shoping_profile = driver.find_element(By.XPATH, '//*[@id="field-sourceShippingProfileId"]/button')
element_shoping_profile.click()
time.sleep(10)
element_shoping_profile_2 = driver.find_element(By.XPATH, '//*[@id="shipping-profile-overlay"]/div/div[2]/ul/li/div/div/div/div[2]/div[1]/button')
element_shoping_profile_2.click()
time.sleep(5)

element_category_input = driver.find_element(By.XPATH, '//*[@id="category-field-search"]')
element_category_input.send_keys("Tabel")
time.sleep(2)
element_category_2 = driver.find_element(By.XPATH, '//*[@id="category-search-option-993"]/div/p[1]')
element_category_2.click()

time.sleep(5)

element_save_button = driver.find_element(By.XPATH, '//*[@id="form-footer"]/div/div/button[2]')
element_save_button.click()


time.sleep(600)

# Quit the WebDriver session
driver.quit()
