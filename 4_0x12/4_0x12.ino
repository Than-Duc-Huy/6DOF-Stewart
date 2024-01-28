/**
 * Wait 5s to move all the way down
 * Then type the distance you want
 * 1000 -> 1cm
 * 
 */



#include <TimerOne.h>
#include <Wire.h> // A4 SDA (PC4); A5 SCL (PC5)
#include <stdlib.h>
#define pin_clock 2 //PD2
#define pin_data 3 //PD3
#define pin_zero 4
#define pin_on 5
#define pin_pwm 6
#define pin_dir 7
#define address 12

#define kp 0.5
#define kd 0.5
#define ki 0.0


void motormove(int pwm_sig);  
void zero();
void onoff();
void receiveEvent();
void requestEvent();

void setup() {
  pinMode(2,INPUT_PULLUP);  // CLOCK
  pinMode(3,INPUT_PULLUP);  //DATA
  pinMode(4,OUTPUT); // ON OFF 4 
  digitalWrite(6,0);
  pinMode(5,OUTPUT); // ZERO 5
  digitalWrite(7,0);
  pinMode(7,OUTPUT); //MOTOR_DIR 7
  pinMode(6,OUTPUT); //MOtOR_PWM 6
  
  Wire.begin(address);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

  Serial.begin(115200);
  attachInterrupt(digitalPinToInterrupt(pin_clock),record,FALLING);  // Falling Edge interrupt of Clock Pin

  Serial.println("Setting Up");
  motormove(-255);
  delay(5000);
  zero();
  Serial.println("Done");
}
static int data[24];   // 24 bits
static int sum;   // sum to convert to decimal
static int diff;
unsigned char count = 0;
bool recorded;    // Bit
unsigned long idleness = 0;
int seri=0;
int goal;

static int prev = 0;
static int deltat = 0;
int from_master = 0;
int reset=0;
bool commu=0;
bool valid=0;



// PID
int motorpower = 0;
int current_error = 0;
int prev_error = 0; 
int sum_error = 0;
int diff_error = 0;

void loop() {
  do{
    if (from_master == 255){
      if (reset == 0){
        Serial.println("Zero");
        motormove(-255);
        delay(500);
        zero();
      }
      reset = 1;
      from_master = 0;
    }
      else reset = 0;
    goal = map(from_master,0,254,0,9000);
    current_error = goal-sum;
    diff_error = current_error - prev_error;
    sum_error += ki*current_error;
    motorpower = kp*current_error + kd*diff_error;
    motormove(motorpower);

    prev_error = current_error;
  } while(abs(current_error) > 80);
  motormove(0);
}

void record(){
  recorded = !digitalRead(pin_data);
  deltat = millis()-prev;
  if (commu == 1) valid = 0;

  if(deltat > 70){
    valid = 1;
    count = 0;
    data[count++] = recorded;
    prev = millis();
  }
  else{
    if(valid == 1){
      data[count++] = recorded;
      prev = millis();
      if (count >=23){
        sum = 0;
        for(int i = 0; i < 16;i++){
          sum += data[i]*pow(2,i);
        }
        if (data[20] == 1) sum = -sum;
        Serial.println(sum);
      }
    }
  }
}
void motormove(int pwm_sig){
  if(pwm_sig < 0){
    digitalWrite(pin_dir,0);
  }
  else {
    digitalWrite(pin_dir,1);
  }
  if (abs(pwm_sig) < 50) analogWrite(pin_pwm,0);
  else analogWrite(pin_pwm,max(60,min(abs(pwm_sig),255)));
}

void onoff(){
      digitalWrite(pin_on,1);
      delay(30);
      digitalWrite(pin_on,0);
      delay(10);
}

void zero(){
      digitalWrite(pin_zero,1);
      delay(30);
      digitalWrite(pin_zero,0);
      delay(10);
}


void requestEvent(){
  commu = 1;
  byte response[4];
  for (byte i = 0; i<4;i++){
    response[i] = (byte)((String)sum).charAt(i);
  }
  Wire.write(response, sizeof(response));
  commu = 0;
}

void receiveEvent(){
  commu = 1;
  from_master = Wire.read();
  commu = 0;
}
