import requests
import stripe
from rest_framework import status

from config.settings import STRIPE_API_KEY, CUR_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_usd(amount):
    usd_price = 90
    response = requests.get(
        f"https://api.currencyapi.com/v3/latest?apikey={CUR_API_KEY}&currencies=RUB"
    )
    if response.status_code == status.HTTP_200_OK:
        usd_price = amount / response.json()["data"]["RUB"]["value"]
    return int(usd_price)


def create_stripe_product(product):
    return stripe.Product.create(name=product)


def create_stripe_price(amount, product):
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product=product.id,
    )


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
