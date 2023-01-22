from mrrobot import bot
from mrrobot.config import SlackChannel
from mrrobot.matchers import reaction_is_dangerous, is_event_in_moderators_channel
from mrrobot.util import delete_message


@bot.event(
    event="reaction_added",
    matchers=[reaction_is_dangerous, is_event_in_moderators_channel]
)
async def handle_reaction_added_in_moderators_event(event: dict, ack):
    await ack()
    await delete_message(
        channel_id=SlackChannel.MODERATORS.value,
        ts=event["item"]["ts"],
        clear_threads=False
    )
