FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /opt/decentmark
WORKDIR /opt/decentmark
ADD requirements.txt /opt/decentmark/
RUN pip install -r requirements.txt
ADD . /opt/decentmark/
