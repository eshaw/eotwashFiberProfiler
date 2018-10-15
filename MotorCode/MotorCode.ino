/* 
This is a test sketch for the Adafruit assembled Motor Shield for Arduino v2
It won't work with v1.x motor shields! Only for the v2's with built in PWM
control

For use with the Adafruit Motor Shield v2 
---->	http://www.adafruit.com/products/1438
*/


#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
int firstSensor = 0;    // first analog sensor
int secondSensor = 0;   // second analog sensor
int thirdSensor = 0;    // digital sensor
String inString = 0;         // incoming serial byte
int ctr = 0;
int MoveInt;

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 2);


void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Stepper test!");

  AFMS.begin(3200);  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  myMotor->setSpeed(0.07);  // 10 rpm   

  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
}

void loop() {
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    inString = Serial.readString();
    Serial.println("String Received"+inString);

    //Cast incoming string to an integer
    MoveInt = inString.toInt();
    Serial.println("Int converted from String"+String(MoveInt));
    //Figure out which way to move and then do it
    if(MoveInt < 200 ){
      Serial.println("Moving motor in the positive direction");
      Serial.println(MoveInt);
      myMotor->step(50, BACKWARD, SINGLE);  
    }//else
       /* if(MoveInt < 5 ){
      Serial.println("Moving motor in the negative direction");
      Serial.println(MoveInt);
      myMotor->step(100, FORWARD, SINGLE); 
    }*/
  }
}
  
  //Serial.println("Single coil steps");
  //myMotor->step(1000, FORWARD, SINGLE); 
  //myMotor->step(1000, BACKWARD, SINGLE); 

  //Serial.println("Double coil steps");
  //myMotor->step(100, FORWARD, DOUBLE); 
  //myMotor->step(100, BACKWARD, DOUBLE);
  
  //Serial.println("Interleave coil steps");
  //myMotor->step(100, FORWARD, INTERLEAVE); 
  //myMotor->step(100, BACKWARD, INTERLEAVE); 
  
  //Serial.println("Microstep steps");
  //myMotor->step(50, FORWARD, MICROSTEP); 
  //myMotor->step(50, BACKWARD, MICROSTEP);

