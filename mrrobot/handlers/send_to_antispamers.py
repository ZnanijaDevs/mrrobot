import re
from logging import Logger
from slackblocks import Message, SectionBlock, ContextBlock, Text
from mrrobot import bot
from mrrobot.config import SlackChannel, GSHEET_INSERT_ROW_INDEX
from mrrobot.db import gsheet
from mrrobot.matchers import has_brainly_task_link
from mrrobot.middleware import fetch_user_data
from mrrobot.util import delete_message, ts_to_date, get_url_with_brainly_host
from mrrobot.brainly_api import brainly_api


@bot.message(
    keyword=re.compile(r"снять\s+(отметку|нарушение)", re.IGNORECASE),
    matchers=[has_brainly_task_link],
    middleware=[fetch_user_data]
)
async def send_reported_content_to_antispamers(message: dict, context: dict, logger: Logger, ack):
    await ack()

    task_id = context["brainly_task_id"]
    task = await brainly_api.get_question(task_id)

    if task is None:
        logger.warn(f"Task {task_id} has been deleted")
        return

    task_link = get_url_with_brainly_host(f"/task/{task_id}")

    await delete_message(channel_id=message["channel"], ts=message["ts"])
    await bot.client.chat_postMessage(**Message(
        channel=SlackChannel.ANTISPAMERS.value,
        text=f"#antispamers - {task_link}",
        blocks=[
            SectionBlock(f":triangular_flag_on_post: {task.subject} {task_link}"),
            SectionBlock(task.short_content or "-"),
            ContextBlock(Text(f"{message['text']}\n<@{message['user']}>")),
        ]
    ))

    gsheet.worksheet("#antispamers logs").insert_row([
        task_link,
        context["user_data"]["nick"],
        ts_to_date(message["ts"]),
        message["text"]
    ], GSHEET_INSERT_ROW_INDEX)
