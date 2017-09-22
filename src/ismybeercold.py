#!/usr/bin/python
import datetime
import psutil
import logging
import os
from flask import Flask, render_template, request, jsonify
from w1thermsensor import W1ThermSensor
from subprocess import check_output
from datadog import initialize, statsd

dd_options = {
    'api_key':os.environ['DD_API_KEY'],
    'app_key':os.environ['DD_APP_KEY'],
    'hostname':'jeferaptor'
}
initialize(**dd_options)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)

# DS18B20
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
sensor = W1ThermSensor()
temperature = None

def read_temp():
    temperature = sensor.get_temperature(W1ThermSensor.DEGREES_F)
    return temperature

@app.route("/")
def ismybeercold():
    statsd.increment('jeferaptor.page_views')
    return render_template('index.html', title="ISMYBEERCOLD?")

@app.route("/_jsondata")
def jsondata():
    uptime = getUptime()
    temp = read_temp()
    tempString = "{0:.2f}".format(temp)
    if temp >= 60.0:
        saying = "Oh Shit, That Beer Is Hot!"
    else:
        saying = "Yeah That Beer Is Cold!"
    timeString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cpu_percent = psutil.cpu_percent()
    virtmem_percent = psutil.virtual_memory()[2]
    return jsonify(uptime=uptime, temp=tempString, time=timeString, cpu=cpu_percent, ram=virtmem_percent, saying=saying)


def getUptime():
    output = check_output(["uptime"])
    uptime = output[output.find("up"):output.find("user") - 5]
    return uptime

if __name__ == "__main__":
    while TRUE:
        app.run(host='0.0.0.0', port=80, debug=False)
        statsd.histogram('jeferaptor.temperature', "{0:.2f}".format(read_temp()))
