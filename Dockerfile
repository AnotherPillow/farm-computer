FROM python:3.11-alpine

RUN apk update && apk add git

ADD requirements.txt /farm-computer/requirements.txt
RUN pip3 install -r /farm-computer/requirements.txt

WORKDIR /farm-computer
CMD ["python3", "-u", "main.py"]