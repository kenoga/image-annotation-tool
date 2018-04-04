FROM python:3.5.2-alpine

RUN pip install --upgrade pip
RUN pip install flask==0.12

RUN apk update
RUN apk add vim git tig bash
