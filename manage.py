#!/usr/bin/env python
import os
import sys
from django.conf import settings

if __name__ == "__main__":
    if settings.DEBUG:
        if os.environ.get("RUN_MAIN") or os.environ.get("WERKZEUG_RUN_MAIN"):
            import ptvsd

            ptvsd.enable_attach(address=("0.0.0.0", 3000))
            ptvsd.wait_for_attach()
            print("Attached!")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
