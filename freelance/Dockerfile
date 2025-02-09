FROM python:3.11-slim
WORKDIR /

ENV DEBIAN_FRONTEND=noninteractive  
RUN apt update && apt install -y \
    gcc g++ python3-dev libpq-dev libfreetype6-dev \
    chromium bash curl unzip && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements/* ./requirements/
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements/dev.txt

EXPOSE 8000
COPY . .
