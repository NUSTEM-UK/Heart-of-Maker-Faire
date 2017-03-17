// Setup WiFi network, reporting local IP address to serial
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
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

}


// Maintain MQTT broker connection, subscribe to topics on (re)connect
void reconnect() {
  // Loop until we're reconnected
  digitalWrite(00, HIGH);
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    digitalWrite(00, LOW);
    if (client.connect(skutterNameArray)) {
      Serial.println("connected");
//      client.publish("orchestra/announce", subsTargetArray);
      client.subscribe(subsTopicArray);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      digitalWrite(00, HIGH);
      delay(5000);
    }
  }
}

