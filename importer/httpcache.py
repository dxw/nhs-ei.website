import requests
import requests_cache
import sys
import os
import logging
import time

from django.conf import settings

logger = logging.getLogger("__name__")

CACHE_DB = "requests_cache.sqlite"


def my_request(*args, **kwargs):
    logger.debug("REQUEST %s %s", args, kwargs)
    while True:
        try:
            values = session._request(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            logger.critical("Aborted connection? %s", e)
            print("\007")  # beep!
            time.sleep(300)
        except Exception as e:
            logger.critical("Error making request: %s", e)
        else:
            break

    return values


if "reset" in sys.argv:
    os.remove(CACHE_DB)
    print("Removed old HTTP cache.")

if settings.DEBUG:
    session = requests_cache.CachedSession(CACHE_DB, allowable_codes=(200, 404))
    session._request = session.request
    session.request = my_request
else:
    session = requests.session()


if __name__ == "__main__":
    print("Quick test: this should take 2 or 0 seconds")
    for i in range(5):
        session.get("http://httpbin.org/delay/2")
    print("Done.")
