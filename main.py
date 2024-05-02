import time
import os
from bme280 import getTemp, getHumid, getPress
import boto3

SCRIPT_HOME = '/home/pi/Documents/andyshoose/'
CSV_FILENAME = SCRIPT_HOME + 'envLog.csv'
JAVASCRIPT_FILENAME = SCRIPT_HOME + 'web/home.js'

#Return current time and date
def getNow():
    return time.strftime("%d/%m/%Y %H:%M")

#Return current room being measured
def getRoom():
    return "Living Room"

#Update environment log
def updateLog():
    data = getNow() + ", " + getRoom() + ", " + getTemp() + ", " + getHumid() + ", " + getPress()
    writeToFile(CSV_FILENAME, data, "a")

#A method to update aws
def updateAWS():
    s3 = boto3.resource('s3')
    writeToFile(JAVASCRIPT_FILENAME, 'document.getElementById("currentTemp").innerHTML = "' + getTemp() +'";', "w")
    writeToFile(JAVASCRIPT_FILENAME, 'document.getElementById("currentHumid").innerHTML = "' + getHumid()[:5] +'";', "a")
    writeToFile(JAVASCRIPT_FILENAME, 'document.getElementById("currentPress").innerHTML = "' + getPress()[:6] +'";', "a")
    writeToFile(JAVASCRIPT_FILENAME, 'document.getElementById("currentTime").innerHTML = "' + getNow() +'";', "a")
    data = open(JAVASCRIPT_FILENAME, 'rb')
    s3.Bucket('andyshoose').put_object(Key='home.js', Body=data, ACL='public-read')

#Write data to csv files
def writeToFile(file, data, permission):
    f = open(file, permission)
    f.write(data)
    f.write('\n')
    f.close()

#A while loop to control the program
i = 60
while True:
    #After 60 minutes update aws
    if i == 60:
        updateAWS()
        i = 0
    updateLog()
    time.sleep(60) #sleep 60 seconds
    i = i + 1
