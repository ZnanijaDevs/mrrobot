from mrrobot.util import get_user


async def fetch_user_data(context: dict, payload: dict, next):
    user: dict | str = payload.get("user")
    user_id = user["id"] if isinstance(user, dict) else user

    slack_user = await get_user(user_id)
    context["user_data"] = slack_user

    await next()
