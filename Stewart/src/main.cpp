/*
 * Test I2C Master
 * On Master request, display 4 bytes of data from the slave (1234)
 * 
 * Master monitor the 
 * On Master sending, send 4 byte of data 
 * 
 */
#include <Arduino.h>
#include <string.h>
#include <Wire.h>
#include <BluetoothSerial.h>
#define number_motor 6

BluetoothSerial SerialBT;

int motor_address[number_motor];
String slave_response;
byte sending[4];

int desired_joint[number_motor];
int prev_joint[number_motor];
int read_joint[number_motor];

int count;
char *b; // Char array
char *token; // Store token
String a; // Serial String

String readserial;
int data;
byte sent[number_motor];

void setup() {
  pinMode(2,OUTPUT);
  for(int i = 0; i< number_motor;i++){
    motor_address[i] = 8+i;
  }
  Serial.begin(115200);
  SerialBT.begin("Stewart_Platform");
  digitalWrite(2,1);
  Serial.println("On");
  Wire.begin();
  for(int i = 0; i< number_motor;i++){
      desired_joint[i] = 0;
      Wire.beginTransmission(motor_address[i]);
      Wire.write(desired_joint[i]);
      Wire.endTransmission();
  }
}

void loop() {
  if(SerialBT.available() > 0){

    //=============READ DATA
    a = SerialBT.readStringUntil('\n');
    Serial.println(a);
    b = &a[0];
    token = strtok(b,",");
    count = 0;
    while (token != NULL){
      desired_joint[count] = atof(token); // atof is char->float. Store token into Number
      token = strtok(NULL,","); // Move through the token
      count++;
    }
    if (count != 6){
      for(int i = 0;i <number_motor;i++){
        desired_joint[i] = prev_joint[i];
      }
    }
    //=========================================

    // Query, I2C Request
    if (desired_joint[0] == -1){
      for(int i = 0; i < number_motor;i++){
        slave_response ="";
        char c;
        Wire.requestFrom(motor_address[i],4);
        while(Wire.available() != 0){
          c = Wire.read();
          slave_response += c;
        }
        read_joint[i] = slave_response.toInt();
        SerialBT.print(read_joint[i]);
        SerialBT.print("\t");
        Serial.print(read_joint[i]);
        Serial.print("\t");
       }
      Serial.println();
      SerialBT.println();
    }

    // Reset, I2C Send 255  When joint = -2
    else if (desired_joint[0] == -2){
      Serial.println("Zero");
      SerialBT.println("Zero");
      for(int i = 0; i< number_motor;i++){
        Serial.print(desired_joint[i]);
        Serial.print("\t");
        Wire.beginTransmission(motor_address[i]);
        Wire.write((byte)255);
        Wire.endTransmission();
      }
      Serial.println();

    }
    // Move, I2C Send 0-254
    else {
      for(int i = number_motor - 1; i>=0;i--){
        sent[i] = map(desired_joint[i],0,90,0,254);
        Wire.beginTransmission(motor_address[i]);
        Wire.write(sent[i]);
        Wire.endTransmission();
        SerialBT.print(desired_joint[i]);
        SerialBT.print("\t");
      }
      Serial.println();
      SerialBT.println();
    }

    for (int i = 0;i<number_motor;i++){
      prev_joint[i] = desired_joint[i];
    }
  }
}
