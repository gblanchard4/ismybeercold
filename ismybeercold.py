#!/usr/bin/python
from flask import Flask, render_template, request, jsonify
import datetime
from subprocess import check_output
import thermometer
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)


@app.route("/")
def ismybeercold():
    uptime = getUptime()
    tempString = thermometer.read_temp()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'ISMYBEERCOLD?',
        'time': timeString,
        'temp': tempString,
        'up': uptime
    }
    return render_template('index.html', **templateData)


def getUptime():
    output = check_output(["uptime"])
    uptime = output[output.find("up"):output.find("user") - 5]
    return uptime


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
