import pytest
from slack_sdk.errors import SlackApiError
from mrrobot import bot
from mrrobot.util import get_user, delete_message
from mrrobot.config import SlackChannel


async def test_get_slack_user():
    user = await get_user("USLACKBOT")

    assert isinstance(user, dict)
    assert user.get("nick") == "Slackbot"


async def test_get_slack_user_by_invalid_id():
    with pytest.raises(SlackApiError):
        await get_user("...")


async def test_delete_message():
    channel_id = SlackChannel.HELP.value

    new_message = await bot.client.chat_postMessage(
        channel=channel_id,
        text="Test message. This message will be deleted soon."
    )

    message_ts = new_message["ts"]

    await bot.client.chat_postMessage(
        channel=channel_id,
        text="Test thread",
        thread_ts=message_ts
    )

    await delete_message(channel_id=channel_id, ts=message_ts)
