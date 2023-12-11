# FROM ubuntu:20.04
FROM python:3.10.12
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y python3.10 python3-pip
WORKDIR /usr/src/app
COPY . ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8050
# CMD ["python3", "-m", "GUI.server"]

