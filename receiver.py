#------------------------------------------------------------#
#Author: Daniel Glasson
#Contact: dglasson18@gmail.com
#lastUpdated: 14/12/19

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
analogValues = ['00000000' for x in range(500)]#list stores previous values of data from more analog style sensors
def processSerial(data):
    global oneZeroValues
    global analogValues
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
        return '40010000' #error code, nothing done with as of 12/12/2019, need to write up file for referencing error codes
    elif int(data[1]) >= 5:# identifies sensor that only utilises 1's and 0's
        #check to see whether new value is different to a previously received value
        #extract data bytes 2,3,4 (devId), use it to access relevant value in list
        prevData = oneZeroValues[int(data[1:4])]
        #data is stored in of size 500, where each object in list is relative to a different device. Device number determines position of data in list
        if prevData != data[0:8]: # value must have changed, updates need to occur
            #Break up into different device classes, 500 - 520 represent water sensors,
            #Message 1111 means sensor has detected presence of water, we don't need to notify user if no water is detected
            if int(data[1:4]) >= 500 and int(data[1:4]) <= 520:
                if data[4:8] == '1111':# Water detected notify user
                     r = requests.post('https://maker.ifttt.com/trigger/binaryChange/with/key/jb2RMajdLlIxlszEeEsbqudfU6m_QWbGzghrDpaFQNc', params={"value1":str(data[0:4]),"value2":"No Water","value3":"Water"})
            oneZeroValues[int(data[1:4])-500] = data[0:8] # ensures that data is truncated
            #r = requests.post('https://maker.ifttt.com/trigger/binaryChange/with/key/jb2RMajdLlIxlszEeEsbqudfU6m_QWbGzghrDpaFQNc', params={"value1":str(data[0:4]),"value2":str(int(not(data[7]))),"value3":str(data[7])})
            dataFile = open('iot/data.txt', 'a') # opens file for data to be written to
            time = datetime.datetime.now()
            dataFile.write(str(data[0:8])+ " " + str(time) + "\n")
            dataFile.close()
    elif int(data[1]) >= 0:# identifies sensor as sending data that is of analog form
        prevData = analogValues[int(data[1:4])][0:8]
        if prevData != data[0:8]:
            #Need to figure out a decent way to know when user needs to be notified for each type of device
            #r = requests.post('https://maker.ifttt.com/trigger/analogChange/with/key/jb2RMajdLlIxlszEeEsbqudfU6m_QWbGzghrDpaFQNc', params={"value1":str(data[0:4]),"value2":str(analogValues[int(data[1:4])][4:8]),"value3":str(data[4:8])})
            dataFile = open('iot/data.txt', 'a')
            time = datetime.datetime.now()
            dataFile.write(str(data[0:8])+ " " + str(time) + "\n")
            dataFile.close()
            analogValues[int(data[1:4])] = data[0:8]

try:
    print("    Ready")
    flag = 0
    while flag==0:
        ser = serial.Serial('/dev/ttyACM0', 9600) #define serial port for communication with arduino
        print("Serial set up")
        curData = ser.readline() #reads data till /n from arduino (Serial.println(data))
        print("data read")
        decoded = curData.decode() #changes data type from bytes to string, easier for me to manipulate
        print("data decoded, ready to be processed")
        processSerial(decoded) #call process serial function and pass the decoded data from arduino as argument
except KeyboardInterrupt:
    print("    Quit")

    # Reset GPIO settings
    GPIO.cleanup()