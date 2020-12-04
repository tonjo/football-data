import json
from types import SimpleNamespace


def json2obj(data):
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
