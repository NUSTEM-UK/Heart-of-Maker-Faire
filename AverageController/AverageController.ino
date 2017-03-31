#include <Adafruit_NeoPixel.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>


// NeoPixel strip settings
#define NeoPIN 4
#define strandLength 39
#define FPS 60.0
Adafruit_NeoPixel strip = Adafruit_NeoPixel(strandLength, NeoPIN, NEO_GRB + NEO_KHZ800);

// WiFi network and MQTT broker settings
const char* ssid = "nustem";
const char* password = "nustem123";
const char* mqtt_server = "192.168.1.1";

String subsTopicString;
char subsTopicArray[100];

WiFiClient espClient;
PubSubClient client(espClient);

// Each device has a unique name, generated from the hardware MAC address.
// These variables will store those names.
// For historical reasons, we refer to ESP8266-based devices as 'skutters'
String huzzahMACAddress;
String skutterNameString;
char skutterNameArray[60];

// Current animation position
int rate;
float currentAnimFrame;
float step;
int numFrames;

int lastTime = millis();
int currentTime = millis();
int sixtieth = (int)1000.0/FPS;

int frames[] = {
    78, 78, 78, 78, 78, 78, 78, 78, 79, 79, 80, 81, 83, 85, 87, 90, 94, 99,
    104, 111, 118, 126, 135, 145, 155, 166, 178, 189, 201, 212, 222, 232, 240,
    247, 252, 255, 255, 253, 248, 241, 231, 218, 203, 187, 169, 149, 130, 110,
    90, 71, 54, 38, 25, 15, 7, 2, 0, 1, 5, 11, 19, 28, 39, 51, 63, 74, 85, 95,
    104, 110, 115, 118, 119, 119, 116, 113, 108, 102, 95, 89, 82, 76, 71, 66,
    63, 60, 58, 58, 58, 60, 62, 64, 67, 71, 74, 77, 80, 82, 84, 85, 86, 87, 86,
    86, 85, 84, 83, 82, 80, 79, 78, 77, 76, 76, 75, 75, 75, 75, 76, 76, 76, 77,
    77, 78, 78, 78, 79, 79, 79, 79, 79, 79, 79, 79, 78, 78, 78, 78, 78, 78, 78,
    78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,
    78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,
    78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,
    78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,
    78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,
    78, 78, 78, 78
};

void setup() {
    Serial.begin(115200);

    // Set up on-board LEDs for diagnostics
    pinMode(02, OUTPUT);

    setup_wifi();

    // Get this Huzzah's MAC address and use it to register with the MQTT server
    huzzahMACAddress = WiFi.macAddress();
    skutterNameString = "skutter_" + huzzahMACAddress;
    Serial.println(skutterNameString);
    skutterNameString.toCharArray(skutterNameArray, 60);

    // Subscribe to the `average` heart
    subsTopicString = "heart/#";
    //    subsTopicString = "heart/average/setRate";
    subsTopicString.toCharArray(subsTopicArray, 60);
    client.setServer(mqtt_server, 1883);
    // Set up callback to handle payloads on this topic
    client.setCallback(callback);

    // Initialise all pixels to 'off'
    strip.begin();
    strip.show();

    // Start from the first frame of the animation
    currentAnimFrame = 0.0;
    // assume starting rate of 60bpm
    rate = 60;
    numFrames = 240;

}

void loop() {
    if (!client.connected()) {
        reconnect();
    }

    currentTime = millis();
    if (currentTime - lastTime > sixtieth) {
        strandUpdate();
        lastTime = millis();
    }
}

void strandUpdate() {
    // Advance by that many frames
    currentAnimFrame += step;
    currentAnimFrame = (int)currentAnimFrame % numFrames;
    // Get magnitude (of red channel) (at desired index)
    int mag = frames[round(currentAnimFrame)];

    // Update the strand
    for (int i = 0 ; i < strandLength ; i++) {
        strip.setPixelColor(i, mag, 0, 0);
    }

    // Flush to the strip
    strip.show();
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
            topicString = topicString.substring(pieceEnd + 1);
            // Find the next '/'
            pieceEnd = topicString.indexOf('/');
            // Check there is one
            if (pieceEnd != -1) {
                subString = topicString.substring(0, pieceEnd);
                // Check we've read the average channel
                if (subString == "average") {
                    topicString = topicString.substring(pieceEnd + 1);
                    // and now we should be left with the command.
                    // So this is where we handle the received command.
                    // ...which strikes me as fairly nasty. But hey, if it works...

                    // Look to see if setRate called, which it really should be
                    if (topicString == "setRate") {
                        rate = topicString.toInt();
                        // Calulate how many frames to advance
                        step = rate/240.0 * (FPS / 4.0);
                        // reset the frame counter so all average hearts beat in sync
                        currentAnimFrame = 0.0;
                    } // setRate
                } else {
                    Serial.println("It's all gone horribly wrong");
                }
            }
        } // heart
    } // pieceEnd
} // MQTT callback
