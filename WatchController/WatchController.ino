int numButtons = 4;

// Sequence here is RED, ORANGE, BLUE, GREEN
String colours[] = { "RED", "ORANGE", "BLUE", "GREEN" };
int lights[] = { 0, 14, 15, 16 };
int buttons[] = {4, 5, 12, 13};

void setup() {
  for (int i = 0 ; i < numButtons ; i++) {
    pinMode(lights[i], OUTPUT);
    pinMode(buttons[i], INPUT_PULLUP);
  }

  Serial.begin(115200);
}


void loop() {
  for (int i = 0; i < numButtons; i++) {
    digitalWrite(lights[i], HIGH);

    buttonRead();
    delay(1000);
  }
  for (int i = 0 ; i < numButtons; i++) {
    digitalWrite(lights[i], LOW);
    buttonRead();
    delay(1000);
  }
  
}


void buttonRead() {
  // Buttons return 1 when unpressed, 0 when pressed (short to GND)
  for (int i = 0; i < numButtons; i++) {
    int value = digitalRead(buttons[i]);
    Serial.print("Button: ");
    Serial.print(colours[i]);
    Serial.print(" State: ");
    Serial.println(value);
  }
}

