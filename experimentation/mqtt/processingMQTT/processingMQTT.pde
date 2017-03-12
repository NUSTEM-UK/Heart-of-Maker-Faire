import mqtt.*;

MQTTClient client;

void setup() {

    // Initialise the MQTT connection
    // See https://github.com/256dpi/processing-mqtt
    client = new MQTTClient(this);
    // Connect to MQTT server, identifying this client ID as heartsim
    client.connect("mqtt://192.168.1.1", "heartsim");
    // Subscribe to the /heart topic
    client.subscribe("heart/#");
    // client.subscribe(".heart", int qos);

}

void draw() {
}

void messageReceived(String topic, byte[] payload) {
    println(">>> New message: " + topic + " :: " + new String(payload));
    println("> Parsing topic string:");
    String[] parts = topic.split("/");
    for (int i = 0; i < parts.length; i++) {
      println(parts[i]);
    }
    println("> Payload:");
    String payloadString = new String(payload);
    println(payloadString);

    // Test command parsing
    if (parts.length > 2) {
      int heartNum = Integer.parseInt(parts[1]);
      String command = parts[2];

      if (command.equals("setRate")) {
        println("### Command Heart #" + heartNum + " to setRate: " + Integer.parseInt(payloadString) );
        // Call hearts[heartNum].setRate(Integer.parseInt(payloadString));
      }

    }
}

// TODO: Handle disconnection & reconnection; handle incomplete messages
