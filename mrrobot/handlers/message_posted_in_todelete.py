from logging import Logger
from mrrobot import bot
from mrrobot.config import PROFILE_LINK_REGEX
from mrrobot.matchers import is_event_in_todelete_channel
from mrrobot.db import redis


@bot.message(
    keyword=PROFILE_LINK_REGEX,
    matchers=[is_event_in_todelete_channel]
)
async def handle_message_posted_in_todelete_event(message: dict, context: dict, logger: Logger, ack):
    await ack()

    user_id = int(context["matches"][-1])
    if user_id < 1:
        logger.info(f"User id must be greater than 0: {message}")

    await redis.set(f"td:{user_id}:{message['ts']}", f"{message['user']}")
