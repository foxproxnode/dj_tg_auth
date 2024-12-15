FROM python:3.12

WORKDIR /app
RUN pip install poetry
# install requirements into a separate layer
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . ./app