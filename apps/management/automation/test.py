import json
import asyncio
from playwright.async_api import async_playwright

async def load_cookies_from_file(file_path):
    with open(file_path, 'r') as file:
        cookies_data = json.load(file)

    cookies = cookies_data["cookies"]

    # Modify cookies to ensure sameSite is valid
    for cookie in cookies:
        if "sameSite" not in cookie:
            cookie["sameSite"] = "None"

    return cookies

async def automate_with_cookies_and_headers(url, cookies, headers):
    async with async_playwright() as p:
        browser = await p.chromium.launch()  # Launch browser without proxy
        context = await browser.new_context()  # Create a new browser context
        page = await context.new_page()  # Create a new page within the context

        # Set headers
        await page.set_extra_http_headers(headers)

        # Add cookies to the page
        await page.context.add_cookies(cookies)

        # Navigate to the URL
        await page.goto(url)

        # Do further automation here...

# Example usage
url = "https://www.etsy.com/"
cookie_file_path = "www.etsy.com_10-04-2024.json"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

async def main():
    cookies = await load_cookies_from_file(cookie_file_path)
    await automate_with_cookies_and_headers(url, cookies, headers)

asyncio.run(main())
