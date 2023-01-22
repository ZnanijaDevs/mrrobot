from cache import AsyncTTL
from mrrobot import bot
from mrrobot.util import env


async def delete_message(channel_id: str, ts: str, clear_threads: bool | None = True):
    """Deletes a message in Slack."""
    if clear_threads:
        replies = await bot.client.conversations_replies(channel=channel_id, ts=ts)
        for reply in replies["messages"]:
            if "parent_user_id" not in reply:
                continue

            await delete_message(
                channel_id=channel_id,
                ts=reply["ts"],
                clear_threads=False
            )

    await bot.client.chat_delete(
        channel=channel_id,
        ts=ts,
        token=env("SLACK_ADMIN_TOKEN")
    )


@AsyncTTL(time_to_live=300)
async def get_user(id: str) -> dict:
    """Retrieve information about a Slack user"""
    data = await bot.client.users_info(user=id)
    user = data["user"]

    return user | {
        "nick": user["profile"]["display_name"] or user["name"]
    }
