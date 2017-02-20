/*
>> Pulse Sensor Heart of Maker Faire 1.0 <<
This code is for Pulse Sensor Amped by Joel Murphy and Yury Gitman
    www.pulsesensor.com 
With code from Peter through Hackster.io
    https://www.hackster.io/Gengus_Kahn/wireless-heart-monitor-1d748f
*/

#include <Ticker.h>
// The Ticker/flipper routine
Ticker flipper;

//  VARIABLES
int blinkPin = D1;                // pin to blink led at each beat
int fadePin = D2;                 // pin to do fancy classy fading blink at each beat
int fadeRate = 0;                 // used to fade LED on with PWM on fadePin


// these variables are volatile because they are used during the interrupt service routine!
volatile int BPM;                   // used to hold the pulse rate
volatile int Signal;                // holds the incoming raw data
volatile int IBI = 600;             // holds the time between beats, must be seeded! 
volatile boolean Pulse = false;     // true when pulse wave is high, false when it's low
volatile boolean QS = false;        // becomes true when Arduoino finds a beat.


void setup(){
  delay(20);
  pinMode(blinkPin,OUTPUT);         // pin that will blink to your heartbeat!
pinMode(BUILTIN_LED, OUTPUT);
pinMode(fadePin,OUTPUT);          // pin that will fade to your heartbeat!
  Serial.begin(115200);             // we agree to talk fast!
  interruptSetup();                 // sets up to read Pulse Sensor signal every 2mS  
}



void loop(){

  if (QS == true){                       // Quantified Self flag is true when arduino finds a heartbeat
        fadeRate = 255;                  // Set 'fadeRate' Variable to 255 to fade LED with pulse
        sendDataToProcessing('B',BPM);   // send heart rate with a 'B' prefix
        //sendDataToProcessing('Q',IBI);   // send time between beats with a 'Q' prefix
        QS = false;                      // reset the Quantified Self flag for next time    

     }
     
//  ledFadeToBeat();
//  delay(10);                             //  take a break
}


//void ledFadeToBeat(){
//    fadeRate -= 15;                         //  set LED fade value
//    fadeRate = constrain(fadeRate,0,255);   //  keep LED fade value from going into negative numbers!
//    analogWrite(fadePin,fadeRate);          //  fade LED
//  }


void sendDataToProcessing(char symbol, int data ){
    Serial.print(symbol);                // symbol prefix tells Processing what type of data is coming
    Serial.println(data);                // the data to send culminating in a carriage return
  }

