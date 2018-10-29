FROM resin/raspberry-pi2-python:3.6.1

# Enable systemd
ENV INITSYSTEM on

# Working directory
ENV APP /ismybeercold

# Set our working directory
RUN mkdir $APP
WORKDIR $APP

# uWSGI Port
EXPOSE 5000

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# This will copy all files in our root to the working  directory in the container
COPY . $APP

# Start uwsgi
CMD ["uwsgi", "--ini" "app.ini"]
