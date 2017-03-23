// Wearable controller for Heart of Maker Faire management
// Provides four buttons which illuminate when a Heart is being added
// to the shelves. Pressing the illuminated button sends a Clear to
// the appropriate channel, commanding Heartsim to revert the location
// colour to red.
// TODO: clear the colour allocation from the SQL.
// Jonathan Sanderson, Northumbria University, 2017-03-22.
// This code targets WeMos D1 mini / Adafruit Feather Huzzah.

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Sequence here is YELLOW, ORANGE, GREEN, CYAN
int numButtons = 4;
String colours[] = { "YELLOW", "ORANGE", "GREEN", "CYAN" }; // not used, in the end
int lights[] = { 0, 14, 16, 15 };
int buttons[] = {12, 4, 5, 13};
// Temporary storage for heart references:
int hearts[4] = {};

const char* ssid = "nustem";
const char* password = "nustem123";
const char* mqtt_server = "192.168.1.1";

String subsTopicString;
char subsTopicArray[100];
char tempBuffer[60];      // Temp for MQTT publish string/array conversions
char tempBuffer2[60];

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

    for (int i = 0 ; i < numButtons ; i++) {
        pinMode(lights[i], OUTPUT);
        pinMode(buttons[i], INPUT_PULLUP);
        digitalWrite(lights[i], LOW);
    }

    setup_wifi();
  
    // Get this Huzzah's MAC address and use it to register with the MQTT server
    huzzahMACAddress = WiFi.macAddress();
    skutterNameString = "skutter_" + huzzahMACAddress;
    Serial.println(skutterNameString);
    skutterNameString.toCharArray(skutterNameArray, 60);
  
    // For testing purposes, subscribe to everything in this namespace
    subsTopicString = "heart/#";
    subsTopicString.toCharArray(subsTopicArray, 60);
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
  
    // The actual channel subscription is handled in reconnect(), based on
    // the character arrays calculated above.

}


void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    buttonRead();
    delay(100);
}


void buttonRead() {
    // Buttons return 1 when unpressed, 0 when pressed (short to GND)
    for (int i = 0; i < numButtons; i++) {
        int value = digitalRead(buttons[i]);
        if (!value) {
            // Check to see if the buttons that's been pressed is active
            if (digitalRead(lights[i])) {
                // Now handle the MQTT
                // we're going to be commanding heart# hearts[i]
                // to setMode, clear.
                String sendTopicString = "heart/";
                sendTopicString += hearts[i];
                sendTopicString += "/setMode";
                String sendPayloadString = "clear";
                sendPayloadString.toCharArray(tempBuffer, 60);
                sendTopicString.toCharArray(tempBuffer2, 60);
                client.publish(tempBuffer2, tempBuffer);
                // ...and we'll let our own callback turn off the light.
                Serial.print("Sent : ");
                Serial.print(tempBuffer2);
                Serial.print(" message: ");
                Serial.println(tempBuffer);
                delay(200); // debounce
            }
        } // handle presses
    
    } // Loop through buttons
}

// Handle MQTT message receipt
void callback(char* topic, byte* payload, unsigned int length) {

    // Convert topic and message to C++ String types, for ease of handling
    String payloadString;
    String subString;
    int pieceEnd;
    int heartNum;
    String command;
    for (int i = 0; i < length; i++) {
        payloadString += String((char)payload[i]);
    }
    String topicString;
    for (int i = 0; i < strlen(topic); i++) {
        topicString += String((char)topic[i]);
    }
    // Debug: print the (processed) received message to serial
    Serial.print("Message arrived on [");
    Serial.print(topicString);
    Serial.print("] : ");
    Serial.println(payloadString);

    // Let's start throwing Strings around
    // Find the index position of the first /, if any
    pieceEnd = topicString.indexOf('/');

    // This is a horribly ugly way of parsing the MQTT topic, but
    // on the other hand, it works. So I'm not going to mess around.
    // ... for now.
    if (pieceEnd != -1) {
        // Pull the first part of the topic
        subString = topicString.substring(0, pieceEnd);
        // Check we're in the intended namespace
        if (subString == "heart") {
            // Chop the front part
            topicString = topicString.substring(pieceEnd+1);
            // Find the next '/'
            pieceEnd = topicString.indexOf('/');
            // Check there is one
            if (pieceEnd != -1) {
                subString = topicString.substring(0, pieceEnd);
                // Extract the heart number
                heartNum = subString.toInt();
                // Chunk the topicString again
                topicString = topicString.substring(pieceEnd+1);
                // and now we should be left with the command.
                // So this is where we handle the received command.
                // ...which strikes me as fairly nasty. But hey, if it works...

                // Look to see if setMode called
                if (topicString == "setMode") {
                    // Check for colour channel assignment, and handle each
                    if (payloadString == "yellow") {
                        // Assign heartNum to store
                        hearts[0] = heartNum;
                        // Turn on appropriate button
                        digitalWrite(lights[0], HIGH);
                        Serial.print("YELLOW channel assigned to heart: ");
                        Serial.println(hearts[0]);
                    } else if (payloadString == "orange") {
                        hearts[1] = heartNum;
                        digitalWrite(lights[1], HIGH);
                        Serial.print("ORANGE channel assigned to heart: ");
                        Serial.println(hearts[1]);
                    } else if (payloadString == "green") {
                        hearts[2] = heartNum;
                        digitalWrite(lights[2], HIGH);
                        Serial.print("GREEN channel assigned to heart: ");
                        Serial.println(hearts[2]);
                    } else if (payloadString == "cyan") {
                        hearts[3] = heartNum;
                        digitalWrite(lights[3], HIGH);
                        Serial.print("CYAN channel assigned to heart: ");
                        Serial.println(hearts[3]);
                    } else if (payloadString == "clear") {
                        // Handle deselecting colours
                        for (int i = 0; i < numButtons; i++) {
                          // Look to see if the target heart is referenced in our
                          // colour array. If so, it must have been cleared elsewhere,
                          // so update our state to reflect the global state
                            if (hearts[i] == heartNum) {
                                // Turn the appropriate light OFF
                                digitalWrite(lights[i], LOW);
                            }
                        }
                    } // end of what would be a switch(), if we could do that on a String
                } // setMode
            } // pieceEnd
        } // heart

    } // pieceEnd test - have we more MQTT topic String to go?

} // MQTT callback

