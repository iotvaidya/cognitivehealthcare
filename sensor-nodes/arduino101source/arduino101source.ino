#include <CurieBLE.h>
#include <Thread.h>
BLEPeripheral blePeripheral;       // BLE Peripheral Device (the board you're programming)
BLEService heartRateService("180D"); // BLE Heart Rate Service
 boolean bpFlag = true;
// BLE Heart Rate Measurement Characteristic"
//BLECharacteristic heartRateChar("2A39",BLERead | BLENotify, 2);
BLECharacteristic cmdChar("2A41",BLERead | BLEWrite, 2);
BLECharacteristic cmdWriteChar("2A42",BLERead | BLEWrite, 2);

// BLE Temperature Measurement Characteristic"
BLECharacteristic paramChar("2A40",BLERead | BLENotify, 15);

int oldHeartRate = 0;  // last heart rate reading from analog input
long previousMillis = 0;  // last time the heart rate was checked, in ms
int gsrPin = A0;
Thread bpThread = Thread();
Thread gsrThread = Thread();

void setup() {
  Serial.begin(9600);    // initialize serial communication
   Serial1.begin(9600);     // opens serial port, sets data rate to 9600 bps
        while(!Serial1);
  pinMode(13, OUTPUT);   // initialize the LED on pin 13 to indicate when a central is connected
  pinMode(gsrPin,INPUT);

  blePeripheral.setLocalName("IoTVaidya");
  blePeripheral.setAdvertisedServiceUuid(heartRateService.uuid());  // add the service UUID
  blePeripheral.addAttribute(heartRateService);   // Add the BLE Heart Rate service
  blePeripheral.addAttribute(paramChar);
  blePeripheral.addAttribute(cmdChar);
  blePeripheral.addAttribute(cmdWriteChar);
  blePeripheral.begin();
  Serial.println("Bluetooth device active, waiting for connections...");

  bpThread.onRun(BPThreadCallback);
  gsrThread.onRun(GSRThreadCallback);
}

void BPThreadCallback(){
   // send data only when you receive data:
   int incomingByte[100];
   boolean insideFlag = false;
   int i = 1;
   
        if (Serial1.available() && (int)Serial1.read() == 13) {
            incomingByte[0] = 13;
            while(i < 15){
               // read the incoming byte:
                incomingByte[i] = Serial1.read();

                // say what you got:
                Serial.print("I received: ");
                Serial.println(incomingByte[i], DEC);
                i++;
            }
            insideFlag = true;

        }
       
        unsigned char CharArray[15];
        
        while(bpFlag && insideFlag){
         
           for(int i = 0 ; i < 15; i++){
            CharArray[i] = (char)incomingByte[i];
            //CharArray[i] = (char)56;
          //Serial.println(incomingByte[i]);
           //delay(500);
        }
        const unsigned char tempArray[1] = {(char)03};
        cmdWriteChar.setValue(tempArray, 1);
        paramChar.setValue(CharArray, 15);
        
        bpFlag = false;
        bpThread.enabled = false;
       }
        
}

 int temp = 0;
void GSRThreadCallback(){
   // send data only when you receive data:
   int incomingByte[100];
   boolean insideFlag = false;

   for(int i = 0 ; i <  25 ;i++){
    unsigned char CharArray[15];
    for(int j = 0 ; j < 15 ; j++){
       CharArray[j] = (char)analogRead(gsrPin);
       Serial.println(CharArray[j]);
       delay(25);
    }
    paramChar.setValue(CharArray, 15);
    if(i == 24)
      gsrThread.enabled = false;
   }
            
}          

void loop() {
  // listen for BLE peripherals to connect:
  BLECentral central = blePeripheral.central();
  // if a central is connected to peripheral:
   bpFlag = true;
   
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());
    // turn on the LED to indicate the connection:
    digitalWrite(13, HIGH);
  int incomingByte[100];
  int i = 1;
    // check the heart rate measurement every 200ms
    // as long as the central is still connected:
    while (central.connected()) {
            //if(bpThread.shouldRun())
                //bpThread.run();
             //if(gsrThread.shouldRun())
                //gsrThread.run();
                /*if(tempChar.value()){
                  Serial.print("central read: ");
                  Serial.println(*tempChar.value());
                }*/
                //const unsigned char CharArray[2] = { 0, (char)34 };
                //tempChar.setValue(CharArray, 2);
                //const unsigned char heartCharArray[2] = { 0, (char)40 };
                //heartRateChar.setValue(heartCharArray, 2);
                if(cmdChar.written()){
                  Serial.print("Read command :");
                  Serial.println(*cmdChar.value());
                  if(*cmdChar.value() == 1){
                      const unsigned char CharArray[1] = {(char)01};
                      cmdWriteChar.setValue(CharArray, 1);
                      if(gsrThread.shouldRun())
                        gsrThread.run();
                  }else if(*cmdChar.value() == 2){
                     const unsigned char tempArray[1] = {(char)02};
                      cmdWriteChar.setValue(tempArray, 1);
                      if(bpThread.shouldRun())
                        bpThread.run();
                  }
                
               
}
/*
      
      long currentMillis = millis();
      // if 200ms have passed, check the heart rate measurement:
      if (currentMillis - previousMillis >= 200) {
        previousMillis = currentMillis;
        updateHeartRate();
      }
*/
      
    }
    // when the central disconnects, turn off the LED:
    digitalWrite(13, LOW);
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}

void updateHeartRate() {
  /* Read the current voltage level on the A0 analog input pin.
     This is used here to simulate the heart rate's measurement.
  */
  int heartRateMeasurement = analogRead(A0);
  int heartRate = map(heartRateMeasurement, 0, 1023, 0, 100);
  if (heartRate != oldHeartRate) {      // if the heart rate has changed
    Serial.print("Heart Rate is now: "); // print it
    Serial.println(heartRate);
    const unsigned char heartRateCharArray[2] = { 0, (char)heartRate };
    //heartRateChar.setValue(heartRateCharArray, 2);  // and update the heart rate measurement characteristic
    oldHeartRate = heartRate;           // save the level for next comparison
  }
}
