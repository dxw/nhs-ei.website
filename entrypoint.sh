#!/bin/sh
echo "migrating"
python manage.py migrate --noinput
if [ ${AUTO_COLLECTSTATIC:-0} -eq 1 ]; then
    python manage.py collectstatic --noinput
fi

exec "$@"
