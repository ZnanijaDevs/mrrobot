import re
from logging import Logger
from slackblocks import Message, SectionBlock, ContextBlock, Text
from mrrobot import bot
from mrrobot.config import SlackChannel, GSHEET_INSERT_ROW_INDEX
from mrrobot.db import gsheet
from mrrobot.matchers import is_event_in_help_channel, has_correction_reaction
from mrrobot.middleware import fetch_message_data
from mrrobot.middleware import fetch_user_data
from mrrobot.util import delete_message, ts_to_date, find_task_id, get_url_with_brainly_host
from mrrobot.brainly_api import brainly_api


@bot.event(
    event="reaction_added",
    matchers=[is_event_in_help_channel, has_correction_reaction],
    middleware=[fetch_user_data, fetch_message_data]
)
async def handle_correction_reaction_in_help_channel(context: dict, logger: Logger, ack):
    await ack()

    message = context["message"]

    task_id = find_task_id(message["text"])
    if task_id is None:
        logger.debug(f"cannot find task id in message {message['text']}")
        return

    task = await brainly_api.get_question(task_id)
    if task is None:
        logger.warn(f"User is trying to correct answer in task {task_id}, but it has been deleted")
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
        task_link,
        task.subject or "#N/A",
        reason,
        ts_to_date(message["ts"]),
        context["message_user"]["nick"],
        message["text"],
        task.answers_count,
        task.created
    ], GSHEET_INSERT_ROW_INDEX)
