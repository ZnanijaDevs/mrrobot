from logging import Logger
from mrrobot import bot
from mrrobot.util import get_user


async def fetch_message_data(context: dict, payload: dict, logger: Logger, next):
    if payload.get("type") == "reaction_added":
        item_ts = payload["item"]["ts"]
        channel_id = payload["item"]["channel"]

        data = await bot.client.conversations_history(
            limit=1,
            channel=channel_id,
            inclusive=True,
            latest=item_ts
        )
        messages: list[dict] = data["messages"]

        if len(messages) == 0:
            logger.info(f"Message with ts {item_ts} not found in #{channel_id}")

        found_message = messages[0]
        if found_message["ts"] != item_ts:
            logger.info(f"""
            The timestamp of the found message is not equal to `item_ts` ({item_ts}).
            Maybe item is a message in a thread.
            Found message: {found_message}
            """)
            return

        context["message"] = found_message
        context["message_user"] = await get_user(found_message["user"])
    elif payload.get("type") == "message" and "subtype" not in payload:
        context["message"] = payload

    await next()
