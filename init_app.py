import os
import logging
from dotenv import load_dotenv
import sentry_sdk


# Load environment variables
load_dotenv(".env.production" if os.environ.get("ENV") == "production" else ".env")

# Add logger
logging.basicConfig(level=logging.INFO)

# Init Sentry
SENTRY_IGNORED_EXCEPTIONS = [
    "'NoneType' object has no attribute 'status'",
    "thread_not_found",
    "message_not_found"
]

sentry_sdk.init(
    traces_sample_rate=0,
    before_send=lambda event, hint: event if hint["exc_info"][1].args[0] not in SENTRY_IGNORED_EXCEPTIONS else None
)
