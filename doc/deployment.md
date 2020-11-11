## Deployment

[[_TOC_]]

### Introduction

* Python dependencies are managed by [Poetry](https://python-poetry.org), see [pyproject.toml](pyproject.toml)
* Development and administration tools are implemented as [Invoke](http://www.pyinvoke.org) tasks
  Run the command ```invoke -l``` or ```inv -l``` to get the list of available tasks

### Configurations

* **Global settings** `prod.env`
	Its path is set using the env `BACKEND_SETTINGS_PATH`
* **Logging** `logging.yml`
	Its path is set in the `.env` file

### Create a database on PostgreSQL

See also `app/deployment/postgresql/setup.sh`

Start PostgreSQL
```sh
systemctl start postgresql
```

Then create a database user
```sh
# from root
su - postgres
createuser --pwprompt USER
```

### Start a Stripe Webhook forwarder (dev only)

See also `app/app/stripe/webhook.py`

<!-- https://stripe.com/docs/cli/docker -->

**Install Stripe CLI** using https://stripe.com/docs/stripe-cli documentation.
```sh
git clone https://github.com/stripe/stripe-cli
cd stripe-cli
make setup
make test
make build
```

**Login to Stripe CLI**
```sh
stripe login

# Your pairing code is: whoa-remedy-homage-proud
# This pairing code verifies your authentication with Stripe.
# Press Enter to open the browser (^C to quit)
# > Done! The Stripe CLI is configured for Stripe Test with account id acct_b1hCDtA3QHdcBKz9
#
# Please note: this key will expire after 90 days, at which point you'll need to re-authenticate.
```

**Start Webhook forwarder**
```sh
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
1. Run
   ```sh
   stripe events resend evt_1HgYxPBKQhCtA3D9ro1Z9V1b
   ```
   ```js
   {
     "id": "evt_1HgYxPBKQhCtA3D9ro1Z9V1b",
     ...
   }
   ```
1. Stripe Forwarder should log
   ```
   2020-10-27 13:48:09   --> checkout.session.completed [evt_1HgYxPBKQhCtA3D9ro1Z9V1b]
   2020-10-27 13:48:09  <--  [404] POST http://localhost:8000/stripe_webhook/ [evt_1HgYxPBKQhCtA3D9ro1Z9V1b]
   ```

### Start dev server

```sh
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

# Create and initialise database (require postgres login)
inv database.bootstrap

# Start Uvicorn
uvicorn app.main:app --reload
```

**Now start the frontend**

```sh
cd checkout-frontend
BROWSER="google-chrome" yarn start
```

### Invoke Tasks

* **Create a schema revision** `database.alembic-revision`
* **Upgrade database** `database.alembic-upgrade`
* **Delete donations** `database.delete-donations`
* ...

### Deploy on production

See `app/deployment/` for Nginx and systemd configuration.

**Note:** Stripe webhooks must be set from the dashboard.

# OpenAPI

Open http://localtest.me:8000/docs

*read more on "localtest.me" domain at https://weblogs.asp.net/owscott/introducing-testing-domain-localtest-me*

## Test a donation

**Note:** Stripe will check the url look like an url ...

**JSON payload**:
```js
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

```sh
curl \
 -X POST "http://127.0.0.1:8000/api/v1/donations/" \
 -H  "accept: application/json" \
 -H  "Content-Type: application/json" \
 -d '{"date":"2020-11-08T20:45:43.315Z","int_amount":50,"donator_type":"individual","name":"John Doe","email":"john.doe@example.com","callback_url":"http://localhost:3000/","success_suffix_url":"?success=true","cancel_suffix_url":"?canceled=true"}'
```
