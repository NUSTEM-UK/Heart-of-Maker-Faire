// Based on http://www.instructables.com/id/Wearable-heart-beat-sensor-ESP8266Pulse-sensor/?ALLSTEPS
// Hacked to run via MQTT

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Ticker.h>

Ticker flipper;
Ticker sender;
const int maxAvgSample = 20;
volatile int rate[maxAvgSample];                    // used to hold last ten IBI values
volatile unsigned long sampleCounter = 0;          // used to determine pulse timing
volatile unsigned long lastBeatTime = 0;           // used to find the inter beat interval
volatile int P =512;                      // used to find peak in pulse wave
volatile int T = 512;                     // used to find trough in pulse wave
volatile int thresh = 512;                // used to find instant moment of heart beat
volatile int amp = 100;                   // used to hold amplitude of pulse waveform
volatile boolean firstBeat = true;        // used to seed rate array so we startup with reasonable BPM
volatile boolean secondBeat = true;       // used to seed rate array so we startup with reasonable BPM
volatile int BPM;                   // used to hold the pulse rate
volatile int Signal;                // holds the incoming raw data
volatile int IBI = 600;             // holds the time between beats, the Inter-Beat Interval
volatile boolean Pulse = false;     // true when pulse wave is high, false when it's low
volatile boolean QS = false;

const char* ssid = "nustem";
const char* password = "nustem123";
const char* mqtt_server = "192.168.1.1";

String sendTopicString;
String subsTopicString;
char subsTopicArray[100];
char tempBuffer[60];      // Temp for MQTT publish string/array conversions
char tempBuffer2[60];
String sendPayloadString;

WiFiClient espClient;
PubSubClient client(espClient);

// Each device has a unique name, generated from the hardware MAC address.
// These variables will store those names.
// For historical reasons, we refer to ESP8266-based devices as 'skutters'
String huzzahMACAddress;
String skutterNameString;
char skutterNameArray[60];

void setup() {
    Serial.begin(115200);
    delay(10);
    setup_wifi();

    // hard-code heart number and MQTT send channel
    sendTopicString = "heart/999/setRate";
    //sendTopicString = "heart/998/setRate";
  
    // Get this Huzzah's MAC address and use it to register with the MQTT server
    huzzahMACAddress = WiFi.macAddress();
    skutterNameString = "skutter_" + huzzahMACAddress;
    Serial.println(skutterNameString);
    skutterNameString.toCharArray(skutterNameArray, 60);
    
    flipper.attach_ms(2, Test);
}

void loop() {

    delay(1000);
    sendTopicString.toCharArray(tempBuffer2, 60);
    sendPayloadString = BPM;
    sendPayloadString.toCharArray(tempBuffer, 60);
    client.publish(tempBuffer2, tempBuffer);
    Serial.print("Sent : ");
    Serial.print(tempBuffer2);
    Serial.print(" message: ");
    Serial.println(tempBuffer);
    
    flipper.attach_ms(2, Test);
  
}


int count = 0;
void Test()
{
  count++;
  if(count == 1000)
  {
    flipper.detach();
    count = 0;

  }

  Signal = analogRead(A0);              // read the Pulse Sensor
  sampleCounter += 2;                         // keep track of the time in mS with this variable
  int N = sampleCounter - lastBeatTime;       // monitor the time since the last beat to avoid noise

  if(Signal < thresh && N > (IBI/5)*3){       // avoid dichrotic noise by waiting 3/5 of last IBI
    if (Signal < T){                        // T is the trough
        T = Signal;                         // keep track of lowest point in pulse wave
     }
   }

  if(Signal > thresh && Signal > P){          // thresh condition helps avoid noise
      P = Signal;                             // P is the peak
     }                                        // keep track of highest point in pulse wave

    //  NOW IT'S TIME TO LOOK FOR THE HEART BEAT
    // signal surges up in value every time there is a pulse
  if (N > 250){                                   // avoid high frequency noise
    if ( (Signal > thresh) && (Pulse == false) && (N > (IBI/5)*3) ){
      Pulse = true;                               // set the Pulse flag when we think there is a pulse
      //digitalWrite(blinkPin,HIGH);                // turn on pin 13 LED
      IBI = sampleCounter - lastBeatTime;         // measure time between beats in mS
      lastBeatTime = sampleCounter;               // keep track of time for next pulse
  
           if(firstBeat){                         // if it's the first time we found a beat, if firstBeat == TRUE
               firstBeat = false;                 // clear firstBeat flag
               return;                            // IBI value is unreliable so discard it
              }
           if(secondBeat){                        // if this is the second beat, if secondBeat == TRUE
              secondBeat = false;                 // clear secondBeat flag
                 for(int i=0; i<=maxAvgSample-1; i++){         // seed the running total to get a realisitic BPM at startup
                      rate[i] = IBI;
                      }
              }

    // keep a running total of the last 10 IBI values
    word runningTotal = 0;                   // clear the runningTotal variable

    for(int i=0; i<=(maxAvgSample-2); i++){                // shift data in the rate array
          rate[i] = rate[i+1];              // and drop the oldest IBI value
          runningTotal += rate[i];          // add up the 9 oldest IBI values
        }

    rate[maxAvgSample-1] = IBI;                          // add the latest IBI to the rate array
    runningTotal += rate[maxAvgSample-1];                // add the latest IBI to runningTotal
    runningTotal /= maxAvgSample;                     // average the last 10 IBI values
    BPM = 60000/runningTotal;               // how many beats can fit into a minute? that's BPM!
    QS = true;                              // set Quantified Self flag
    // QS FLAG IS NOT CLEARED INSIDE THIS ISR
    }
}

  if (Signal < thresh && Pulse == true){     // when the values are going down, the beat is over
      //digitalWrite(blinkPin,LOW);            // turn off pin 13 LED
      Pulse = false;                         // reset the Pulse flag so we can do it again
      amp = P - T;                           // get amplitude of the pulse wave
      thresh = amp/2 + T;                    // set thresh at 50% of the amplitude
      P = thresh;                            // reset these for next time
      T = thresh;
     }

  if (N > 2500){                             // if 2.5 seconds go by without a beat
      thresh = 512;                          // set thresh default
      P = 512;                               // set P default
      T = 512;                               // set T default
      lastBeatTime = sampleCounter;          // bring the lastBeatTime up to date
      firstBeat = true;                      // set these to avoid noise
      secondBeat = true;                     // when we get the heartbeat back
     }

  //sei();                                     // enable interrupts when youre done!
}// end isr
