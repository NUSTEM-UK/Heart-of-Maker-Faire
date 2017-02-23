// Adapted from the 2D Array example code, primarily.

OPC opc;

Heart[] hearts;

// Number of columns and rows in the grid
int cols = 36;
int rows = 14;
int numHearts = cols * rows;

int heartsize = 10;  // pixel width/height

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
        float hue = 0;
        float heartRate = random(50, 120);
        // float heartRate = 60;
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
    opc.ledStrip(448, 60, ((cols*heartsize)/6), (heartsize * 7)-(heartsize/2), (heartsize/5), 0, true);

    frameRate(60);
    colorMode(HSB);

}

void draw() {
    background(0);
    // The counter variables i and j are also the column and row numbers and
    // are used as arguments to the constructor for each object in the grid.
    for (int i = 0; i < numHearts; i++) {
        // Oscillate and display each object
        hearts[i].update();
        hearts[i].display();
    }

    // Randomly set colour of random cell, for teh lolz
    // int targetHeart = int(random(numHearts));
    // hearts[targetHeart].setColour(random(255));

    // println(frameRate);
}
