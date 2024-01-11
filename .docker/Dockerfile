FROM python:3.11-alpine

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /app
COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

COPY . .
