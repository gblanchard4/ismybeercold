#!/usr/bin/python
import datetime
import psutil
import logging
import os
from flask import Flask, render_template, request, jsonify
from time import sleep
from multiprocessing import Process, Value
from w1thermsensor import W1ThermSensor
from subprocess import check_output
from datadog import initialize, api
from uptime import uptime

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

page_views = 0

def read_temp():
    temperature = sensor.get_temperature(W1ThermSensor.DEGREES_F)
    float("{0:.2f}".format(temperature))
    return temperature


def dd_temp_update():
    while True:
        temperature = read_temp()
        print("START: Update DD temperature metric =={}".format(temperature))
        api.Metric.send(metric='jeferaptor.temperature', points=temperature, type='counter', host='Jeferaptor')
        sleep(1)


@app.route("/")
def ismybeercold():
    global page_views
    page_views += 1
    api.Metric.send(metric='jeferaptor.page_views', points=page_views, type='counter', host='Jeferaptor')
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
    page_views = 0
    dd_process = Process(target=dd_temp_update)
    dd_process.start()
    app.run(host='0.0.0.0', port=80, debug=False)
    dd_process.join()
