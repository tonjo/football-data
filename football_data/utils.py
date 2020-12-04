import os
import requests
import logging
logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# TODO NOT USED
def headers():
    try:
        api_key = os.environ['FOOTBALL_API_KEY']
        return {"X-Auth-Token": api_key}
    except:
        return {}


def api_request(url, headers):
    try:
        res = requests.get(url, headers=headers).json()
        if 'errorCode' in res or 'error' in res:
            msg = res['message']
            logger.error(msg)
            return False
        else:
            return res
    except:
        msg = 'requests.get error'
        logger.error(msg)
        return False
