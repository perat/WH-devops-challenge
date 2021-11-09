# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# RUN apt-get update -y && \
#     apt-get install -y python-pip python-dev && \
#     rm -rf /var/lib/apt/lists/*

RUN groupadd app_group && \
    useradd --create-home -g app_group app_user 

USER app_user:app_group
WORKDIR /home/app_user

# We copy just the requirements.txt first to leverage Docker cache
COPY src/python/flask-api-key-package/requirements.txt ./
RUN pip install -r requirements.txt

COPY src/python/flask-api-key-package/flask-api-key/* ./
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
EXPOSE $FLASK_RUN_PORT
CMD [ "python3", "-m" , "flask", "run"]
