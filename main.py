import time
import os
from bme280 import getTemp, getHumid, getPress

CSV_FILENAME = 'envLog.csv'
JAVASCRIPT_FILENAME = 'web/home.js'

#Return current time and date
def getNow():
    return time.strftime("%d/%m/%Y %H:%M")

#Return current room being measured
def getRoom():
    return "Bedroom1"

#Update environment log
def updateLog():
    data = getNow() + ", " + getRoom() + ", " + getTemp() + ", " + getHumid() + ", " + getPress()
    writeToFile(CSV_FILENAME, data, "a")

#A method to update aws
def updateAWS():
    writeToFile(JAVASCRIPT_FILENAME, 'document.getElementById("currentTemp").innerHTML = "' + getTemp() +'";', "w")
    writeToFile(JAVASCRIPT_FILENAME, 'document.getElementById("currentHumid").innerHTML = "' + getHumid()[:5] +'";', "a")
    writeToFile(JAVASCRIPT_FILENAME, 'document.getElementById("currentPress").innerHTML = "' + getPress()[:6] +'";', "a")
    writeToFile(JAVASCRIPT_FILENAME, 'document.getElementById("currentTime").innerHTML = "' + getNow() +'";', "a")
    os.system("aws s3 cp web/home.js s3://andyshoose/home.js --acl public-read")

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