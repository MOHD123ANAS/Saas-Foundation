from email.policy import default
from xmlrpc.client import boolean

import stripe
from decouple import config
DJANGO_DEBUG=config('DJANGO_DEBUG',default=False,cast=boolean)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY",default="",cast=str)

if "sk_test" in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError("Invalid stripe key for prod")

stripe.api_key = STRIPE_SECRET_KEY
def create_customer(name="",email="",metadata={},raw=False):
    response = stripe.Customer.create(
        name=name,
        email=email,
        metadata=metadata,
    )
    if raw:
        return response
    stripe_id = response.id
    return stripe_id