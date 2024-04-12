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
def get_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = file.readlines()
    return proxies

# Get proxies from file
proxies = get_proxies("proxies.txt")

# Function to check proxy availability
def check_proxy(proxy):
    try:
        response = requests.get(site, proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            return response
    except Exception as e:
        print(f"Error occurred while checking proxy: {e}")
    return None

# Loop to select a working proxy
proxy = None
for _ in range(len(proxies)):
    proxy = random.choice(proxies)
    response = check_proxy(proxy.strip())
    if response:
        print("Proxy is working. Headers:")
        print(response.headers)
        print("Response text:")
        print(response.text)
        break
    else:
        print(f"Proxy {proxy.strip()} is not responding. Trying another one.")

# Set up Chrome WebDriver with options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--lang=en-US")
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
chrome_options.add_argument("--referer=https://www.etsy.com/")
chrome_options.add_argument("--disable-javascript")

if proxy:
    chrome_options.add_argument(f"--proxy-server={proxy.strip()}")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the desired site
driver.get(site)

# Read cookies from file and add them to the WebDriver session
with open("etsy_cookies_login.json", "r") as file:
    cookies = json.load(file)

for cookie in cookies:
    driver.add_cookie(cookie)

# Sleep to ensure cookies are set before interacting with elements
time.sleep(30)

driver.find_element_by_xpath('//*[@id="gnav-header-inner"]/div[4]/nav/ul/li[1]/span/a/span/svg').click()

time.sleep(400)

# Quit the WebDriver session
driver.quit()