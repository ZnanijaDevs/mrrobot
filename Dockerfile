FROM python:3.11.4-slim-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY *.py poetry.lock pyproject.toml .env* requirements.txt /code/
COPY ./mrrobot/ /code/mrrobot/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --without dev --no-root

ENV ENV=production
CMD ["python", "run.py"]