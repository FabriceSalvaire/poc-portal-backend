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

import stripe   # https://github.com/stripe/stripe-python

from app.core.config import settings

####################################################################################################

class StripeWebhookError(NameError):
    pass

####################################################################################################

def construct_event(stripe_signature: str, body: str):
    try:
        # event = stripe.Event.construct_from(body, settings.STRIPE_API_KEY)
        # https://stripe.com/docs/webhooks/signatures
        # construct_event requires raw JSON to verify the signature
        event = stripe.Webhook.construct_event(
            body,
            stripe_signature,
            settings.STRIPE_ENDPOINT_SECRET,
        )
        return event
    except ValueError as e:
        raise StripeWebhookError("Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise StripeWebhookError(f"Invalid signature: {e}")
