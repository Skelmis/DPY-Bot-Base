from datetime import timedelta, datetime
from typing import Any, Dict

from bot_base.caches import Entry
from bot_base.caches.abc import Cache
from bot_base.exceptions import NonExistentEntry, ExistingEntry


class TimedCache(Cache):
    __slots__ = ("cache",)

    def __init__(self):
        self.cache: Dict[Any, Entry] = {}

    def __contains__(self, item: Any) -> bool:
        try:
            entry = self.cache[item]
            if entry.expiry_time < datetime.now():
                return False
        except KeyError:
            return False
        else:
            return True

    def add_entry(
        self, key: Any, value: Any, *, ttl: timedelta = None, override: bool = False
    ) -> None:
        ttl = ttl or timedelta()
        if key in self and not override:
            raise ExistingEntry

        self.cache[key] = Entry(value=value, expiry_time=(datetime.now() + ttl))

    def delete_entry(self, key: Any) -> None:
        try:
            self.cache.pop(key)
        except KeyError:
            pass

    def get_entry(self, key: Any) -> Any:
        if key not in self:
            raise NonExistentEntry

        return self.cache[key].value

    def force_clean(self) -> None:
        now = datetime.now()
        for k, v in self.cache.items():
            if v.expiry_time < now:
                self.delete_entry(k)