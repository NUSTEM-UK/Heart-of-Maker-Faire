// WeMos test code for MQTT parsing.
// Based on Robot_Orchestra_Wemos


#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "nustem";
const char* password = "nustem123";
const char* mqtt_server = "192.168.1.1";

String subsTopicString;
char subsTopicArray[100];
char tempBuffer[60];        // Temporary for MQTT publish string/array conversions

WiFiClient espClient;
PubSubClient client(espClient);

// Each device has a unique name, generated from the hardware MAC address.
// These variables will store those names.
String huzzahMACAddress;
String skutterNameString;
char skutterNameArray[60];

void setup() {
    Serial.begin(115200);
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
                // So this is where we'd handle the received command.
                // ...which strikes me as fairly nasty. But hey, if it works...
                Serial.print("Command would be to heart #");
                Serial.print(heartNum);
                Serial.print(" with signal: ");
                Serial.print(topicString);
                Serial.print(" and value: ");
                Serial.println(payloadString);
            }
            
        }
    }

    // Chuck the payload back to the root topic, as a demo
    // Payload needs to be a char* array, so we first make that:

    // Wrap this in a test so we don't flood the channel in this example.
    // ...not that I did that. Ahem.
    if ( heartNum != 0 ) {
        payloadString.toCharArray(tempBuffer, 60);
        client.publish("heart/00/test", tempBuffer);
    }
}

