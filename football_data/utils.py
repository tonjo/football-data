import json
import re
from types import SimpleNamespace


def json2obj(data):
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


def validate_date(d):

    if d:
        d = str(d)
        pattern = re.compile(r"[1-9][0-9]{3}-[0-9]{2}-[0-9]{2}")
        if pattern.match(d):
            return True
    return False
