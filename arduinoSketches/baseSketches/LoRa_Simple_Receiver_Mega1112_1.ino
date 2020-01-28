#include <SPI.h>

//Radio Head Library:
#include <RH_RF95.h> 

// We need to provide the RFM95 module's chip select and interrupt pins to the
// rf95 instance below.On the SparkFun ProRF those pins are 12 and 6 respectively.
RH_RF95 rf95;

int LED = 13; //Status LED is on pin 13

int packetCounter = 0; //Counts the number of packets sent
long timeSinceLastPacket = 0; //Tracks the time stamp of last packet received

uint8_t senSent = '1';
uint8_t devSent = '0';

// The broadcast frequency is set to 921.2, but the SADM21 ProRf operates
// anywhere in the range of 902-928MHz in the Americas.
// Europe operates in the frequencies 863-870, center frequency at 868MHz.
// This works but it is unknown how well the radio configures to this frequency:
//float frequency = 915.0; 
float frequency = 916.8; //Broadcast frequency

void setup()
{
  pinMode(LED, OUTPUT);

  Serial.begin(9600);
  // It may be difficult to read Serial messages on startup. The following line
  // will wait for Serial to be ready before continuing. Comment out if not needed.
  //while(!Serial); 
  Serial.println("RFM Client!"); 

  //Initialize the Radio.
  if (rf95.init() == false){
    Serial.println("30010000"); //Radio init failed - freezing
    while (1);
  }
  else{
    //An LED inidicator to let us know radio initialization has completed. 
    Serial.println("20010000"); 
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    delay(500);
  }

  // Set frequency
  rf95.setFrequency(frequency);

   // The default transmitter power is 13dBm, using PA_BOOST.
   // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
   // you can set transmitter powers from 5 to 23 dBm:
   // Transmitter power can range from 14-20dbm.
   rf95.setTxPower(13);

}


void loop()
{
  // Now wait for a reply
  byte buf[RH_RF95_MAX_MESSAGE_LEN];
  byte len = sizeof(buf);

  if (rf95.waitAvailableTimeout(3000)) {
    // Should be a reply message for us now
    if (rf95.recv(buf, &len)) {
      //Serial.print("Got message from device "); Serial.print((char)buf[1]); Serial.println((char)buf[2]);
      //Serial.print("Message reads: ");
      //Serial.println((char*)buf);
      if (buf[0] == senSent){
        //Serial.print("Match to device 1 with message:");
        Serial.println((char*)buf);
        //Serial.println("Sending Message:");
        rf95.send(buf, sizeof(buf));
        rf95.waitPacketSent();
      }//this else can be removed to return it back to what it was earlier
      else{
        //Serial.print("Received unformatted message: ");
        //Serial.println((char*)buf);
        //Serial.println("Sending message back");
        uint8_t toSend[] = "Hello Wrong Message";
        rf95.send(toSend, sizeof(toSend));
        rf95.waitPacketSent();
      }
    }
    else {
      //Serial.println("Receive failed");
    }
  }
  else {
    //Serial.println("No reply, is the receiver running?");
  }
  //Serial.print("RSSI: ");
  //Serial.println(rf95.lastRssi(), DEC);
  delay(5000);
}
