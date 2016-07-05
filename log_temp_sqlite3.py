#!/usr/bin/env python
import sqlite3
import thermometer
import datetime

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

if __name__ == '__main__':

    temperature = float(thermometer.read_temp())
    connection = sqlite3.connect("ismybeercold.db")
    cursor = connection.cursor()

    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))
    connection.commit()
    connection.close()
