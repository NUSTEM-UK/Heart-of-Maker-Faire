#include <Ticker.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>


const char* ssid = "nustem";
const char* password = "nustem123";

Ticker flipper;

//  VARIABLES
int blinkPin = BUILTIN_LED;                // pin to blink led at each beat

// these variables are volatile because they are used during the interrupt service routine!
volatile int BPM;                   // used to hold the pulse rate
volatile int Signal;                // holds the incoming raw data
volatile int IBI = 600;             // holds the time between beats, must be seeded!
volatile boolean Pulse = false;     // true when pulse wave is high, false when it's low
volatile boolean QS = false;        // becomes true when Arduoino finds a beat.


void setup() {
  pinMode(BUILTIN_LED, OUTPUT);        // pin that will blink to your heartbeat!
  Serial.begin(115200);             // we agree to talk fast!
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  interruptSetup();                 // sets up to read Pulse Sensor signal every 2mS
  // UN-COMMENT THE NEXT LINE IF YOU ARE POWERING The Pulse Sensor AT LOW VOLTAGE,
  // AND APPLY THAT VOLTAGE TO THE A-REF PIN
  //analogReference(EXTERNAL);
}



void loop() {
  if (QS == true) {                      // Quantified Self flag is true when arduino finds a heartbeat
    Serial.print("Your BPM is:");
    Serial.println(BPM);
    QS = false;                      // reset the Quantified Self flag for next time
  }


  delay(20);                             //  take a break
}




void sendDataToProcessing(char symbol, int data ) {
  Serial.print(symbol);                // symbol prefix tells Processing what type of data is coming
  Serial.println(data);                // the data to send culminating in a carriage return
}







