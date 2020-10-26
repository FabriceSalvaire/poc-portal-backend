####################################################################################################

__all__ = ["create_checkout_session", "PaymentStatus"]

####################################################################################################

from enum import auto

from fastapi_utils.enums import StrEnum

import stripe   # https://github.com/stripe/stripe-python

from app.core.config import settings

####################################################################################################

stripe.api_key = settings.STRIPE_API_KEY

####################################################################################################

class PaymentStatus(StrEnum):
    incomplete = auto()   # The customer has not entered their payment method
    succeeded = auto()    # This payment is complete
    # ...   # Fixme: complete

####################################################################################################

class StripeError(NameError):
    pass

####################################################################################################

def create_checkout_session(
        customer_email: str,
        amount: int,
        product_name: str,
        callback_url: str,
        success_suffix_url: str = "/success.html",
        cancel_suffix_url: str = "/cancel.html",
) -> int:
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=customer_email,
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "unit_amount": amount,
                        "product_data": {
                            "name": product_name,
                            # "images": ["https://"],
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=callback_url + success_suffix_url,
            cancel_url=callback_url + cancel_suffix_url,
        )
        return checkout_session.id
    except Exception as e:
        # Fixme: logging
        print(e)
        raise StripeError("...")
