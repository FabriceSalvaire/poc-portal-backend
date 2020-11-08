####################################################################################################
#
# POC - 
# Copyright (C) 2020 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

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
