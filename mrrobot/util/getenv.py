from os import environ
from typing import Any
from functools import cache


@cache
def env(name: str, default_value: Any | None = None) -> Any | None:
    """Get an environment variable"""
    return environ.get(name, default_value)


@cache
def is_production() -> bool:
    """Check whether the current environment is production"""
    return env("ENV") == "production"
