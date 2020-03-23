from redis import Redis as _Redis
from pickle import dumps, loads, HIGHEST_PROTOCOL, UnpicklingError

from swiper.conf import REDIS


class Redis(_Redis):
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        pickled_data = dumps(value)
        return super().set(name, pickled_data, ex, px, nx, xx)

    def get(self, name, default=None):
        pickled_data = super().get(name)
        if pickled_data is None:
            return default
        else:
            try:
                value = loads(pickled_data)
            except UnpicklingError:
                return pickled_data
            else:
                return value

    def hmset(self, name, mapping):
        for k, v in mapping.items():
            mapping[k] = dumps(v, HIGHEST_PROTOCOL)
        return super().hmset(name, mapping)

    def hmget(self, name, keys, *args):
        values_list = super().hmget(name, keys, *args)
        for idx, value in enumerate(values_list):
            if value is not None:
                try:
                    values_list[idx] = loads(value)
                except UnpicklingError:
                    pass
        return values_list

    def hgetall(self, name):
        mapping = super().hgetall(name)
        for k, v in mapping.items():
            try:
                mapping[k] = loads(v)
            except UnpicklingError:
                pass
        return mapping


rds = Redis(**REDIS)

