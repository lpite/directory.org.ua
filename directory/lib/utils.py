from typing import TypeVar

T = TypeVar("T")


def chunks(items: list[T], n: int) -> list[T]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(items), n):
        yield items[i : i + n]
