import aioredis
from mrrobot.util import env


db = aioredis.from_url(env("REDIS_DB_URL"))
