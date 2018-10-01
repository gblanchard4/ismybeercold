#!/usr/bin/python
import datetime
import psutil
import logging
import os
from flask import Flask, render_template, jsonify
from w1thermsensor import W1ThermSensor
from uptime import uptime

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
    temperature = "{0:.2f}".format(temperature)
    temperature = float(temperature)
    return temperature

@app.route("/")
def ismybeercold():
    global page_views
    print("page_views incremented")
    return render_template('index.html', title="ISMYBEERCOLD?")

@app.route("/_jsondata")
def jsondata():
    uptime_var = int(uptime())
    temp = read_temp()
    tempString = str(temp)
    if temp >= 60.0:
        saying = "Oh Shit, That Beer Is Hot!"
    else:
        saying = "Yeah That Beer Is Cold!"
    timeString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cpu_percent = psutil.cpu_percent()
    virtmem_percent = psutil.virtual_memory()[2]
    return jsonify(uptime=uptime_var, temp=tempString, time=timeString, cpu=cpu_percent, ram=virtmem_percent, saying=saying)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
