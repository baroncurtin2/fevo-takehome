from typing import Any, Protocol


class CachingStrategy(Protocol):
    def get_value(self, key: int) -> Any:
        """Returns the value from the cache"""
        pass

    def save(self, key: int, value: Any) -> None:
        """Saves the value in the cache"""
        pass


class DictionaryCachingStrategy:
    cache: dict

    def __init__(self):
        self.cache = {}

    def get_value(self, key: int) -> Any:
        return self.cache.get(key)

    def save(self, key: int, value: Any) -> None:
        self.cache[key] = value


STRATEGIES = {"dict": DictionaryCachingStrategy}
