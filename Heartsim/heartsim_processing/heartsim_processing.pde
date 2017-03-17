/* ************************************************
** HEARTSIM                                      **
** Simulates a displayed grid of beating hearts. **
** Run in Processing3 on a Raspberry PI, which   **
** also serves as FadeCandy server.              **
**                                               **
** Originally built for Maker Faire UK 2017      **
** by Jonathan Sanderson and Joe Shimwell        **
** NUSTEM, Northumbria University, Newcastle, UK **
**                                               **
** Dependencies:                                 **
** opc  : Open Pixel Control. See Adafruit docs. **
** mqtt : Install from Processing GUI.           **
** SQL  : Install from Processing GUI.           **
** Requirements:                                 **
** MySQL server & MQTT broker, assumed to be on  **
** same host (Pi Zero W)                         **
**                                               **
** See Github for full documentation.            **
***************************************************
*/

OPC opc;
import mqtt.*;
import de.bezier.data.sql.*;

MQTTClient client;
MySQL mysql;

Heart[] hearts;

// Number of columns and rows in the grid
int cols = 30;
int rows = 16;
int numHearts = cols * rows;
// Geometry: over how many boards is the display arranged?
// Should be a factor of cols
int boards = 3;
// Across how many LEDs does each heart span?
int spanLEDs = 5;
int stripLength = (cols / boards) * spanLEDs;

// Performance-sensitive configuration options
// For Raspberry Pi, set this to 10 for 60fps performance.
int heartsize = 10;           // pixel width/height
boolean drawOutlines = false; // draw cell outline frames?
                              // true arguably looks nicer,
                              // but false is *much* faster, on RPi

// MySQL connection, for disaster recovery or resyncing
String user = "root";         // Yes, yes. We know.
String pass = "plokij";       // Seriously. We *are* this lame
String server = "192.168.1.1";
String dbname = "Heart";

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

    // BEGIN OPC configuration

    // Connect to the OPC server
    opc = new OPC(this, "127.0.0.1", 7890);

    // Set the location of several LEDs arranged in a strip.
    // (x,y) is the center of the strip.
    // void ledStrip(int index, int count, float x, float y, float spacing, float angle, boolean reversed)

    // For most versions, we want the strips to be run in reversed geometry.
    // This also seems to be marginally faster, which makes no sense to me,
    // but so it goes.
    boolean reversed = true;

    // First, the left-most column
    // precalculate the horizontal centre
    float xcentre = (cols * heartsize)/6.0;
    for (int i = 0; i < 16 ; i++) {
        opc.ledStrip( i * 64, stripLength, xcentre, (heartsize * i)+(heartsize/2), (heartsize/spanLEDs), 0, true );
        println ("Strip " + i + " initialized");
    }
    println( ">>> COLUMN 1 COMPLETE" );

    // Centre column. Again, precalculate horizontal centre
    xcentre = (cols * heartsize) / 2.0;
    for (int i = 0; i < 16 ; i++) {
        opc.ledStrip( (i+16) * 64, stripLength, xcentre, (heartsize * i)+(heartsize/2), (heartsize/spanLEDs), 0, true );
        println ("Strip " + (i+16) + " initialized");
    }
    println( ">>> COLUMN 2 COMPLETE" );

    // ...and the rightmost column
    xcentre = ((cols * heartsize) * 5.0)/6.0;
    for (int i = 0; i < 16 ; i++) {
        opc.ledStrip( (i + 32) * 64, stripLength, xcentre, (heartsize * i)+(heartsize/2), (heartsize/spanLEDs), 0, true );
        println ("Strip " + (i+32) + " initialized");
    }
    println( ">>> COLUMN 3 COMPLETE" );
    // END OPC configuration

    // BEGIN MQTT configuration
    // Initialise the MQTT connection
    // See https://github.com/256dpi/processing-mqtt
    client = new MQTTClient(this);
    // Connect to MQTT server, identifying this client ID as heartsim
    client.connect("mqtt://192.168.1.1", "heartsim");
    // Subscribe to the /heart topic
    client.subscribe("heart/#");
    // client.subscribe(".heart", int qos);
    // END MQTT configuration

    // Conenct to the MySQL server. Might as well hold this connection open
    mysql = new MySQL( this, server, dbname, user, pass );

    frameRate(60);
    colorMode(HSB);

} // setup()

void draw() {
    background(0);

    // Iterate over the hearts, telling each to update and display.
    for (int i = 0; i < numHearts; i++) {
        // Oscillate and display each object
        hearts[i].update();
        hearts[i].display();
    }

    // Following test code commented out, since we're now able to command the
    // simulation from MQTT.

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
} // draw()

void messageReceived(String topic, byte[] payload) {
    println("new message: " + topic + " - " + new String(payload));

    // Tokenise the topic string by splitting it on '/'
    String[] topicParts = topic.split("/");
    // Convert the payload to a String. We're not overly-worried about performance,
    // and this is easy. We may revisit later, however.
    String payloadString = new String(payload);

    // Parse commands.
    // First check if the topic is long enough to contain a valid command
    if (topicParts.length > 2) {
      // Work out to which heart we're speaking
      int heartNum = Integer.parseInt(topicParts[1]);
      // ...and the command we're sending it
      String command = topicParts[2];

      // Handle setMode = update
      if (command.equals("setMode")) {
        if (payloadString.equals("update")) {
          // Set random colour for this heart
          hearts[heartNum].setColour(random(255), 1.0);
        }
      }

      // Handle setRate command
      if (command.equals("setRate")) {
        println("### Command Heart #" + heartNum + " to setRate: " + Integer.parseInt(payloadString) );
        hearts[heartNum].setRate(Integer.parseInt(payloadString));
      }

      // Handle setMode = clear
      if (command.equals("setMode")) {
        if (payloadString.equals("clear")) {
          // Change the colour to red over 5 seconds
          hearts[heartNum].setColour(0.0, 5.0);
          // Could send an acknowledgement here
        }
      }
    } // if topicParts.length
} // messageReceived

void keyPressed() {
  // Check to see if 'R' pressed
  // This acts as an automatic callback during draw()
  if (key == 82 ) {
    println(">>> EMERGENCY! SQL RELOAD REQUESTED!");
    if ( mysql.connect() ) {
      // Pull the data then step through it, rewriting the Hearts' rates
      mysql.query( "SELECT * from heart_store");
      while (mysql.next()) {
        int heartNum = mysql.getInt("cell_id");
        int heartRate = mysql.getInt("heart_rate");
        // If heartRate > 0, update that cell and trigger phase to red
        if (heartRate > 0) {
            hearts[heartNum].setRate(heartRate);
            hearts[heartNum].setColour(0.0, 5.0);
        }
      }
      println("<<< SQL RELOAD COMPLETE");
    } else {
      println("<<< MySQL CONNECTION FAILED!");
    }
  }
}
