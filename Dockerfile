FROM resin/raspberry-pi2-python:3.6.1

# Enable systemd
ENV INITSYSTEM on

# Set our working directory
WORKDIR /usr/src/app

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

WORKDIR /ismybeercold
# This will copy all files in our root to the working  directory in the container
COPY src  /ismybeercold

# start.sh will run when container starts up on the device
CMD ["python", "ismybeercold.py"]
