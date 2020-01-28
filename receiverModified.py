#------------------------------------------------------------#
#Author: Daniel Glasson
#Contact: dglasson18@gmail.com
#lastUpdated: 28/01/20 - requires testing

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

htmlMenuText = '<!DOCTYPE html>\n<html>\n<body><h1><a href ="tankFile.html"><Tanks </a><a href="irriFile.html"> Irrigation</a><a href="tempFile.html"> Temperature</a></h1>\n'
htmlTankText = ""
htmlIrriText = ""
htmlTempText = ""
htmlHumiText = ""
serialDir = '/dev/ttyUSB0'

# Turn off GPIO warnings
GPIO.setwarnings(False)
time
oneZeroValues = [0*x for x in range(500)]#list stores previous values of data from devices
previousDataList = ['00000000' for x in range(500)]#list stores previous values of data from more analog style sensors
managedDevices = []
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
        print("Device not found in device list")
        print(type(getDevData(data)))
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
    devDataFile = open("iot/deviceData.txt", "r")
    fileLine = devDataFile.readlines()
    for n in fileLine:
        if data[1:4] == n[0:3]:#device found
            devData[0] = n[0:3] #devNum
            devData[1] = n[4:8] #devType
            devData[2] = n[9:13] #val1
            devData[3] = n[14:18] #val2
            devData[4] = n[19:23] #val3
            devDataFile.close()
            return devData
    devDataFile.close()
    return False

#go through list of devices, storing each device in managedDevices variable
def checkPotentialDevices():
    global managedDevices
    print("Checking Potential Devices")
    devData = ["numb", "type", "val1", "val2", "val3"]
    devDataFile = open("iot/deviceData.txt", "r")
    fileLine = devDataFile.readlines()
    for n in fileLine: 
        managedDevices.append(n[0:8])
    print(managedDevices)
    devDataFile.close()
#should be run after checkPotentialDevices
def createMenuText():
    print("createMenuText")
    global htmlTankText
    global htmlIrriText
    global htmlTempText
    global htmlHumiText
    global htmlMenuText
    global managedDevices
    tank = False
    irri = False
    temp = False
    for n in managedDevices:
        print("going through devices whilst creating menu")
        print(str(n[4:8]))
        if n[4:8] == 'tank':
            tank = True
            htmlTankText = htmlTankText + '<a href="tankFile'+str(n[0:3])+'.html">Tank '+str(n[0:3])+'</a>'
        elif n[4:8] == 'irri':
            irri = True
            print("irri found")
            htmlIrriText = htmlIrriText + '<a href="irriFile'+str(n[0:3])+'.html">Irri '+str(n[0:3])+'</a>'
        elif n[4:8] == 'temp':
            temp = True
            htmlTempText = htmlTempText + '<a href="tempFile'+str(n[0:3])+'.html">Temp '+str(n[0:3])+'</a>'
        elif n[4:8] == 'humi':
            humi = True
            htmlHumiText = htmlHumiText + '<a href="tempFile'+str(n[0:3])+'.html">Temp '+str(n[0:3])+'</a>'
    htmlMenuText = ''
    if tank:
        htmlMenuText = htmlMenuText + '<div class = "dropdown">\n<button class="dropbtn">Tank<i class="fa fa-caret-down"></i></button>\n<div class="dropdown-content">\n'+htmlTankText+'</div></div>'
    if irri:
        print("Adding irri")
        htmlMenuText = htmlMenuText + '<div class = "dropdown">\n<button class="dropbtn">Irri<i class="fa fa-caret-down"></i></button>\n<div class="dropdown-content">\n'+htmlIrriText+'</div></div>'
    if temp:
        htmlMenuText = htmlMenuText + '<div class = "dropdown">\n<button class="dropbtn">Temp<i class="fa fa-caret-down"></i></button>\n<div class="dropdown-content">\n'+htmlTempText+'</div></div>'
    if humi:
        htmlMenuText = htmlMenuText + '<div class ="dropdown">\n<button class="dropbtn">Humi<i class="fa fa-caret-down"></i></button>\n<div class="dropdown-content">\n'+htmlHumiText+'</div></div>'
    htmlMenuText = htmlMenuText + '\n</div></div>'

def writeData(data):#write data to log file data.txt
    dataFile = open('iot/data.txt', 'a') # opens file for data to be written to
    time = datetime.datetime.now()
    dataFile.write(str(data[0:8])+ " " + str(time) + "\n")
    dataFile.close()

