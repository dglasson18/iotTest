//sketch for a dual ultrasonic distance monitor set up to transmit
//data using LoRa to a receiver.
/*Hardware: Arduino Uno R3
            Dragino LoRa Shield (915MHz)
            HC-SR04 Ultrasonic Distance Sensor x 2
*/
#include <SPI.h>
#include <RH_RF95.h> 
#include "LowPower.h"
#include <dht11.h>
#define DHT11PIN 4

dht11 DHT11;

RH_RF95 rf95;

int processData0(int data);
int processData1(int data);
int processData2(int data);
int processData3(int data);

int iteration = 0;

float frequency = 916.8;
//deviceNumber 001,
uint8_t senSend = '1';
uint8_t devSend = '0';
uint8_t devNum1 = '0';
uint8_t devNum2 = '0';
uint8_t devNum3 = '5';
uint8_t devNum4 = '6';
long duration, cm;
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
  int chk = DHT11.read(DHT11PIN);
  int sensorData;
  if (iteration == 0){
    sensorData = DHT11.temperature;
    toSend[3] = devNum3;
    iteration++;
  }
  else {
    sensorData = DHT11.humidity;
    toSend[3] = devNum4;
    iteration = 0;
  }
    boolean sent = false;
    toSend[0] = senSend;
    toSend[1] = devNum1;
    toSend[2] = devNum2;
    
    toSend[4] = processData0(sensorData);
    toSend[5] = processData1(sensorData);
    toSend[6] = processData2(sensorData);
    toSend[7] = processData3(sensorData);
  
  //  for(int i = 4; i < 7; i++){
    //   toSend[i] = sensorData % 10;  // remainder of division with 10 gets the last digit
      // sensorData /= 10;     // dividing by ten chops off the last digit.
   // }
  
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
  for(int i = 0; i <= 2700; i++){
    //LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
  }
  delay(10000);
}

int processData0(int data){
  int result;
  for (int i = 1000; i <= 7000; i = i + 1000){ //sensor shouldn't return value greater than 5000
    if (data < i){
      result = (i-1000)/1000;
      break;
    }
  }
  return result + 48;
}

int processData1(int data){
  int result;
  data = data % 1000;
  for (int i = 100; i <= 1000; i = i + 100){
    if (data < i){
      result = (i-100)/100;
      break;
    }
  }
  return result + 48;
}

int processData2(int data){
  int result;
  data = data % 100;
  for (int i = 10; i <= 100; i = i + 10){
    if (data < i){
      result = (i-10)/10;
      break;
    }
  }
  return result + 48;
}

int processData3(int data){
  data = data % 10;
  return data + 48;
}
