#------------------------------------------------------------#
#Author: Daniel Glasson
#Contact: dglasson18@gmail.com
#lastUpdated: 14/12/19
#Limited feature GUI for implementation in conjunction with
#IoT sensors.

#Information regarding sensor/device needs to be stored in 
#file with name 'deviceData.txt' which should itself be stored
#in the same directory as this file is being run from, addresses
#below can of course be modified to suit. See example in repo
#for appropriate formatting

#Data from sensors should be written to a file data.txt, stored
#in same directory this, see data.txt in repo for example formatting
#or receiver.py for example of how data may be written

#User enters device number, most recent data for that device
#is returned and displayed in appropriate form. Not yet
#properly tested, repo will be updated when testing takes place
#------------------------------------------------------------#
from guizero import App, Drawing, Text, TextBox, PushButton

def updateValues():
    deviceFound = False
    file = open("iot/data.txt", "r") #open file containing log from sensors
    fileLine = file.readlines()
    for n in fileLine: #check if user input matches a device in data file
        if str(uInput.value) == n[1:4]: #final value stored in data should be most up to date
            data = n[4:8]
            deviceFound = True
    d.clear() #clears ui for most utd info to be displayed
    file.close()
    if deviceFound:
        deviceFound2=False #device may not exist in file listing devices,
        deviceDataFile = open("iot/deviceData.txt", "r") #file used to store any data required for processing data, such as depth of tank
        deviceData = ["numb", "type", "val1", "val2", "val3"]
        fileLine1 = file.readlines()
        for n in fileLine1:
            if str(uInput.value) == n[0:3]: #if user input matches device number
                deviceData[0] = n[0:3]
                deviceData[1] = n[5:9]
                deviceData[2] = n[11:15]
                deviceData[3] = n[17:21]
                deviceData[4] = n[23:27]
                deviceFound = True #mark device as being found
                break #exit loop, device should only be included in file once, no point repeating loop
        if deviceFound2 == False:
            d.text(500,500, "No data available on how to display device data, add to deviceData.txt and try again", colour="black", size="22")
        elif deviceData[2] == "tank": #specifies a water tank, display appropriately
            displayTank(deviceData, data)
        elif deviceData[2] == "irri": #specificies irrigation system, display appropriately
            displayIrri(deviceData, data)
    else:
        d.text(500,500, "No data received from device specified", colour="black", size="22")

def displayTank(deviceData, data):
    #tank depth is stored in val1, i.e. deviceData[2]
    percentage = (int(data) - deviceData[2]) * 100
    tankMinusPercentage = 100 - percentage
    d.rectangle(150,100,100,tankMinusPercentage, color="green", outline=True)
    d.rectangle(150,tankMinusPercentage,100,0, color="white", outline=True)
    d.text(100,110, deviceData[0], color="black", size="10", max_width=50)
    
def displayIrri(deviceData, data):
    #bay in which the sensor is found stored in val1
    if data == "0000":
        d.text(500, 500, "bay" + str(deviceData[2]) + "has not detected water", color="black", size="30")
    elif data == "1111":
        d.text(500, 500, "bay" + str(deviceData[2]) + "has detected water", color="black", size="30")
    else:
        d.text(500, 500, "Unsure how to display data: " + data, color="black", size="30")

app = App(title="Hello world")
uInput = TextBox(app)
updateText = PushButton(app, command=updateValues, text="update")
d = Drawing(app, width = 1000, height = 1000)
app.display()