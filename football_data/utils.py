import os
import requests
import json
from types import SimpleNamespace


# TODO NOT USED
def headers():
    try:
        api_key = os.environ['FOOTBALL_API_KEY']
        return {"X-Auth-Token": api_key}
    except:
        return {}


def json2obj(data):
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
