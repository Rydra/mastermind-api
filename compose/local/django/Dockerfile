ARG PYTHON_VERSION=3.10.9
FROM python:${PYTHON_VERSION}-slim-buster AS base-stage

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
  # poetry:
  POETRY_VERSION=1.1.13 \
  PATH="$PATH:/root/.local/bin"

ARG POETRY_ENV=production

# Install any required debian packages
COPY install-packages.sh .
RUN chmod +x install-packages.sh && ./install-packages.sh

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_VERSION=1.1.8 python -

# Requirements are installed here to ensure they will be cached.
WORKDIR /tmp
COPY poetry.lock pyproject.toml /tmp/
RUN POETRY_VIRTUALENVS_CREATE=false "/root/.local/bin/poetry" install $(if [ "$POETRY_ENV" = 'production' ]; then echo '--no-dev'; fi)


COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app/src

# this command serves to run the application with django
# CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--conf", "/app/compose/local/django/gunicorn_conf.py", "--preload", "--pythonpath", "/app/src"]
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["/entrypoint"]
