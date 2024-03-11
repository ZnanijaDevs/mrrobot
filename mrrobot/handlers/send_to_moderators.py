import re
from logging import Logger
from slackblocks import Message, SectionBlock, ContextBlock, Text
from mrrobot import bot
from mrrobot.config import SlackChannel, GSHEET_INSERT_ROW_INDEX, CORRECTION_EMOJI
from mrrobot.db import gsheet
from mrrobot.matchers import has_brainly_task_link
from mrrobot.middleware import fetch_user_data
from mrrobot.util import delete_message, ts_to_date, get_url_with_brainly_host
from mrrobot.brainly_api import brainly_api


@bot.message(
    keyword=re.compile(rf":{CORRECTION_EMOJI}:"),
    matchers=[has_brainly_task_link],
    middleware=[fetch_user_data]
)
async def send_wrong_content_to_moderators(message: dict, context: dict, logger: Logger, ack):
    await ack()

    task_id = context["brainly_task_id"]
    task = await brainly_api.get_question(task_id)

    if task is None:
        logger.warn(f"We cannot send wrong content to moderators because task {task_id} has been deleted")
        return

    task_link = get_url_with_brainly_host(f"/task/{task_id}")
    reason = re.sub(r":[\w\d]*:|<[\w:\/\.|]*>", "", message["text"]).strip()

    await delete_message(channel_id=message["channel"], ts=message["ts"])
    await bot.client.chat_postMessage(**Message(
        channel=SlackChannel.MODERATORS.value,
        text=f"#moderators - {task_link}",
        blocks=[
            SectionBlock(f"<{task_link}> - *{task.subject}* (ответы: {task.answers_count})\n{reason}"),
            SectionBlock(task.short_content),
            ContextBlock(Text(f"<@{message['user']}>"))
        ]
    ))

    gsheet.worksheet("#moderators logs").insert_row([
        task["link"],
        task.subject or "#N/A",
        reason,
        ts_to_date(message["ts"]),
        context["user_data"]["nick"],
        message["text"],
        task.answers_count,
        task.created
    ], GSHEET_INSERT_ROW_INDEX)
