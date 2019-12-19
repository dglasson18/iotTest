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
    writing.value=""
    file.close()
    if deviceFound:
        deviceFound2=False #device may not exist in file listing devices,
        deviceDataFile = open("iot/deviceData.txt", "r") #file used to store any data required for processing data, such as depth of tank
        deviceData = ["numb", "type", "val1", "val2", "val3"]
        fileLine1 = deviceDataFile.readlines()
        for n in fileLine1:
            if str(uInput.value) == n[0:3] and deviceFound2 == False: #if user input matches device number
                deviceData[0] = n[0:3]
                deviceData[1] = n[4:8]
                deviceData[2] = n[9:13]
                deviceData[3] = n[14:18]
                deviceData[4] = n[19:23]
                print(deviceData)
                deviceFound2 = True #mark device as being found
                break #exit loop, device should only be included in file once, no point repeating loop
        if deviceFound2 == False:
            print("No data")
            d.text(50, 100, "No data available on how to display device data, add to deviceData.txt and try again", color="black", size="20", max_width=300)
        elif deviceData[1] == "tank": #specifies a water tank, display appropriately
            print("Displaying tank")
            displayTank(deviceData, data)
        elif deviceData[1] == "irri": #specificies irrigation system, display appropriately
            print("Displaying irrigation")
            displayIrri(deviceData, data)
    else:
        print("No data from device")
        d.text(50, 100, "No data received from device specified", color="black", size="20", max_width=300)

def displayTank(deviceData, data):
    #tank depth is stored in val1, i.e. deviceData[2]
    percentage = (int(data)/int(deviceData[2])) * 100
    tankMinusPercentage = 100 - percentage
    d.rectangle(300,200,200,percentage*2, color="green", outline=True)
    d.rectangle(300,percentage*2,200,0, color="white", outline=True)
    d.text(100,110, "Tank " + deviceData[0] + " " +str(tankMinusPercentage)+"%", color="black", size="15", max_width=100)
    
def displayIrri(deviceData, data):
    #bay in which the sensor is found stored in val1
    if data == "0000":
        writing.value="bay " + str(deviceData[2]) + " has not detected water"
    elif data == "1111":
        writing.value="bay " + str(deviceData[2]) + " has detected water"
    else:
        writing.value="Unsure how to display data: " + data

app = App(title="Hello world")
uInput = TextBox(app)
updateText = PushButton(app, command=updateValues, text="update")
writing = Text(app, text="", color="black", size="20")
d = Drawing(app, width = 1000, height = 1000)
app.display()