FROM python:3.10.13-slim-bullseye
COPY ./requirements.txt ./requirements.txt

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2.2 \
    TERM=xterm

RUN pip install "poetry==$POETRY_VERSION"
RUN apt-get update && apt-get install make

WORKDIR /starship

COPY pyproject.toml poetry.lock ./

COPY . .

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && \
    poetry build

CMD ["make", "run"]
