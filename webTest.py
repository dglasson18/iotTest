def writeTank():
    index = 0
    deviceData = open("iot/deviceData.txt", 'r')
    fileLine = deviceData.readlines()
    tanks = []
    for n in fileLine: #check if user input matches a device in data file
        if n[4:8] == "tank": #final value stored in data should be most up to date
            tanks1 = [[n[0:3], n[4:8], n[9:13]]]
            tanks = tanks + tanks1
            index = index + 1;
    deviceData.close()
    print(tanks)
    sensorData = open("iot/data.txt", 'r')
    fileLine = sensorData.readlines()
    tankFile = open("iot/tankFile.html", 'w')
    tankFile.write('<!DOCTYPE html>\n<html>\n<body><h1><a href="tankFile.html">Tanks </a><a href="irriFile.html"> Irrigation</a></h1>\n')
    for i in tanks:
        dataValue = 0
        print(i)
        dataFound = False
        for n in fileLine:
            print(n)
            if i[0] == n[1:4]:
                print("Data found")
                dataValue = n[4:8]
                dataFound = True
        if dataFound:
            print("writing data")
            tankFile.write('<div class="dataDisplay"><div style="width:50%; height:'+ str(int(dataValue)/int(i[2]) * 300) + 'px; border:1px solid black"></div><div style="width:50%; height:'+ str(3*(100 - int(dataValue)/int(i[2]) * 100)) + 'px; border:1px solid black; background-color: green;"></div>\n<h1>Tank ' + i[0] + ' is at ' + str(100 - int(dataValue)/int(i[2]) * 100)+' %</h1>\n</div>\n')
            
    tankFile.write("</body>\n</html>\n")

writeTank()
        
    
    
            
    