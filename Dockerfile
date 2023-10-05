FROM python:latest

WORKDIR /app

COPY . /app/

RUN pip install -r /app/requirements.txt
RUN python3 manage.py collectstatic --noinput
RUN useradd -u 8877 nonroot

USER nonroot

ENV ENV='DOCKER_DEV'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000


CMD ["/bin/bash", "./docker_start.sh"]