def writeTank(data, devData):
    global htmlMenuText
    tankFile = open("/var/www/html/tankFile"+str(data[1:4])+".html", 'w')
    htmlTop = open('iot/Top.html', 'r')
    htmlBottom = open('iot/Bottom.html', 'r')
    tankFile.write(htmlTop.read() + htmlMenuText)
    print(str(int(data[4:8])))
    tankFile.write('<div class="dataDisplay"><div style="width:50%; height:'+ str(int(data[4:8])/int(devData[2]) * 300) + 'px; border:1px solid black"></div><div style="width:50%; height:'+ str(3*(100 - int(data[4:8])/int(devData[2]) * 100)) + 'px; border:1px solid black; background-color: green;"></div>\n<h1>Tank ' + devData[0] + ' is at ' + str(100 - int(data[4:8])/int(devData[2]) * 100)+' %</h1>\n</div>\n')
    tankFile.write(htmlBottom.read())
    tankFile.close()
    htmlTop.close()
    htmlBottom.close()

def writeIrri(data, devData):
    global htmlMenuText
    irriFile = open("/var/www/html/irriFile"+str(data[1:4])+".html", "w")
    htmlTop = open('iot/Top.html', 'r')
    htmlBottom = open('iot/Bottom.html', 'r')
    irriFile.write(htmlTop.read() + htmlMenuText)
    print(data[8])
    print(type(data[8]))
    if data[7] == '1':
        irriFile.write("<p>Water has reached Sensor</p>")
    else:
        irriFile.write("<p>Water has not reached sensor</p>")
    irriFile.write(htmlBottom.read())
    irriFile.close()
    htmlTop.close()
    htmlBottom.close()

def writeTemp(data, devData):
    global htmlMenuText
    tempFile = open("/var/www/html/tempFile" + str(data[1:4]) +".html", "w")
    htmlTop = open('iot/Top.html', 'r')
    htmlBottom = open('iot/Bottom.html', 'r')
    tempFile.write(htmlTop.read() + htmlMenuText)
    tempFile.write("<p>Temperature: " + data[5:8] + "degrees celcius</p>")
    tempFile.write(htmlBottom.read())
    tempFile.close()
    htmlTop.close()
    htmlBottom.close()

def writeHumi(data, devData):
    global htmlMenuText
    humiFile = open("/var/www/html/tempFile" + str(data[1:4]) +".html", "w")
    htmlTop = open('iot/Top.html', 'r')
    htmlBottom = open('iot/Bottom.html', 'r')
    humiFile.write(htmlTop.read() + htmlMenuText)
    humiFile.write("<p>Humidity: " + data[5:8] + "%</p>")
    humiFile.write(htmlBottom.read())
    humiFile.close()
    htmlTop.close()
    htmlBottom.close()

def writeIndex():
    global htmlMenuText
    htmlTop = open('iot/Top.html', 'r')
    htmlBottom = open('iot/Bottom.html', 'r')
    indexFile = open("/var/www/html/index.html", "w")
    indexFile.write(htmlTop.read() + htmlMenuText + htmlBottom.read())
    indexFile.close()
    htmlTop.close()
    htmlBottom.close()

def processSerial(data):
    global oneZeroValues
    global analogValues
    global previousDataList
    if validateData(data):
        devData = getDevData(data)
        prevData = previousDataList[int(data[1:4])]
        if prevData != data[0:8]: # value must have changed, updates need to occur
            writeData(data)
            print("Value updated")
            previousDataList[int(data[1:4])] = data[0:8]
            if devData[1] == 'tank':
                writeTank(data, devData)
            elif devData[1] == "irri":
                writeIrri(data, devData)
                r=requests.post('https://maker.ifttt.com/trigger/binaryChange/with/key/jb2RMajdLlIxlszEeEsbqudfU6m_QWbGzghrDpaFQNc', params={"value1":str(data[0:4]), "value2":"No Water", "value3":"Water"})
            elif devData[1] == "temp":
                writeTemp(data, devData)
            elif devData[1] == "humi":
                writeHumi(data, devData)


try:
    print("    Ready")
    flag = 0
    checkPotentialDevices()
    createMenuText()
    writeIndex()
    while flag==0:
        try:
            ser = serial.Serial(serialDir, 9600) #define serial port for communication with arduino
            print("Serial set up")
            curData = ser.readline() #reads data till /n from arduino (Serial.println(data))
            print("data read")
        except KeyboardInterrupt:
            print ("    Quit")
            flag = 1
        except OSError:
            print("An error occurred while attempting to read data from arduino")
        else:
            decoded = curData.decode() #changes data type from bytes to string, easier for me to manipulate
            print("data decoded, ready to be processed")
            processSerial(decoded) #call process serial function and pass the decoded data from arduino as argument
except KeyboardInterrupt:
    print("    Quit")

    # Reset GPIO settings
    GPIO.cleanup()
