FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install python3-pip libjpeg-dev libjpeg8-dev sqlite3 redis-tools supervisor -y

RUN mkdir /run/daphne/

WORKDIR /app
COPY ./requirements.txt /app

RUN pip3 install -r requirements.txt

RUN echo "hello"
COPY ./src /app

ENV PORT 8000
EXPOSE 8000
#ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
#ENTRYPOINT [ "daphne", "-u", "/run/daphne/daphne.sock", "--fd", "0", "--access-log", "- --proxy-headers", "main.asgi:application"]
#CMD ["daphne", "-u", "/run/daphne/daphne.sock", "--fd", "0", "main.asgi:application", "--port", "8000", "--bind", "0.0.0.0", "-v2"]
ENTRYPOINT ["daphne", "main.asgi:application", "--port", "8000", "--bind", "0.0.0.0", "-v2"]
#ENTRYPOINT ["docker-entrypoint.sh"]
