int v0, v1, v2, v3, v4;
unsigned long oldmillis = 0;
unsigned long newmillis = 0;
int cnt = 0;
int timings[8];

void setup() {
  Serial.begin(9600);
  delay(2000);
}

void loop() {
  v2 = v1;
  v1 = v0;
  for (int i = 0; i < 16; i++) { // Average over 16 measurements
    v0 += analogRead(A0);
  }
  v0 = v0 / 16;

  if (v0 < v1 && v1 > v2 && v1 > 1) {
  oldmillis = newmillis;
  newmillis = millis();

  timings[cnt%8] = (int)(newmillis-oldmillis);
  int totalmillis = 0;

  for(int i=0;i<8;i++){
    totalmillis +=timings[i];
  }
  int heartRate = 60000/(totalmillis/8);
  Serial.println(heartRate, DEC);
  cnt++;}
  

  }

