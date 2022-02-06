import secrets
import uuid
from typing import TypeVar

T = TypeVar("T")


def gen_uuid() -> str:
    return str(uuid.uuid4())


def get_secret(length=32) -> str:
    return secrets.token_urlsafe(length)


def chunks(items: list[T], n: int) -> list[T]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(items), n):
        yield items[i : i + n]
