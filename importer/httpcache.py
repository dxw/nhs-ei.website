import requests
import requests_cache
import sys
import os
import logging
logger = logging.getLogger("__name__")
"""TODO: this should use the Django config but I haven't figured that out."""
# from django.conf import settings
# DEBUG = settings.DEBUG
DEBUG = True

CACHE_DB = "requests_cache.sqlite"

def my_request(*args, **kwargs):
    logger.debug("REQUEST %s %s", args, kwargs)
    while True:
        try:
            values = session._request(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            logger.critical("Aborted connection? %s", e)
            print ("\007") # beep!
            r = input("Connection Aborted? Press Enter to retry or type something to skip.")
            if r.strip():
                break
        except Exception as e:
            logger.critical("Error making request: %s", e)
        else:
            break

    return values

if "reset" in sys.argv:
    os.remove(CACHE_DB)
    print("Removed old HTTP cache.")

if DEBUG:
    session = requests_cache.CachedSession(CACHE_DB, allowable_codes = (200, 404))
    session._request = session.request
    session.request = my_request
else:
    session = requests.session()


if __name__ == "__main__":
    print("Quick test: this should take 2 or 0 seconds")
    for i in range(5):
        session.get("http://httpbin.org/delay/2")
    print("Done.")
