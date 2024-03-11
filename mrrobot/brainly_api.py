from .api import BrainlyAPI
from .util import env


brainly_api = BrainlyAPI(
    host=env("ZNANIJA_API_HOST"),
    token=env("ZNANIJA_API_TOKEN")
)
