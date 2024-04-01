# FROM ubuntu:20.04
FROM python:3.10-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m GUI.start_db
COPY . .
EXPOSE 8050


