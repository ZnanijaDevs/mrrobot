from mrrobot.config import admins, SlackChannel
from mrrobot.matchers import user_is_admin, reaction_is_dangerous, has_brainly_task_link, \
    is_event_in_help_channel, is_event_in_moderators_channel, is_event_in_todelete_channel


async def test_user_is_admin_matcher():
    event_with_admin = {"user": admins[0]}
    event_without_admin = {"user": "USER"}

    assert await user_is_admin(event_with_admin) is True
    assert await user_is_admin(event_without_admin) is False


async def test_user_is_not_admin():
    event_without_admin = {"user": "USER"}

    result = await user_is_admin(event_without_admin)
    assert result is False


async def test_reaction_is_dangerous_matcher():
    assert await reaction_is_dangerous({
        "reaction": "white_check_mark"
    }) is True

    assert await reaction_is_dangerous({
        "reaction": "some_random_reaction"
    }) is False


async def test_has_brainly_task_link_matcher():
    message_with_link = {"text": "<https://znanija.com/task/123> test"}
    message_without_link = {"text": "Test"}

    assert await has_brainly_task_link(message_with_link, {}) is True
    assert await has_brainly_task_link(message_without_link, {}) is False


async def test_is_event_in_help_channel_matcher():
    assert await is_event_in_help_channel({
        "channel": SlackChannel.HELP.value
    }) is True

    assert await is_event_in_help_channel({
        "item": {"channel": SlackChannel.TODELETE.value}
    }) is False


async def test_is_event_in_todelete_channel_matcher():
    assert await is_event_in_todelete_channel({
        "item": {"channel": SlackChannel.TODELETE.value}
    }) is True

    assert await is_event_in_todelete_channel({
        "item": {"channel": ""}
    }) is False


async def test_is_event_in_moderators_channel_matcher():
    assert await is_event_in_moderators_channel({
        "item": {"channel": SlackChannel.MODERATORS.value}
    }) is True

    assert await is_event_in_moderators_channel({
        "channel": "Test Channel"
    }) is False
