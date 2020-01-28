//sketch for a dual ultrasonic distance monitor set up to transmit
//data using LoRa to a receiver.
/*Hardware: Arduino Uno R3
            Dragino LoRa Shield (915MHz)
            HC-SR04 Ultrasonic Distance Sensor x 2
*/
#include <SPI.h>
#include <RH_RF95.h> 
#include "LowPower.h"

RH_RF95 rf95;

float frequency = 916.8;
//deviceNumber 004,
uint8_t senSend = '1';
uint8_t devSend = '0';
uint8_t devNum1 = '0';
uint8_t devNum2 = '0';
uint8_t devNum3 = '4';

int counter = 0;

uint8_t toSend[] = "00000000";

void setup(){

  delay(5000); 
  
  if (rf95.init() == false){
    while (1);
  }
  // Setup ISM frequency
  rf95.setFrequency(frequency);

   // The default transmitter power is 13dBm, using PA_BOOST.
   // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
   // you can set transmitter powers from 5 to 23 dBm:
   // Transmitter power can range from 14-20dbm.
   rf95.setTxPower(14, false);

}

void loop(){
    if (counter % 2 == 0)
      toSend[7] = '1';
    else
      toSend[7] = '3';
    boolean sent = false;
    toSend[0] = senSend;
    toSend[1] = devNum1;
    toSend[2] = devNum2;
    toSend[3] = devNum3;
    toSend[4] = '0';
    toSend[5] = '1';
    toSend[6] = '2';
  
    while (!sent){
      rf95.send(toSend, sizeof(toSend));
      rf95.waitPacketSent();
      byte buf[RH_RF95_MAX_MESSAGE_LEN];
      byte len = sizeof(buf);
      if (rf95.waitAvailableTimeout(3000)) {
        // Should be a reply message for us now
        if (rf95.recv(buf, &len)) {
          if (buf[0] == 'r' && buf[1] == toSend[1] && buf[2] == toSend[2] && buf[3] == toSend[3] && buf[4] == toSend[4] && buf[5] == toSend[5] && buf[6] == toSend[6] && buf[7] == toSend[7]){//(buf[0] == (byte)'M' && buf[1] == (byte)devNum1 && buf[2] == (byte)devNum2 && buf[3] == (byte)oldSensorState){
            sent=!sent;
          }
        }
        else {
        }
      }
      else {
      }
      delay(5000);
    }
  //Sensors should be checked once an hour
  for(int i = 0; i <= 6; i++){
    LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
  }
  counter++;
}
