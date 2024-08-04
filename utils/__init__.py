from collections.abc import MutableMapping, Mapping
from typing import ItemsView, Iterator, KeysView, ValuesView, Optional
from cachetools import TTLCache


class bidict[_KT, _KV](MutableMapping[_KT, _KV]):
    def __init__(
        self,
        mapping: Optional[Mapping[_KT, _KV]] = None,
        ttl: Optional[float] = None,
        max_size: Optional[int] = None,
    ) -> None:
        if mapping is None:
            mapping = {}
        if ttl and max_size:
            self.key_to_value = TTLCache(max_size, ttl)
            self.key_to_value.update(mapping)
            vk = {v: k for k, v in mapping.items()}
            self.value_to_key = TTLCache(max_size, ttl)
            self.value_to_key.update(vk)
        else:
            self.key_to_value = dict(mapping)
            self.value_to_key = {v: k for k, v in mapping.items()}

    def keys(self) -> KeysView[_KT]:
        return self.key_to_value.keys()

    def values(self) -> ValuesView[_KV]:
        return self.key_to_value.values()

    def items(self) -> ItemsView[_KT, _KV]:
        return self.key_to_value.items()

    def __setitem__(self, key: _KT, value: _KV) -> None:
        self.key_to_value[key] = value
        self.value_to_key[value] = key

    def __delitem__(self, key: _KT) -> None:
        val = self.key_to_value.pop(key)
        self.value_to_key.pop(val)

    def __getitem__(self, key: _KT) -> _KV:
        return self.key_to_value[key]

    def __len__(self) -> int:
        return len(self.key_to_value)

    def __iter__(self) -> Iterator[_KT]:
        return iter(self.key_to_value)

    def by_key(self, key: _KT, default: Optional[_KV] = None) -> Optional[_KV]:
        return self.key_to_value.get(key, None)

    def by_val(self, val: _KV, default: Optional[_KT] = None) -> Optional[_KT]:
        return self.value_to_key.get(val, None)

    def exist_val(self, val: _KV) -> bool:
        return val in self.value_to_key

    def __repr__(self) -> str:
        return self.key_to_value.__repr__()
