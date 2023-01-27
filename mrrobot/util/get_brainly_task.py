from http import HTTPStatus
from httpx import AsyncClient, HTTPError, ConnectError
from mrrobot.util import env


REQUEST_TIMEOUT = 10
ZNANIJA_API_GATEWAY_AUTH_TOKEN = env("ZNANIJA_API_GATEWAY_AUTH_TOKEN")
ZNANIJA_API_GATEWAY_HOST = env("ZNANIJA_API_GATEWAY_HOST")


class BrainlyTaskDoesNotExistException(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id

        super().__init__(f"Task #{task_id} does not exist")


class BrainlyRequestFailedException(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)


async def get_brainly_task(task_id: int) -> dict:
    """Get a Brainly task by ID"""
    async with AsyncClient(
        base_url=ZNANIJA_API_GATEWAY_HOST,
        headers={
            "Authorization": f"Basic {ZNANIJA_API_GATEWAY_AUTH_TOKEN}",
            "X-Service": "mrrobot-slack-bot"
        },
        http2=True,
        timeout=REQUEST_TIMEOUT
    ) as client:
        try:
            response = await client.get(f"/tasks/{id}")

            if response.status_code != HTTPStatus.OK:
                raise HTTPError("Response status must be 200 OK")

            data = response.json()
            if data is None:
                raise BrainlyTaskDoesNotExistException(task_id)
        except (HTTPError, ConnectError) as exc:
            raise BrainlyRequestFailedException(f"Request to the Brainly service failed: {str(exc)}") from None

    return data
