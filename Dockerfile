FROM python:latest

WORKDIR /app

COPY . /app/

RUN pip install -r /app/requirements.txt
RUN python3 manage.py collectstatic --noinput
RUN useradd -u 8877 nonroot

USER nonroot

ENV DJANGO_SECRET_KEY='fp$9^593hsriajg$_%=5trot9g!1qa@ew(o-1#@=&4%=hp46(s'
ENV ENV='DOCKER_DEV'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000


CMD ["/bin/bash", "./docker_start.sh"]