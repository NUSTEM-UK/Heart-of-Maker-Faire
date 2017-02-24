// Adapted from the 2D Array example code, primarily.

OPC opc;

// 2D Array of objects
Cell[][] grid;

// Number of columns and rows in the grid
int cols = 36;
int rows = 14;

void setup() {
    size(720,280);
    grid = new Cell[cols][rows];
    for (int i = 0; i < cols; i++) {
        for (int j = 0; j < rows; j++) {
            // Initialize each object
            grid[i][j] = new Cell(i*20,j*20,20,20,i+j);
        }
    }
    opc = new OPC(this, "127.0.0.1", 7890);
    // Set the location of several LEDs arranged in a strip.
    // Angle is in radians, measured clockwise from +X.
    // (x,y) is the center of the strip.
    // void ledStrip(int index, int count, float x, float y, float spacing, float angle, boolean reversed)
    opc.ledStrip(448, 60, (width/6), ((height/14)*7)-10, 4, 0, true);

    frameRate(1000);
    colorMode(HSB);
}

void draw() {
    background(0);
    // The counter variables i and j are also the column and row numbers and
    // are used as arguments to the constructor for each object in the grid.
    for (int i = 0; i < cols; i++) {
        for (int j = 0; j < rows; j++) {
            // Oscillate and display each object
            grid[i][j].oscillate();
            grid[i][j].display();
        }
    }
    println(frameRate);
}

// A Cell object
class Cell {
    // A cell object knows about its location in the grid
    // as well as its size with the variables x,y,w,h
    float x,y;     // x,y location
    float w,h;     // width and height
    float angle;   // angle for oscillating brightness

    // Cell Constructor
    Cell(float tempX, float tempY, float tempW, float tempH, float tempAngle) {
        x = tempX;
        y = tempY;
        w = tempW;
        h = tempH;
        angle = tempAngle;
    }

    // Oscillation means increase angle
    void oscillate() {
        angle += 0.02;
    }

    void display() {
        // Setting noStroke() doubles frame rate (to about 40 on RPi, 120 on
        // low-end Windows tablet; 550+ on iMac 5K)
        stroke(255);
        // noStroke();
        // Color calculated using sine wave
        // fill(127+127*sin(angle), 255, 255);
        fill(0, 255, 127+127*sin(angle));
        rect(x,y,w,h);
    }
}
