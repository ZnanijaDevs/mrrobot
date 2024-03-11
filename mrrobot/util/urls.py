from .getenv import env


def get_url_with_brainly_host(path: str) -> str:
    return env("ZNANIJA_HOST") + path
