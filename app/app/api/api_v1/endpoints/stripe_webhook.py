####################################################################################################

# https://stripe.com/docs/webhooks

####################################################################################################

from typing import Any, List

from fastapi import (
    APIRouter, Body, Depends, Header, HTTPException, Request, Response, status,
)
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.stripe import StripeWebhookError, construct_event

####################################################################################################

router = APIRouter()

####################################################################################################

# Headers({
#     'host': 'localhost:8000',
#     'user-agent': 'Stripe/1.0 (+https://stripe.com/docs/webhooks)',
#     'content-length': '1327',
#     'accept': '*/*; q=0.5, application/xml',
#     'cache-control': 'no-cache',
#     'content-type': 'application/json; charset=utf-8',
#     'stripe-signature': 't=1603806669, v1=bb9a7372a112897fca9456b34a6eb60bdd5c1fefdde0a2a0b431792acc77c01d,
#                                        v0=320d48447902b53f829a1b87b31b0370f811c7737df8334efc402131aa01f404',
#     'accept-encoding': 'gzip'
# })

# {
#     'id': 'evt_1HgYxPBKQhCtA3D9ro1Z9V1b',
#     'object': 'event',
#     'api_version': '2020-08-27',
#     'created': 1603731247,
#     'data': {
#         'object': {
#             'id': 'cs_test_873IUJbhvZNjltdATfDfGFDgIJcrfFmT0vMkeT5pxNWP6BnijNjTqrrA',
#             'object': 'checkout.session',
#             'allow_promotion_codes': None,
#             'amount_subtotal': 5000,
#             'amount_total': 5000,
#             'billing_address_collection': None,
#             'cancel_url': 'http://localhost:3000/checkout?canceled=true',
#             'client_reference_id': None,
#             'currency': 'eur',
#             'customer': 'cus_IH7BaClMwFkpjZ',
#             'customer_email': 'john.doe@example.com',
#             'livemode': False,
#             'locale': None,
#             'metadata': {},
#             'mode': 'payment',
#             'payment_intent': 'pi_1HgYuXBKQhCtA3D9az0sivEk',
#             'payment_method_types': ['card'],
#             'payment_status': 'paid',
#             'setup_intent': None,
#             'shipping': None,
#             'shipping_address_collection': None,
#             'submit_type': None,
#             'subscription': None,
#             'success_url': 'http://localhost:3000/checkout?success=true',
#             'total_details': {
#                 'amount_discount': 0,
#                 'amount_tax': 0
#             }
#         }
#     },
#     'livemode': False,
#     'pending_webhooks': 1,
#     'request': {
#         'id': None,
#         'idempotency_key': None
#     },
#     'type': 'checkout.session.completed'
# }

####################################################################################################

@router.post("/", status_code=200)
async def webhook(
        request: Request,
        # stripe_signature: str = Header(None),
        # body: Any = Body(...),   # get raw body
        response: Response,
        db: Session = Depends(deps.get_db),
) -> Any:
    # print(request.headers)
    # print(body)
    # print(stripe_signature, body)
    stripe_signature = request.headers["stripe-signature"]
    body = await request.body()
    try:
        # requires raw JSON to verify the signature
        event = construct_event(stripe_signature, body)
        # print(event)
        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            # print(session)
            stripe_session_id = session["id"]
            payment_status = session["payment_status"]   # "paid"
            print(stripe_session_id, payment_status)
            donation = crud.donation.update_payment_status(db=db, stripe_session_id=stripe_session_id, payment_status=payment_status)
    except StripeWebhookError as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
