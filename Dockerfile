# Use an official Python runtime based on Debian 11 "bullseye" as a parent image.
FROM python:3.8.13-slim-bullseye as app

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=cms.settings.base \
    PORT=8000



# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
    postgresql-client \
    python-dev \
    # WeasyPrint dependencies \
    python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Install nodejs LTS
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    nodejs \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install and set up Poetry for python dependencies management
ENV POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_PATH="/usr/venvs" \
    POETRY_REPOSITORIES={}

# Install the project requirements.
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

COPY ./pyproject.toml /
COPY ./poetry.lock /
RUN . $HOME/.poetry/env && \
    poetry self update && \
    poetry install

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Install node packages
ENV NPM_CONFIG_CACHE=/tmp/.npm
RUN npm install
RUN npm run build

# Touch the .env file so things don't error out
RUN touch /app/cms/settings/.env

# Collect static files.
RUN python manage.py collectstatic --noinput --clear
ENTRYPOINT ["./entrypoint.sh"]

CMD gunicorn --access-logfile - cms.wsgi:application
