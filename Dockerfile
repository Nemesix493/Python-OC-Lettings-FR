FROM python:latest
WORKDIR /app
COPY . /app/
RUN pip install -r /app/requirements.txt
EXPOSE 8000
CMD ["python", "-m", "manage", "runserver"]