/*
  Both the TX and RX ProRF boards will need a wire antenna. We recommend a 3" piece of wire.
  This example is a modified version of the example provided by the Radio Head
  Library which can be found here:
  www.github.com/PaulStoffregen/RadioHeadd
  Low power library used to reduce power draw for battery applications
  https://www.arduinolibraries.info/libraries/arduino-low-power
*/
#include "ArduinoLowPower.h"
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
  toSend[0] = senSend;
  toSend[1] = devNum1;
  toSend[2] = devNum2;
  toSend[3] = devNum3;
  toSend[4] = '0';
  toSend[5] = '0';
  toSend[6] = '0';
  toSend[7] = '0';
  //Send a message to the other radio
  //sprintf(toSend, "Hi, my counter is: %d", packetCounter++);
  rf95.send(toSend, sizeof(toSend));
  rf95.waitPacketSent();

  // Now wait for a reply
  byte buf[RH_RF95_MAX_MESSAGE_LEN];
  byte len = sizeof(buf);
  while(!sent){
    if (rf95.waitAvailableTimeout(2000)) {
      // Should be a reply message for us now
      if (rf95.recv(buf, &len)) {
        if (buf[0] == 'r' && buf[1] == toSend[1] && buf[2] == toSend[2] && buf[3] == toSend[3] && buf[4] == toSend[4] && buf[5] == toSend[5] && buf[6] == toSend[6] && buf[7] == toSend[7]){//(buf[0] == (byte)'M' && buf[1] == (byte)devNum1 && buf[2] == (byte)devNum2 && buf[3] == (byte)oldSensorState){
          sent=!sent;}
        //SerialUSB.print(" RSSI: ");
        //SerialUSB.print(rf95.lastRssi(), DEC);
      }
      else {
      }
    }
    else {
    }
  }
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);

  LowPower.sleep(600000);
}
