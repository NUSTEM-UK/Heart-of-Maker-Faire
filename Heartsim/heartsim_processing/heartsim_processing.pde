// Adapted from the 2D Array example code, primarily.

OPC opc;
import mqtt.*;

MQTTClient client;

Heart[] hearts;

// Number of columns and rows in the grid
int cols = 36;
int rows = 14;
int numHearts = cols * rows;
// Geometry: over how many boards is the display arranged?
// Should be a factor of cols
int boards = 3;
// Across how many LEDs does each heart span?
int spanLEDs = 5;
int stripLength = (cols / boards) * spanLEDs;

// For Raspberry Pi, set this to 10 for 60fps performance.
// Also set noStroke() in Heart.display().
int heartsize = 40;  // pixel width/height

void settings() {
    // Have to do this here in Processing3.x, rather than in setup()
    size(cols * heartsize, rows * heartsize);
}

void setup() {

    // Fire up the object array
    hearts = new Heart[numHearts];
    // Now initialise all those lovely hearts
    for (int i = 0; i < numHearts ; i++) {
        // determine heart position in matrix.
        // fill columns, then rows.
        int xpos = (i % cols) * heartsize;
        int ypos = abs(i / cols) * heartsize;
        // float hue = random(255);
        // float hue = 0;   // Red!
        float hue = 165; // Blue!
        float heartRate = 0.0; // Empty data
        // float heartRate = random(50, 150);
        // float heartRate = 120;
        hearts[i] = new Heart(
            xpos, ypos, heartsize,
            heartRate,
            hue
        );
    }

    // Connect to the OPC server
    opc = new OPC(this, "127.0.0.1", 7890);
    // Set the location of several LEDs arranged in a strip.
    // (x,y) is the center of the strip.
    // void ledStrip(int index, int count, float x, float y, float spacing, float angle, boolean reversed)
    for (int i = 0; i < 8 ; i++) {
        // println(i*64, stripLength, ((cols*heartsize)/6), (heartsize * i)+(heartsize/2), (heartsize/spanLEDs), 0);
        opc.ledStrip(i * 64, stripLength, ((cols*heartsize)/6), (heartsize * i)+(heartsize/2), (heartsize/spanLEDs), 0, true);
        println ("Strip " + i + " initialized");
    }
    // opc.ledStrip(448, 60, ((cols*heartsize)/6), (heartsize * 7)-(heartsize/2), (heartsize/5), 0, true);

    // Initialise the MQTT connection
    // See https://github.com/256dpi/processing-mqtt
    client = new MQTTClient(this);
    // Connect to MQTT server, identifying this client ID as heartsim
    client.connect("mqtt://localhost", "heartsim");
    // Subscribe to the /heart topic
    client.subscribe("heart/#");
    // client.subscribe(".heart", int qos);


    frameRate(60);
    colorMode(HSB);

}

void draw() {
    background(0);

    // Iterate over the hearts, telling each to update and display.
    for (int i = 0; i < numHearts; i++) {
        // Oscillate and display each object
        hearts[i].update();
        hearts[i].display();
    }

    // Set rate and colour of random cell, every 2 seconds
    // if (frameCount % int(random(15, 45)) == 0) {
    //     int targetHeart = int(random(numHearts));
    //     // hearts[targetHeart].setColour(random(255), 10.0);
    //     hearts[targetHeart].setColour(0, 6.0);
    //     hearts[targetHeart].setRate(random(30, 160));
    // }

    // If we're badly dropping frames, tell the console
    if (frameRate < 58 ) {
        println(frameRate);
    }

    // ...and around we go again
}

void messageReceived(String topic, byte[] payload) {
    println("new message: " + topic + " - " + new String(payload));

    // Tokenise the topic string by splitting it on '/'
    String[] topicParts = topic.split("/");
    // Convert the payload to a String. We're not overly-worried about performance,
    // and this is easy. We may revisit later, however.
    String payloadString = new String(payload);

    // Parse commands
    if (topicParts.length > 2) {
      // Work out to which heart we're speaking
      int heartNum = Integer.parseInt(topicParts[1]);
      // ...and the command we're sending it
      String command = topicParts[2];

      // Handle setRate commands
      if (command.equals("setRate")) {
        println("### Command Heart #" + heartNum + " to setRate: " + Integer.parseInt(payloadString) );
        hearts[heartNum].setRate(Integer.parseInt(payloadString));
      }

    }

    // TODO: parse and act on received messages.
}
