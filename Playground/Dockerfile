FROM python:3.11-slim
RUN groupadd -r groupplaygrounds && useradd -r -g groupplaygrounds usersport

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
WORKDIR /app/Playground
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER usersport