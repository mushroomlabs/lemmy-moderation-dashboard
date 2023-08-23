# Start with a Python image.
FROM python:3.12-slim-bookworm AS builder

RUN apt-get update
RUN apt-get install build-essential cargo -y

# Install poetry
RUN pip install poetry

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# Install project dependencies
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR


# Copy all relevant files into the image.
COPY ./lemmy_moderation_dashboard /app/lemmy_moderation_dashboard

FROM builder as release
COPY ./README.md /app
# Install our requirements.
RUN poetry install --without dev

FROM builder as development
COPY ./pytest.ini /app
COPY ./setup.cfg /app/lemmy_moderation_dashboard
RUN poetry install
