from mrrobot import bot
from mrrobot.config import SlackChannel
from mrrobot.matchers import is_event_in_todelete_channel, reaction_is_dangerous, user_is_admin
from mrrobot.util import delete_message


@bot.event(
    event="reaction_added",
    matchers=[is_event_in_todelete_channel, reaction_is_dangerous, user_is_admin]
)
async def handle_reaction_added_in_todelete_event(event: dict, ack):
    await ack()
    await delete_message(
        channel_id=SlackChannel.TODELETE.value,
        ts=event["item"]["ts"]
    )
