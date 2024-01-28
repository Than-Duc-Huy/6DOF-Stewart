

#include <Wire.h> //Library for I2C
#include <VL53L1X.h> //Library for VL53L1X

VL53L1X sensor1; //create instance of sensor1

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(400000); // 400 kHz
  pinMode(2,OUTPUT);
  digitalWrite(2,HIGH);
  
  sensor1.setTimeout(500); //Timeout in 500ms
  if (!sensor1.init()){
    Serial.println("Failed to initialized. Please restart!");
  }

///////////////////////////////////////////// Setting 
  // Long Distance Mode and allowing 50000 us (50 ms) for a measurement

  Serial.println(sensor1.getAddress(),HEX);
//  sensor1.setAddress(0x32);
//  Serial.println("Changed");
//  Serial.println(sensor1.getAddress(),HEX);
  
  sensor1.setDistanceMode(VL53L1X::Long);
  sensor1.setMeasurementTimingBudget(50000); // in micro sec
  sensor1.startContinuous(50); // in milisecond (should be as long as the timing budget)
//  digitalWrite(2,LOW);
  Wire.endTransmission();
}

void loop() {
  Serial.print(sensor1.read());
  if (sensor1.timeoutOccurred()){Serial.print("TIMEOUT");}
  Serial.println();
  Serial.print("0x");
  Serial.println(sensor1.getAddress(),HEX);

}
