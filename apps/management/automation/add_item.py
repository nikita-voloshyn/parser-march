import requests
import json

session = requests.Session()

# URL сервера, куда отправляем запрос
url = 'https://www.etsy.com/your/shops/Theclothesofthewest/tools/listings/create'

# Данные для отправки
data = {
    "listing_id": 1695622222,
    "shop_id": 51167133,
    "user_id": 912355539,
    "section_id": None,
    "title": "thhhhh",
    "description": "",
    "quantity": 1,
    "state": 3,
    "url": "https://www.etsy.com/listing/1695622222/thhhhh",
    "non_taxable": False,
    "featured_rank": -1,
    "is_available": False,
    "create_date": 1712384081,
    "update_date": 1712384081,
    "shop_subdomain_listing_url": "https://theclothesofthewest.etsy.com/listing/1695622222",
    "price": "100.00",
    "price_int": 10000,
    "currency_code": "USD",
    "currency_symbol": "$",
    "is_featured": False,
    "is_retail": True,
    "is_pattern": False,
    "is_reserved": False,
    "is_reserved_listing": False,
    "is_private": False,
    "is_frozen": False,
    "is_fixed_cost": True,
    "taxonomy_id": 977,
    "suggested_taxonomy_id": None,
    "full_path_taxonomy_ids": [
        891,
        967,
        973,
        977
    ],
    "full_path_taxonomy_names": [
        "Home & Living",
        "Furniture",
        "Dining Room Furniture",
        "Kitchen & Dining Tables"
    ],
    "is_mapped_ott_node": None,
    "is_taxonomy_suggestion": None,
    "is_empty_taxonomy_suggestion": None,
    "mapped_attributes": None,
    "unmapped_taxonomy_path_names": None,
    "unmapped_taxonomy_id": None,
    "subscription_discount_amount": None,
    "subscription_max_duration": None,
    "activation_cost": {
        "amount": 20,
        "divisor": 100,
        "currency_code": "USD",
        "currency_formatted_short": "USD 0.20",
        "currency_formatted_long": "USD 0.20 USD",
        "currency_formatted_raw": "0.20"
    },
    "has_ip_infringement_flag": False,
    "ip_owner_name": None,
    "legacy_state": "draft",
    "category_id": None,
    "category_name": None,
    "category_tags": [],
    "category_ids": [],
    "section_name": None,
    "type": "physical",
    "has_variation_pricing": False,
    "has_variation_quantity": False,
    "has_variation_sku": False,
    "has_variations": False,
    "is_supply": False,
    "is_vintage": False,
    "is_handmade": True,
    "is_digital": False,
    "in_person_eligible": False,
    "is_customizable": False,
    "is_personalizable": False,
    "personalization_instructions": None,
    "personalization_char_count_max": 256,
    "personalization_is_required": True,
    "personalization_price_diff": None,
    "who_made": "i_did",
    "when_made": "made_to_order",
    "compliance_summary": "",
    "show_truncated_compliance_summary_alert": False,
    "tags": [],
    "materials": [
        "wood"
    ],
    "styles": [
        ""
    ],
    "images": [
        "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_fullxfull.5947163617_98eq.jpg"
    ],
    "image_url_fullxfull": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_fullxfull.5947163617_98eq.jpg",
    "listing_images": [
        {
            "image_id": 5947163617,
            "owner_id": 51167133,
            "url": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_fullxfull.5947163617_98eq.jpg",
            "url_75x75": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_75x75.5947163617_98eq.jpg",
            "url_170x135": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_170x135.5947163617_98eq.jpg",
            "url_224xN": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_224xN.5947163617_98eq.jpg",
            "url_300x300": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_300x300.5947163617_98eq.jpg",
            "url_340x270": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_340x270.5947163617_98eq.jpg",
            "url_680x540": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_680x540.5947163617_98eq.jpg",
            "url_570xN": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_570xN.5947163617_98eq.jpg",
            "url_372x296": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_372x296.5947163617_98eq.jpg",
            "url_744x592": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_744x592.5947163617_98eq.jpg",
            "url_642xN": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_642xN.5947163617_98eq.jpg",
            "url_794xN": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_794xN.5947163617_98eq.jpg",
            "url_1588xN": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_1588xN.5947163617_98eq.jpg",
            "url_600x600": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_600x600.5947163617_98eq.jpg",
            "url_1140xN": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_1140xN.5947163617_98eq.jpg",
            "url_1000x1000": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_1000x1000.5947163617_98eq.jpg",
            "url_175x175": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_175x175.5947163617_98eq.jpg",
            "url_500x500": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_500x500.5947163617_98eq.jpg",
            "url_300x200": "https://i.etsystatic.com/51167133/r/il/2f133b/5947163617/il_300x200.5947163617_98eq.jpg",
            "volume": 226,
            "version": 1,
            "extra_data": "98eq",
            "extension": "",
            "color": None,
            "blur_hash": "LmHCJy-=bw%L_4x^tRnlx]bJaeWA",
            "hue": None,
            "saturation": None,
            "height": 184,
            "width": 185,
            "alt_text": None
        }
    ],
    "videos": [],
    "source_shipping_profile_id": 229607947047,
    "state_date": 1712384081,
    "ending_date": 1722924881,
    "formatted_create_date": "Apr 6, 2024",
    "formatted_ending_date": "Aug 6, 2024",
    "formatted_update_date": "Apr 6, 2024",
    "formatted_original_create_date": "Apr 6, 2024",
    "short_url": None,
    "item_weight": None,
    "item_weight_unit": "g",
    "item_length": None,
    "item_width": None,
    "item_height": None,
    "item_dimensions_unit": "mm",
    "should_auto_renew": True,
    "display_unit_price": False,
    "requires_renew_before_activation": False,
    "is_inventory_backwards_compatible": True,
    "inventory_product_count": 1,
    "inventory_min_price": "100.00",
    "inventory_min_price_with_symbol": "USD 100",
    "inventory_min_price_int": 10000,
    "inventory_max_price": "100.00",
    "inventory_max_price_with_symbol": "USD 100",
    "inventory_max_price_int": 10000,
    "is_inventory_unified": False,
    "is_waitlist_enabled": False,
    "waitlist_subscriptions": 0,
    "waitlist_offering_subscriptions": 0,
    "product_identifiers": [],
    "has_buyer_promise_free_shipping": False,
    "is_promoted": False,
    "needs_to_be_reviewed": False,
    "channel_constants": [
        {
            "sales_channel_id": 1,
            "maximum_product_quantity": 999,
            "minimum_product_price": {
                "amount": 20,
                "divisor": 100,
                "currency_code": "USD",
                "currency_formatted_short": "USD 0.20",
                "currency_formatted_long": "USD 0.20 USD",
                "currency_formatted_raw": "0.20"
            },
            "maximum_product_price": {
                "amount": 5000000,
                "divisor": 100,
                "currency_code": "USD",
                "currency_formatted_short": "USD 50,000.00",
                "currency_formatted_long": "USD 50,000.00 USD",
                "currency_formatted_raw": "50,000.00"
            }
        }
    ],
    "digital_fulfillment": 0,
    "in_cart_count": 0,
    "has_domestic_price": False,
    "has_listing_readiness_survey_response": False,
    "production_cost": None,
    "can_write_inventory_data": True,
    "primary_shipping_cost": "USD 0",
    "auto_renewal_blocked_context": None,
    "auto_renewal_blocked_date": None,
    "listing_publish_alert_variant": "v2"
}

with open('fds.json', 'r') as file:
    cookies = json.load(file)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'referer': 'https://www.etsy.com/your/shops/Theclothesofthewest/tools/listings/create',
}
session.cookies.update(cookies)

response = session.post(url, json=data, headers=headers)

# Проверяем ответ сервера
if response.status_code == 200:
    print("Товар успешно добавлен!")
else:
    print("Ошибка при добавлении товара. Код ошибки:", response.status_code)
    print("Текст ошибки:", response.text)
