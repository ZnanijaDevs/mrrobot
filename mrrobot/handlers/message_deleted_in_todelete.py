from logging import Logger
from mrrobot import bot
from mrrobot.util import get_deletion_reason, find_profile_link, find_user_id_in_profile_link, \
    ts_to_date, get_user
from mrrobot.matchers import is_event_in_todelete_channel
from mrrobot.config import GSHEET_INSERT_ROW_INDEX
from mrrobot.db import redis, gsheet


async def has_deletion_data_in_message_text(event: dict, context: dict, logger: Logger) -> bool:
    previous_message: dict | None = event.get("previous_message")
    if previous_message is None or "thread_ts" in previous_message:
        return False

    text = previous_message["text"]
    profile_link = find_profile_link(text)
    deletion_reason = get_deletion_reason(text)

    if not profile_link or not deletion_reason:
        logger.debug(f"Message does not have deletion data: {text} (ts: {previous_message['ts']})")
        return False

    context["profile_link"] = profile_link
    context["deleted_user_id"] = find_user_id_in_profile_link(profile_link)
    context["deletion_reason"] = deletion_reason

    return True


@bot.event(
    event={
        "type": "message",
        "subtype": "message_deleted"
    },
    matchers=[is_event_in_todelete_channel, has_deletion_data_in_message_text]
)
async def handle_message_deleted_in_todelete_event(event: dict, context: dict, ack):
    await ack()

    message = event["previous_message"]
    deleted_user_id = context["deleted_user_id"]

    message_sender = await get_user(message["user"])

    await redis.delete(f"td:{deleted_user_id}:{message['ts']}")
    gsheet.worksheet("#to-delete logs").insert_row([
        ts_to_date(event["event_ts"]),
        context["profile_link"],
        context["deletion_reason"],
        message_sender["nick"],
        ts_to_date(message["ts"]),
        message["text"],
        deleted_user_id
    ], GSHEET_INSERT_ROW_INDEX)
