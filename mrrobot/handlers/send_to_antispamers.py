import re
from slackblocks import Message, SectionBlock, ContextBlock, Text
from mrrobot import bot
from mrrobot.config import SlackChannel, GSHEET_INSERT_ROW_INDEX
from mrrobot.db import gsheet
from mrrobot.matchers import has_brainly_task_link
from mrrobot.middleware import fetch_user_data
from mrrobot.util import get_brainly_task, delete_message, ts_to_date


@bot.message(
    keyword=re.compile(r"снять\s{1,}(отметку|нарушение)", re.IGNORECASE),
    matchers=[has_brainly_task_link],
    middleware=[fetch_user_data]
)
async def send_reported_content_to_antispamers(message: dict, context: dict, ack, say):
    await ack()

    task = await get_brainly_task(context["brainly_task_id"])

    await delete_message(channel_id=message["channel"], ts=message["ts"])
    await bot.client.chat_postMessage(**Message(
        channel=SlackChannel.ANTISPAMERS.value,
        text=f"#antispamers - {task['link']}",
        blocks=[
            SectionBlock(f":triangular_flag_on_post: {task.get('subject', '')} {task['link']}"),
            SectionBlock(task["short_content"] or "No content"),
            ContextBlock(Text(f"{message['text']}\n<@{message['user']}>")),
        ]
    ))

    gsheet.worksheet("#antispamers logs").insert_row([
        task["link"],
        context["user_data"]["nick"],
        ts_to_date(message["ts"]),
        message["text"]
    ], GSHEET_INSERT_ROW_INDEX)
