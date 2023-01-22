from logging import Logger
from mrrobot import bot
from mrrobot.config import SlackChannel, GSHEET_INSERT_ROW_INDEX
from mrrobot.db import gsheet
from mrrobot.matchers import is_event_in_help_channel, reaction_is_dangerous
from mrrobot.middleware import fetch_user_data, fetch_message_data
from mrrobot.util import delete_message, ts_to_date


@bot.event(
    event="reaction_added",
    matchers=[is_event_in_help_channel, reaction_is_dangerous],
    middleware=[fetch_user_data, fetch_message_data]
)
async def handle_reaction_added_in_help_event(event: dict, context: dict, logger: Logger, ack, say):
    await ack()

    message: dict = context["message"]
    message_user: dict = context["message_user"]
    message_text: str = message["text"]

    event_user: dict = context["user_data"]

    if "<!here>" in message_text or "<!channel>" in message_text:
        logger.info(f"Forbidden to delete messages with @here and @channel: {message}, event user: {event_user['nick']}")
        return

    await delete_message(channel_id=SlackChannel.HELP.value, ts=message["ts"])

    gsheet.worksheet("#help logs").insert_row([
        message_text,
        message_user["nick"],
        ts_to_date(message["ts"]),
        event_user["nick"],
        ts_to_date(event["event_ts"]),
        message_user["is_admin"]
    ], GSHEET_INSERT_ROW_INDEX)
