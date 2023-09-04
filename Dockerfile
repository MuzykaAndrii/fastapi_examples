FROM python:3.11

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random

ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV
RUN $POETRY_VENV/bin/pip install -U pip setuptools
RUN $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR .

COPY poetry.lock pyproject.toml .
COPY . ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction  --no-cache

CMD ["poetry", "run", "python3", "./run.py"]

EXPOSE 8000