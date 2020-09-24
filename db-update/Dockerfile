FROM ubuntu:latest
MAINTAINER shadi.boomi@gmail.com

WORKDIR /db-update

RUN apt-get update && apt-get install -y \
    python=3.8 \
    python3-pip \
    cron

COPY requirements.txt .

RUN pip3 install -U pip && pip install -r requirements.txt

COPY . .

RUN chmod 0644 cron-job
RUN touch cron.log

CMD cron && tail -f cron.log