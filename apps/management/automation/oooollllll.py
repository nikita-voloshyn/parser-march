import time
import json
from selenium import webdriver

site = "https://www.etsy.com/"

# Set up Chrome WebDriver with options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--lang=en-US")
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
chrome_options.add_argument("--referer=https://www.etsy.com/signin")
chrome_options.add_argument("--disable-javascript")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the desired site
driver.get(site)

# Read cookies from file and add them to the WebDriver session
with open("www.etsy.com_15-04-2024.json", "r") as file:
    cookies = json.load(file)

for cookie in cookies:
    driver.add_cookie(cookie)

time.sleep(60)

driver.refresh()

time.sleep(60)

# Quit the WebDriver session
driver.quit()
