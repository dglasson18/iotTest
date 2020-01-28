/*
 * Moisture sensor code taken from example sketch from dfrobot
  # Example code for the moisture sensor
  # Editor     : Lauren
  # Date       : 13.01.2012
  # Version    : 1.0
  # Connect the sensor to the A0(Analog 0) pin on the Arduino board

  # the sensor value description
  # 0  ~300     dry soil
  # 300~700     humid soil
  # 700~950     in water
*/

#include <SPI.h>
#include <RH_RF95.h> 

RH_RF95 rf95;

float frequency = 916.8;

uint8_t senSend = '1';
uint8_t devSend = '0';
//devNum1,2,3 are combined, e.g. 3, 4, 2 results in device number 342
uint8_t devNum1 = '0';
uint8_t devNum2 = '0';
uint8_t devNum3 = '1';
int ledPin = 4;
static uint8_t newSensorState = 0; //sensor is reading a value below 650, it can be assumed there is no water
static uint8_t oldSensorState = '0';
uint8_t toSend[] = "00000000";

void setup(){
  //serial used for debugging, can be removed
  pinMode(ledPin, OUTPUT);

  Serial.begin(9600);

  Serial.println("RFM Client!"); 
  
  Serial.println("Start LoRa Client");
  if (rf95.init() == false){
    Serial.println("Radio Init Failed - Freezing");
    while (1);
  }
  // Setup ISM frequency
  rf95.setFrequency(frequency);
  //while (rf95.init() == false){
    //Serial.println("Failed to initialise radio - freezing");
    //while(1);
  //}
  //else{
    //Flash led twice indicating that radio initialisation has completed
    //digitalWrite(ledPin, HIGH);
    //delay(5000);
  //}

  digitalWrite(ledPin, HIGH);
  delay(500);
  digitalWrite(ledPin, LOW);
  delay(500);
  digitalWrite(ledPin, HIGH);
  delay(500);
  digitalWrite(ledPin, LOW);
  delay(500);

   // The default transmitter power is 13dBm, using PA_BOOST.
   // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
   // you can set transmitter powers from 5 to 23 dBm:
   // Transmitter power can range from 14-20dbm.
   rf95.setTxPower(14, false);

}

void loop(){
  //byte buf[RH_RF95_MAX_MESSAGE_LEN];
  //byte len = sizeof(buf);
  //newSensorState=!newSensorState;
  Serial.print("Moisture Sensor Value:");
  Serial.println(analogRead(A0));

  if (analogRead(A0) > 650 && oldSensorState == '0'){
    oldSensorState = '1';
    newSensorState = 1;
    Serial.println("Sensor has detected water");
  }
  else if (analogRead(A0) < 650 && oldSensorState == '1'){
    oldSensorState = '0';
    Serial.println("Sensor doesn't detect water");
    newSensorState = 1;
  }
  Serial.print("SensorState: ");
  Serial.println(newSensorState);
  
  while ((int)newSensorState != 0){
    digitalWrite(ledPin, HIGH);
    Serial.println("Prepping variables to send");
    toSend[0] = senSend;
    toSend[1] = devNum1;
    toSend[2] = devNum2;
    toSend[3] = devNum3;
    toSend[4] = oldSensorState;
    toSend[5] = oldSensorState;
    toSend[6] = oldSensorState;
    toSend[7] = oldSensorState;
    Serial.println("Variables prepped, ready to send message");
    
    rf95.send(toSend, sizeof(toSend));
    rf95.waitPacketSent();
    Serial.println("Sending message");
    Serial.println((char*)toSend);
    byte buf[RH_RF95_MAX_MESSAGE_LEN];
    byte len = sizeof(buf);
    if (rf95.waitAvailableTimeout(3000)) {
      // Should be a reply message for us now
      if (rf95.recv(buf, &len)) {
        Serial.print("Got reply that reads");
        Serial.print((char*)buf);
        if (buf[0] == toSend[0] && buf[1] == toSend[1] && buf[2] == toSend[2] && buf[3] == toSend[3] && buf[4] == toSend[4] && buf[5] == toSend[5] && buf[6] == toSend[6] && buf[7] == toSend[7]){//(buf[0] == (byte)'M' && buf[1] == (byte)devNum1 && buf[2] == (byte)devNum2 && buf[3] == (byte)oldSensorState){
          Serial.println("Acknowledged");
          Serial.println((char*)buf);
          newSensorState = 0;
          digitalWrite(ledPin, LOW);
        }
      }
      else {
        Serial.println("Receive failed or message received from another device");
      }
    }
    else {
      Serial.println("No reply, is the receiver running?");
    }
    delay(5000);
  }

  
  delay(10000);

}
