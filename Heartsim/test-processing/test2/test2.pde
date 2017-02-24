void setup() {
  size(200, 200);
  background(255);
}

void draw() {
  stroke(0);
  rectMode(CENTER);
  line(pmouseX, pmouseY, mouseX, mouseY);
}

void keyPressed() {
  background(255);
}