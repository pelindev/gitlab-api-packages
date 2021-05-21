FROM python:3.9-alpine

RUN apk add npm composer git
RUN pip install virtualenv
