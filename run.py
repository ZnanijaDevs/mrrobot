import init_app

import logging
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from mrrobot import bot
import mrrobot.handlers


async def run_bot():
    logging.info("Booting the bot...")

    handler = AsyncSocketModeHandler(bot)
    await handler.start_async()


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_bot())
