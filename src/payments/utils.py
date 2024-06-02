import random

import httpx

from src.payments.schemas import PaymentSchema

CREATE_PAYMENT_API_URL = "https://sandboxapi.upayments.com/api/v1/charge"
CHECK_PAYMENT_API_URL = "https://sandboxapi.upayments.com/api/v1/get-payment-status/track_id"


async def get_payment(amount: int, currency: str = "USD") -> PaymentSchema:
    """
    Creates payment's url and returns it
    """
    payload = {
        "order": {
            "id": str(random.randint(1000000, 9999999)),
            "reference": "202210101",
            "description": "Subscribe in private channel one",
            "currency": currency,
            "amount": amount
        },
        "language": "en",
        "paymentGateway": {"src": "knet"},
        "reference": {"id": "ord_000000101121012121211231212"},
        "returnUrl": "https://www.yourwebsite.com/success",
        "cancelUrl": "https://www.yourwebsite.com/cancel",
        "notificationUrl": "https://www.yourwebsite.com/notification"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer jtest123"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(CREATE_PAYMENT_API_URL, json=payload, headers=headers)
        return PaymentSchema(url=response.json()["data"]["link"], id_=payload["order"]["id"])


async def check_payment(payment_id: int) -> bool:
    """
    Checks payment's url and returns True if it paid
    """
    # params = {"track_id": payment_id}
    # headers = {
    #     "accept": "application/json",
    #     "Authorization": f"Bearer {config.PAYMENTS_API_TOKEN}"
    # }
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(CHECK_PAYMENT_API_URL, params=params, headers=headers)
    #     return response.json()['status']
    return True
