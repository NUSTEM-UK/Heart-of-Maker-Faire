// From http://www.ohnitsch.net/2015/03/18/measuring-heart-rate-with-a-piezoelectric-vibration-sensor/
// Streams output from DFRobot vibration sensor (piezo) attached to A2
// Modified to find maximum output

int avg = 0;
int max = 0;
int new_reading = 0;


void setup() {
  Serial.begin(57600); 
}

void loop() {
  avg = 0;
  for(int i=0;i<64;i++){
    avg+=analogRead(A2);
  }
  new_reading = avg/64;
  if (new_reading > max) {
    max = new_reading;
    Serial.print("NEW PEAK: ");
    Serial.print(max);
    Serial.print(" | ");
  }
  Serial.println(new_reading,DEC);
  delay(5);
}
