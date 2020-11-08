# Proof of Concept Portal

**Backend Stack**

```
Backend : [ Nginx HTTP proxy <-> Gunicorn * [Uvicorn ASGI] @ Python 3.7 > FastAPI -> PostgreSQL ]

    <--- HTTP JSON XHR / REST API --->

Browser > Web Frontend
```

* [FastAPI](https://fastapi.tiangolo.com) Web Framework to build REST server

 **key features:**
 - fast and competitive
 - asynchronous I/O event loop using [libuv](https://github.com/libuv/libuv)
 - support [OpenAPI](https://github.com/OAI/OpenAPI-Specification) / [JSON Schema](http://json-schema.org)
 - generate automatic interactive documentation
 - load JSON to class object and verify schema
 - support [GraphQL](https://graphql.org)

* [Starlette](https://github.com/encode/starlette) ASGI framework/toolkit
* [Uvicorn](https://www.uvicorn.org) ASGI server as [Gunicorn](https://gunicorn.org) worker
* [SqlAlchemy](https://www.sqlalchemy.org) ORM -> [PostgreSQL](https://www.postgresql.org)
* [MJML](https://mjml.io) Responsive Email Framework

## Deployment

### Configurations

* **Global settings** `prod.env`
	Its path is set using the env `BACKEND_SETTINGS_PATH`
* **Logging** `logging.yml`
	Its path is set in the `.env` file

### Create a database on PostgreSQL

See also `app/deployment/postgresql/setup.sh`

```
# as root

# Start PostgreSQL
systemctl start postgresql

su - postgres
createuser --pwprompt USER
createdb --owner=USER --encoding=UTF8 --template=template0 DATABASE
```

### Start a Stripe Webhook forwarder (dev only)

See also `app/app/stripe/webhook.py`

**Install Stripe CLI** using https://stripe.com/docs/stripe-cli documentation.
```
git clone https://github.com/stripe/stripe-cli
cd stripe-cli
make setup
make test
make build
```

**Login to Stripe CLI**
```
stripe login

# Your pairing code is: whoa-remedy-homage-proud
# This pairing code verifies your authentication with Stripe.
# Press Enter to open the browser (^C to quit)
# > Done! The Stripe CLI is configured for Stripe Test with account id acct_b1hCDtA3QHdcBKz9
#
# Please note: this key will expire after 90 days, at which point you'll need to re-authenticate.
```

**Start Webhook forwarder**
```
stripe listen --forward-to localhost:8000/api/v1/stripe_webhook/

#  Ready! Your webhook signing secret is whsec_h1sMQd6YTJYLiVYhayaJyOyJO5nJIDRE (^C to quit)
```

**==>** copy-paste the secret in the backend `.env` to `STRIPE_ENDPOINT_SECRET` setting

**Resend an event for a payment**
1. Go to Dashboard/Payments
   https://dashboard.stripe.com/test/payments
1. Pickup a payment
   `https://dashboard.stripe.com/test/payments/pi_1HgYuXBKQhCtA3D9az0sivEk`
1. Select an event in the activity list and click on "View event detail" to get the event id
   `https://dashboard.stripe.com/test/events/evt_1HgYxPBKQhCtA3D9ro1Z9V1b`
```
stripe events resend evt_1HgYxPBKQhCtA3D9ro1Z9V1b
```

### Start dev server

```
# Go to backend source directory
cd backend

# Create a virtual environment
python3 -m venv env
source env/bin/activate

# Go to app source directory
cd app

# Install Python dependencies
poetry install

# Setup the environment
source setenv.sh

# Initialise database
inv database.alembic-upgrade
python3 app/initial_data.py

# Start Uvicorn
uvicorn app.main:app --reload
```

**Now start the frontend**

```
cd checkout-frontend
BROWSER="google-chrome" yarn start
```

### Invoke Tasks

* **Create a schema revision** `database.alembic-revision`
* **Upgrade database** `database.alembic-upgrade`
* **Delete donations** `database.delete-donations`

### Deploy on production

See `app/deployment/` for Nginx and systemd configuration.

**Note:** Stripe webhooks must be set from the dashboard.

# OpenAPI

Open http://localtest.me:8000/docs

## Test a donation

**Note:** Stripe will check the url look like an url ...

**JSON payload**:
```
{
  "date": "2020-11-08T20:45:43.315Z",
  "int_amount": 50,
  "donator_type": "individual",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "callback_url": "http://localhost:3000/",
  "success_suffix_url": "?success=true",
  "cancel_suffix_url": "?canceled=true"
}
```

```
curl \
 -X POST "http://127.0.0.1:8000/api/v1/donations/" \
 -H  "accept: application/json" \
 -H  "Content-Type: application/json" \
 -d '{"date":"2020-11-08T20:45:43.315Z","int_amount":50,"donator_type":"individual","name":"John Doe","email":"john.doe@example.com","callback_url":"http://localhost:3000/","success_suffix_url":"?success=true","cancel_suffix_url":"?canceled=true"}'
```
