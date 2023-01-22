import re
from slackblocks import Message, SectionBlock, ContextBlock, Text
from mrrobot import bot
from mrrobot.config import SlackChannel, GSHEET_INSERT_ROW_INDEX
from mrrobot.db import gsheet
from mrrobot.matchers import has_brainly_task_link
from mrrobot.middleware import fetch_user_data
from mrrobot.util import get_brainly_task, delete_message, ts_to_date


@bot.message(
    keyword=re.compile(r":arrows_counterclockwise:"),
    matchers=[has_brainly_task_link],
    middleware=[fetch_user_data]
)
async def send_wrong_content_to_moderators(message: dict, context: dict, ack, say):
    await ack()

    task = await get_brainly_task(context["brainly_task_id"])

    subject = task.get("subject", "Unknown subject")
    reason = re.sub(r":[\w\d]*:|<[\w:\/\.|]*>", "", message["text"]).strip()

    await delete_message(channel_id=message["channel"], ts=message["ts"])
    await bot.client.chat_postMessage(**Message(
        channel=SlackChannel.MODERATORS.value,
        text=f"#moderators - {task['link']}",
        blocks=[
            SectionBlock(f"<{task['link']}> - *{subject}* (ответы: {task['answers_count']})\n{reason}"),
            SectionBlock(task["short_content"]),
            ContextBlock(Text(f"<@{message['user']}>"))
        ]
    ))

    gsheet.worksheet("#moderators logs").insert_row([
        task["link"],
        subject,
        reason,
        ts_to_date(message["ts"]),
        context["user_data"]["nick"],
        message["text"],
        task["answers_count"],
        task["created"]
    ], GSHEET_INSERT_ROW_INDEX)
