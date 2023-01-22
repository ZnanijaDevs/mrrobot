from mrrobot import bot
from mrrobot.util import delete_message
from mrrobot.matchers import user_is_admin
from mrrobot.config import SILENT_DELETION_REACTION


async def is_silent_deletion_reaction(event: dict) -> bool:
    return event["reaction"] == SILENT_DELETION_REACTION


@bot.event(
    event="reaction_added",
    matchers=[is_silent_deletion_reaction, user_is_admin]
)
async def handle_silent_deletion_reaction_added_event(event: dict):
    await delete_message(
        channel_id=event["item"]["channel"],
        ts=event["item"]["ts"],
        clear_threads=False
    )
