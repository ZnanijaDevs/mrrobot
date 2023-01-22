import re
import logging
from mrrobot.config import admins, DANGER_REACTIONS_REGEX, SlackChannel
from mrrobot.util import find_task_id


async def user_is_admin(event: dict) -> bool:
    """Check whether the user is an admin"""
    return event["user"] in admins


async def reaction_is_dangerous(event: dict) -> bool:
    """Check whether the reaction is on the list of dangerous reactions"""
    return re.search(DANGER_REACTIONS_REGEX, event["reaction"]) is not None


def check_event_is_in_channel(event: dict, channel_id: SlackChannel) -> bool:
    """Check whether the event has occured in the specified channel ID"""
    if "item" in event:
        return event["item"]["channel"] == channel_id.value
    elif "channel" in event:
        return event["channel"] == channel_id.value
    else:
        logging.warn(f"Could not find the channel id: {event}")
        return False


async def is_event_in_todelete_channel(event: dict) -> bool:
    return check_event_is_in_channel(event, SlackChannel.TODELETE)


async def is_event_in_help_channel(event: dict) -> bool:
    return check_event_is_in_channel(event, SlackChannel.HELP)


async def is_event_in_moderators_channel(event: dict) -> bool:
    return check_event_is_in_channel(event, SlackChannel.MODERATORS)


async def has_brainly_task_link(message: dict, context: dict) -> bool:
    """Check whether the text of the posted message contains a link to a Brainly task"""
    if (task_id := find_task_id(message["text"])) is None:
        return False

    context["brainly_task_id"] = task_id
    return True
