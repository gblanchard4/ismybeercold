FROM resin/rpi-raspbian:jessie

# switch on systemd init system in container
ENV INITSYSTEM on

# arch
ENV DIST_ARCH linux-armv7
ENV NODE_EXPORTER_VERSION 0.15.2

# downloading utils
RUN apt-get update && apt-get install wget

# alertmanager deps
RUN apt-get install build-essential libc6-dev

# Set our working directory
WORKDIR /usr/src/app

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt

# pip install python deps from requirements.txt on the resin.io build server
RUN apt-get install python3-pip python3-dev
RUN pip3 install -r /requirements.txt

# This will copy all files in our root to the working  directory in the container
COPY . ./

WORKDIR /etc

WORKDIR /

COPY start.sh ./

WORKDIR /usr/src/app

# main.py will run when container starts up on the device
CMD ["bash", "start.sh"]
