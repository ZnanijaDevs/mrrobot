from logging import Logger
import sentry_sdk
from slack_bolt.response import BoltResponse
from slack_bolt.error import BoltUnhandledRequestError
from mrrobot import bot
from mrrobot.util import is_production


@bot.error
async def error_handler(error: Exception, logger: Logger):
    if isinstance(error, BoltUnhandledRequestError):
        return BoltResponse(status=200, body="Unhandled request.")

    if is_production():
        sentry_sdk.capture_exception(error)
    else:
        logger.exception(error)
