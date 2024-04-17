import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from apps.models import Product

def fill_product_fields(driver, product_data):
    element_listing_title_input = driver.find_element(By.XPATH, '//*[@id="listing-title-input"]')
    element_listing_title_input.send_keys(product_data['title'])

    element_listing_description_textarea = driver.find_element(By.XPATH, '//*[@id="listing-description-textarea"]')
    element_listing_description_textarea.send_keys(product_data['description'])

    element_listing_quantity_input = driver.find_element(By.XPATH, '//*[@id="listing-quantity-input"]')
    element_listing_quantity_input.send_keys(str(product_data['quantity']))

    element_listing_price_input = driver.find_element(By.XPATH, '//*[@id="listing-price-input"]')
    element_listing_price_input.send_keys(str(product_data['price']))


def add_product_to_etsy(product_data):
    driver = webdriver.Chrome()

    try:

        driver.get("https://www.etsy.com/add-listing")


        fill_product_fields(driver, product_data)

        element_save_button = driver.find_element(By.XPATH, '//*[@id="form-footer"]/div/div/button[2]')
        element_save_button.click()

        time.sleep(5)

    finally:
        # Закрытие WebDriver
        driver.quit()

def auto_fill_etsy_store():
    products = Product.objects.all()[:20]

    for product in products:
        product_data = {
            'title': product.title,
            'description': product.description,
            'quantity': product.quantity,
            'price': product.price,
        }

        add_product_to_etsy(product_data)

auto_fill_etsy_store()
