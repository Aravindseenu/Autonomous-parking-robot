
/******************Autonomous parking code ********************/
/********************coded by Aravind AK***********************/
/****supported by Rahul_R Jaswanth_I ID_Samueal Gautam_Raj*****/


#include <Servo.h>
// motor controls
int Forward = 2;  // Arduino PWM output pin 5; connect to IBT-2 pin 1 (RPWM)
int Backward = 3; // Arduino PWM output pin 6; connect to IBT-2 pin 2 (LPWM)
//steering servo 
Servo steer;
char command; 
#include <Ultrasonic.h>
Ultrasonic ultrasonic2(5, 4),ultrasonic1(7, 6),ultrasonic3(10, 11),ultrasonic4(12, 13);
//connect the sensors as per the pins defined or define it accordingly
  long front_sensor       = ultrasonic1.read();
  long right_front_sensor = ultrasonic2.read();
  long right_back_sensor  = ultrasonic3.read();
  long back_sensor        = ultrasonic4.read();
#define width 20    // Width of the car (cm)
#define length_l 40 // length of the car (cm)
int previous_state = 0;
int datafromNvidia=0;
void setup() {
  Serial.begin(9600);
  steer.attach(9);    // attaches the servo on pin 9 to the servo object
  steer.write(77);
}

void loop() {
 if (Serial.available()>0)
  {
    datafromNvidia=Serial.read();



if((right_front_sensor <= width)&&(previous_state == 0)&&(datafromNvidia == 'F'))
   {
   forward();
    previous_state = 1; 
   }
if ((right_back_sensor <= width)&&(previous_state == 1))
    {
    forward();
    previous_state = 2; 
    }
if((right_front_sensor <= width)&&(previous_state == 2))
   {
    forward();
    previous_state = 3; 
   }
if ((right_back_sensor <= width)&&(previous_state == 3))
    {
    Stop();
    previous_state = 4; 
    delay(1500);
    straight_park();    
    }
if((datafromNvidia == 'L'))
   {
    left();
    previous_state = 0; 
   }
 if((datafromNvidia == 'R'))
   {
    right();
    previous_state = 0; 
   }
}
}


void forward()
{
steer.write(77); 
analogWrite(Backward, 0);
analogWrite(Forward, 27);

//Serial.println("Forward");
}

void Stop()
{
 steer.write(77); 
 analogWrite(Forward, 0);
analogWrite(Backward, 0);
}

  void right()
  {
    steer.write(120);
    analogWrite(Backward, 0);
    analogWrite(Forward,25);
  
    //Serial.println("forward");
    

    }

    void left()
  {
    steer.write(40);
    analogWrite(Backward, 0);
    analogWrite(Forward, 25);
    }


void straight_park()
{
  if((back_sensor >5)&&(front_sensor >5))
    {
    steer.write(77);
    delay(1100);
    analogWrite(Backward, 30);
    delay(700);
    analogWrite(Backward, 0);
    steer.write(120);
    delay(1100);
    analogWrite(Backward, 30);
    delay(700);
    analogWrite(Backward, 0);
    
    steer.write(40);
    delay(1000);
    analogWrite(Forward, 35);
    delay(1000);
    analogWrite(Forward, 0);
    
    steer.write(120);
    delay(1000);
    analogWrite(Backward, 30);
    delay(1000);
    analogWrite(Backward, 0);
    steer.write(80);

     steer.write(40);
    delay(1000);
    analogWrite(Forward, 35);
    delay(900);
    analogWrite(Forward, 0);

     steer.write(120);
    delay(1000);
    analogWrite(Backward, 30);
    delay(1300);
    
    analogWrite(Backward, 0);
    steer.write(77);
    analogWrite(Backward, 30);
    delay(600);
    analogWrite(Backward, 0);
    
    if((right_front_sensor <= 10)&&(right_front_sensor > 5))
    {Serial.println("parked successfully");}   

}
}
