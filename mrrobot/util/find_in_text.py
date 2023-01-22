import re
from mrrobot.config import DELETION_REASON_REGEX, TASK_ID_REGEX, PROFILE_LINK_REGEX


def get_deletion_reason(text: str) -> str | None:
    """Get deletion reason in the text"""
    match = re.search(DELETION_REASON_REGEX, text, re.IGNORECASE)

    if match is None:
        return None

    return re.sub(r"(^,|-)\s*|\.$", "", match.group()).strip().capitalize()


def find_profile_link(text: str) -> str | None:
    """Find link to a user profile on Brainly in the text"""
    link = re.search(PROFILE_LINK_REGEX, text)
    return link.group() if link is not None else None


def find_task_id(text: str) -> int | None:
    """Find task ID in the text"""
    task_id = re.search(TASK_ID_REGEX, text)

    if task_id is None:
        return

    return int(task_id.group())


def find_user_id_in_profile_link(link: str) -> int:
    """
    Find user ID in the link to a user profile on Brainly.
    Allowed formats: `https://znanija.com/profil/nick-1`, `https://znanija.com/users/redirect_user/1` and
    `https://znanija.com/users/user_content/1`
    """
    splitted_link = link.split("/")
    last_item_in_splitted_link = splitted_link[-1]

    if "-" in last_item_in_splitted_link:
        return int(last_item_in_splitted_link.split("-")[-1])
    else:
        return int(last_item_in_splitted_link)
