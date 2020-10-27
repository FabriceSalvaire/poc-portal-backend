####################################################################################################

import subprocess

import stripe   # https://github.com/stripe/stripe-python

from app.core.config import settings

####################################################################################################
#
# https://stripe.com/docs/cli/docker
#
# Build stripe-cli
#     > git clone https://github.com/stripe/stripe-cli
#     > cd stripe-cli
#     > make setup
#     > make test
#     > make build
#
# Login to Stripe CLI
#     > stripe login
#         Your pairing code is: whoa-remedy-homage-proud
#         This pairing code verifies your authentication with Stripe.
#         Press Enter to open the browser (^C to quit)
#         > Done! The Stripe CLI is configured for Stripe Test with account id acct_b1hCDtA3QHdcBKz9
#
#         Please note: this key will expire after 90 days, at which point you'll need to re-authenticate.
#
# Start Webhook forwarder
#     > stripe listen --forward-to localhost:8000/api/v1/stripe_webhook/
#         > Ready! Your webhook signing secret is whsec_h1sMQd6YTJYLiVYhayaJyOyJO5nJIDRE (^C to quit)
#
# Resend an event for a payment
#     Go to Dashboard/Payments
#         https://dashboard.stripe.com/test/payments
#     Pickup a payment
#         https://dashboard.stripe.com/test/payments/pi_1HgYuXBKQhCtA3D9az0sivEk
#     Select an event in the activity list and click on "View event detail" to get the event id
#         https://dashboard.stripe.com/test/events/evt_1HgYxPBKQhCtA3D9ro1Z9V1b
#
#     > stripe events resend evt_1HgYxPBKQhCtA3D9ro1Z9V1b
#         {
#           "id": "evt_1HgYxPBKQhCtA3D9ro1Z9V1b",
#           "object": "event",
#           "api_version": "2020-08-27",
#           "created": 1603731247,
#           "data": {
#             "object": {
#               "id": "cs_test_873IUJbhvZNjltdATfDfGFDgIJcrfFmT0vMkeT5pxNWP6BnijNjTqrrA",
#               "object": "checkout.session",
#               "allow_promotion_codes": null,
#               "amount_subtotal": 5000,
#               "amount_total": 5000,
#               "billing_address_collection": null,
#               "cancel_url": "http://localhost:3000/checkout?canceled=true",
#               "client_reference_id": null,
#               "currency": "eur",
#               "customer": "cus_IH7BaClMwFkpjZ",
#               "customer_email": "john.doe@example.com",
#               "livemode": false,
#               "locale": null,
#               "metadata": {
#               },
#               "mode": "payment",
#               "payment_intent": "pi_1HgYuXBKQhCtA3D9az0sivEk",
#               "payment_method_types": [
#                 "card"
#               ],
#               "payment_status": "paid",
#               "setup_intent": null,
#               "shipping": null,
#               "shipping_address_collection": null,
#               "submit_type": null,
#               "subscription": null,
#               "success_url": "http://localhost:3000/checkout?success=true",
#               "total_details": {
#                 "amount_discount": 0,
#                 "amount_tax": 0
#               }
#             }
#           },
#           "livemode": false,
#           "pending_webhooks": 2,
#           "request": {
#             "id": null,
#             "idempotency_key": null
#           },
#           "type": "checkout.session.completed"
#         }
#
#      Stripe Forwarder should log
#         2020-10-27 13:48:09   --> checkout.session.completed [evt_1HgYxPBKQhCtA3D9ro1Z9V1b]
#         2020-10-27 13:48:09  <--  [404] POST http://localhost:8000/stripe_webhook/ [evt_1HgYxPBKQhCtA3D9ro1Z9V1b]

####################################################################################################

class StripeCliWrapper:

    ##############################################

    def __init__(self, stripe="stripe"):
        self._stripe = stripe

    ##############################################

    # stripe config --list

    ##############################################

    def stripe_login(self):
        """Require to authenticate in browser"""
        command = (
            self._stripe,
            "login",
            # "--interactive",
            # "--project-name=",
            # "--api-key=",    # sk_... or use env STRIPE_API_KEY
        )
        subprocess.call(command, shell=True)

    ##############################################

    def stripe_listen(self, endpoint_url="localhost:8000/webhook/"):
        """Note: it is a daemon like command"""
        command = (self._stripe, "listen", "--forward-to", endpoint_url)
        subprocess.call(command, shell=True)

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
