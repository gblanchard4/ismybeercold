#!/usr/bin/python
from flask import Flask, render_template, request, jsonify
import datetime
import psutil
from subprocess import check_output
import thermometer
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)


@app.route("/")
def ismybeercold():
    return render_template('index.html', title="ISMYBEERCOLD?")


@app.route("_jsondata")
def jsondata():
    uptime = getUptime()
    tempString = thermometer.read_temp()
    timeString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cpu_percent = psutil.cpu_percent()
    virtmem_percent = psutil.virtual_memory()[2]
    return jsonify(uptime=uptime, temp=tempString, time=timeString, cpu=cpu_percent, ram=virtmem_percent)


def getUptime():
    output = check_output(["uptime"])
    uptime = output[output.find("up"):output.find("user") - 5]
    return uptime

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(host='0.0.0.0', port=8888, debug=True)
