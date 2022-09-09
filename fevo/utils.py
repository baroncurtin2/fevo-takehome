import os
from datetime import datetime

from dotenv import dotenv_values


def get_api_key(api_key: str = None) -> str:
    if api_key is not None:
        return api_key

    # if api_key is not passed, check environment
    env_vars = dotenv_values()
    return env_vars.get("API_KEY") or os.getenv("API_KEY") or None


def parse_date_strings(date_str: str, date_format: str = "%Y-%m-%d") -> datetime:
    return datetime.strptime(date_str, date_format)
