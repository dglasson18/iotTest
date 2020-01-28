#include <ArduinoLowPower.h>



/*
  Both the TX and RX ProRF boards will need a wire antenna. We recommend a 3" piece of wire.
  This example is a modified version of the example provided by the Radio Head
  Library which can be found here:
  www.github.com/PaulStoffregen/RadioHeadd
  Low power library used to reduce power draw for battery applications
  https://www.arduinolibraries.info/libraries/arduino-low-power
*/
#include <SPI.h>

//Radio Head Library:
#include <RH_RF95.h> 

// We need to provide the RFM95 module's chip select and interrupt pins to the
// rf95 instance below.On the SparkFun ProRF those pins are 12 and 6 respectively.
RH_RF95 rf95(12, 6);

int LED = 13; //Status LED is on pin 13

uint8_t senSend = '1';
uint8_t devSend = '0';
uint8_t devNum1 = '0';
uint8_t devNum2 = '0';
uint8_t devNum3 = '3';
uint8_t toSend[] = "00000000";

int packetCounter = 0; //Counts the number of packets sent
long timeSinceLastPacket = 0; //Tracks the time stamp of last packet received

static uint8_t newSensorState = 0; //sensor is reading a value below 650, it can be assumed there is no water
static uint8_t oldSensorState = '1';

// The broadcast frequency is set to 921.2, but the SADM21 ProRf operates
// anywhere in the range of 902-928MHz in the Americas.
// Europe operates in the frequencies 863-870, center frequency at 868MHz.
// This works but it is unknown how well the radio configures to this frequency:
//float frequency = 864.1; 
float frequency = 916.8; //Broadcast frequency

void setup()
{
  pinMode(LED, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  //Initialize the Radio.
  while (rf95.init() == false){
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    delay(500);
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    delay(500);
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    delay(2000);
  }
    //An LED inidicator to let us know radio initialization has completed. 
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    delay(500);

  // Set frequency
  rf95.setFrequency(frequency);

   // The default transmitter power is 13dBm, using PA_BOOST.
   // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
   // you can set transmitter powers from 5 to 23 dBm:
   // Transmitter power can range from 14-20dbm.
   rf95.setTxPower(14, false);
}


void loop()
{
  boolean sent = false;
  //byte buf[RH_RF95_MAX_MESSAGE_LEN];
  //byte len = sizeof(buf);
  //newSensorState=!newSensorState;
  SerialUSB.print("Moisture Sensor Value:");
  SerialUSB.println(analogRead(A0));

  if (analogRead(A0) > 650 && oldSensorState == '0'){
    oldSensorState = '1';
    newSensorState = 1;
    SerialUSB.println("Sensor has detected water");
  }
  else if (analogRead(A0) < 650 && oldSensorState == '1'){
    oldSensorState = '0';
    SerialUSB.println("Sensor doesn't detect water");
    newSensorState = 1;
  }
  SerialUSB.print("SensorState: ");
  SerialUSB.println(newSensorState);
  
  while ((int)newSensorState != 0){
    SerialUSB.println("Prepping variables to send");
    toSend[0] = senSend;
    toSend[1] = devNum1;
    toSend[2] = devNum2;
    toSend[3] = devNum3;
    toSend[4] = oldSensorState;
    toSend[5] = oldSensorState;
    toSend[6] = oldSensorState;
    toSend[7] = oldSensorState;
    SerialUSB.println("Variables prepped, ready to send message");
    
    rf95.send(toSend, sizeof(toSend));
    rf95.waitPacketSent();
    SerialUSB.println("Sending message");
    SerialUSB.println((char*)toSend);
    byte buf[RH_RF95_MAX_MESSAGE_LEN];
    byte len = sizeof(buf);
    while(!sent){
      if (rf95.waitAvailableTimeout(3000)) {
        // Should be a reply message for us now
        if (rf95.recv(buf, &len)) {
          SerialUSB.print("Got reply that reads");
          SerialUSB.print((char*)buf);
          if (buf[0] == 'r' && buf[1] == toSend[1] && buf[2] == toSend[2] && buf[3] == toSend[3] && buf[4] == toSend[4] && buf[5] == toSend[5] && buf[6] == toSend[6] && buf[7] == toSend[7]){//(buf[0] == (byte)'M' && buf[1] == (byte)devNum1 && buf[2] == (byte)devNum2 && buf[3] == (byte)oldSensorState){
            SerialUSB.println("Acknowledged");
            SerialUSB.println((char*)buf);
            newSensorState = 0;
            sent = true;
          }
        }
        else {
          SerialUSB.println("Receive failed or message received from another device");
        }
      }
      else {
        SerialUSB.println("No reply, is the receiver running?");
      }
    }
    delay(5000);
  }
  //delay(10000);
  LowPower.sleep(600000);
}
