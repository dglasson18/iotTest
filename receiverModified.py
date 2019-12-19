#------------------------------------------------------------#
#Author: Daniel Glasson
#Contact: dglasson18@gmail.com
#lastUpdated: 19/12/19 - requires testing

#Basic implementation of script to receive data from serial
#of an arduino, acting as a LoRa receiver.

#Data is written to a file data.txt, see example in repo,
#And depending on the data push notifications may also
#be sent to user through utilisation of IFTTT and Pushbullet,
#will add reference material for this later

#Intended to be used in conjunction with guiTest.py for
#automation of basic tasks such as irrigation monitoring

#Reference List
#Lists - https://www.programiz.com/python-programming/list
#Data types - https://realpython.com/python-data-types/
#------------------------------------------------------------#
# Imports
import RPi.GPIO as GPIO
import time
import requests
import datetime
import serial

# Set the GPIO naming convention
GPIO.setmode(GPIO.BCM)

# Turn off GPIO warnings
GPIO.setwarnings(False)
time
oneZeroValues = [0*x for x in range(500)]#list stores previous values of data from devices
previousDataList = ['00000000' for x in range(500)]#list stores previous values of data from more analog style sensors
def validateData(data):
    if len(data) != 10 or data[0] != '1': #Data received not formatted correctly, write
        #to error log with poor data and timestamp.
        print(data)
        print(len(data))
        errorLog = open('iot/errorLog.txt', 'a')
        time = datetime.datetime.now() #get time for use as timestamp
        errorLog.write(str(data) + " " + str(time) + "\n") #write poorly formatted data with timestap to file
        #send post request to IFTTT service to trigger notification
        r = requests.post('https://maker.ifttt.com/trigger/dataError/with/key/jb2RMajdLlIxlszEeEsbqudfU6m_QWbGzghrDpaFQNc', params={"value1":"none","value2":"none","value3":"none"})
        errorLog.close() #close error file
        return False
    elif type(getDevData(data)) is bool:
        errorLog = open('iot/errorLog.txt', 'a')
        time = datetime.datetime.now() #get time for use as timestamp
        errorLog.write(str(data) + " " + str(time) + "\n") #write poorly formatted data with timestap to file
        #send post request to IFTTT service to trigger notification
        r = requests.post('https://maker.ifttt.com/trigger/dataError/with/key/jb2RMajdLlIxlszEeEsbqudfU6m_QWbGzghrDpaFQNc', params={"value1":"none","value2":"none","value3":"none"})
        errorLog.close() #close error file
        return False
    return True

def getDevData(data):
    devData = ["numb", "type", "val1", "val2", "val3"]
    devDataFile = open("iot/data.txt", "r")
    fileLine = devDataFile.readlines()
    for n in fileLine:
        if data[1:4] == n[0:3]:#device found
            deviceData[0] = n[0:3] #devNum
            deviceData[1] = n[4:8] #devType
            deviceData[2] = n[9:13] #val1
            deviceData[3] = n[14:18] #val2
            deviceData[4] = n[19:23] #val3
            devDataFile.close()
            return deviceData
    devDataFile.close()
    return False

def writeData(data):
    dataFile = open('iot/data.txt', 'a') # opens file for data to be written to
    time = datetime.datetime.now()
    dataFile.write(str(data[0:8])+ " " + str(time) + "\n")
    dataFile.close()

def writeTank(data, devData):
    tankFile = open("iot/tankFile.html", 'w')
    tankFile.write('<!DOCTYPE html>\n<html>\n<body><h1><a href="tankFile.html">Tanks </a><a href="irriFile.html"> Irrigation</a></h1>\n')
    tankFile.write('<div class="dataDisplay"><div style="width:50%; height:'+ str(int(data[4:8])/int(devData[2]) * 300) + 'px; border:1px solid black"></div><div style="width:50%; height:'+ str(3*(100 - int(data[4:8])/int(devData[2]) * 100)) + 'px; border:1px solid black; background-color: green;"></div>\n<h1>Tank ' + devData[0] + ' is at ' + str(100 - int(data[4:8])/int(devData[2]) * 100)+' %</h1>\n</div>\n')
    tankFile.write("</body>\n</html>\n")
    tankFile.close()

def writeIrri(data, devData)
    irriFile = open("iot/irriFile.html", "w")
    irriFile.write('<!DOCTYPE html>\n<html>\n<body><h1><a href="tankFile.html">Tanks </a><a href="irriFile.html"> Irrigation</a></h1>\n')
    irriFile.write("</body>\n</html>\n")
    irriFile.close()

def processSerial(data):
    global oneZeroValues
    global analogValues
    global previousDataList
    if validateData(data):
        devData = getDevData(data)
        prevData = previousDataList[int(data[1:4])]
        if prevData != data[0:8]: # value must have changed, updates need to occur
            writeData(data)
            if devData[1] == 'tank':
                writeTank(data, devData)
            elif devData[1] == "irri"
                writeIrri(data, devData)


try:
    print("    Ready")
    flag = 0
    while flag==0:
        try:
            ser = serial.Serial('/dev/ttyACM0', 9600) #define serial port for communication with arduino
            print("Serial set up")
            curData = ser.readline() #reads data till /n from arduino (Serial.println(data))
            print("data read")
        except:
            print("an error ocurred reading data from arduino")
        else:
            decoded = curData.decode() #changes data type from bytes to string, easier for me to manipulate
            print("data decoded, ready to be processed")
            processSerial(decoded) #call process serial function and pass the decoded data from arduino as argument
except KeyboardInterrupt:
    print("    Quit")

    # Reset GPIO settings
    GPIO.cleanup()
