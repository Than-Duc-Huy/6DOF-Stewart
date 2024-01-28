#include <Wire.h> //Library for I2C
#include <VL53L1X.h> //Library for VL53L1X
#include <SimpleKalmanFilter.h>

/////////////////////////////////// DEFINE
#define Lidarxshut 12 //Xshut start at pin 12
#define numLidar 2 // number of lidar
#define address 0x29 // default address

VL53L1X Lidar[numLidar];  // Array of Lidar
SimpleKalmanFilter Left(2,2,0.01);
SimpleKalmanFilter Right(2,2,0.01);
float estimated_val[2];
void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(400000);
  for(int i = 0; i < numLidar ; i++ ){
    pinMode(Lidarxshut+i,OUTPUT);
    digitalWrite(Lidarxshut+i, LOW); // Shut the Lidar first
    Serial.print("Pin ");
    Serial.print(i);
    Serial.println(" is off");
  }
  Wire.beginTransmission(address);
  Lidarinit();
  Wire.endTransmission();
}

void loop() {
  for(int i = 0; i < numLidar; i++){
    Serial.print("\t");
    Serial.print(Lidar[i].read());
  }
  delay(50);
  Serial.println();
}

void Lidarinit(){
  for(int i = 0; i < numLidar; i++){
    digitalWrite(Lidarxshut+i,HIGH); // Turn on the Lidar
    Serial.print("Pin ");
    Serial.print(i);
    Serial.println(" is on");
    if (!Lidar[i].init()){
      Serial.println(" failed");
    }
    Lidar[i].setAddress(address + i+1);
    Lidar[i].setDistanceMode(VL53L1X::Long);
    Lidar[i].setMeasurementTimingBudget(50000); // in micro sec
    Lidar[i].startContinuous(50); // in milisec
    Lidar[i].setTimeout(100);
  }
}
