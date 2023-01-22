import gspread
from mrrobot.util import env
from mrrobot.config import GOOGLE_SERVICE_ACCOUNT


gc = gspread.service_account_from_dict(GOOGLE_SERVICE_ACCOUNT)

sheet = gc.open_by_key(env("LOG_SHEETS_ID"))
