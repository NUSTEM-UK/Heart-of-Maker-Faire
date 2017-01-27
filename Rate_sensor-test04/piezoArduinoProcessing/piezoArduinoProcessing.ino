void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
int vibration = analogRead(A0);
Serial.println(vibration*10);
delay(10);
}
