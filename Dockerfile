FROM python:3.10.0-slim-buster
RUN pip install poetry

WORKDIR /bot
COPY *.py poetry.lock pyproject.toml .env* /bot
COPY ./mrrobot/ /bot/mrrobot/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --without dev --no-root

ENV "ENV" "production"
CMD ["python", "run.py"]