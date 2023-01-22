from enum import Enum
from mrrobot.util import env


class SlackChannel(Enum):
    HELP = env("HELP_CHANNEL_ID")
    TODELETE = env("TODELETE_CHANNEL_ID")
    ANTISPAMERS = env("ANTISPAMERS_CHANNEL_ID")
    MODERATORS = env("MODERATORS_CHANNEL_ID")


TIMEZONE = "Europe/Minsk"

DANGER_REACTIONS_REGEX = r"check|magic_wand|completed|peacock|reasonable|mary_cheek|^(bug|canc_noj)$"
SILENT_DELETION_REACTION = "test_tube"

TASK_ID_REGEX = r"(?<=\/task\/)\d+(?=\||>|\?)"
PROFILE_LINK_REGEX = r"(?<=<)[A-Za-z:\/]+(znanija\.com)\/((app\/profile\/)|(profil\/\w+-)|(users\/(user_content|redirect_user)\/))(\d+)"
DELETION_REASON_REGEX = r"(?<=\|)[А-Яа-я0-9]+|.+(?=<)|(?<=>)(.|\n)+?[А-Яа-я0-9\s]+"

GSHEET_INSERT_ROW_INDEX = 2
