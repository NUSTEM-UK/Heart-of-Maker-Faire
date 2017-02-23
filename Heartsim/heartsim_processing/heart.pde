// A Cell object
class Heart {
    // A cell object knows about its location in the grid
    // as well as its size with the variables x,y,w,h
    int x,y;             // x,y location
    int size;            // width and height
    int rate;            // Target heartrate
    // int[] frames;        // animation frames (array)
    int hue;             // What colour are we?
    int targetHue;       // Colour we're transitioning to
    int framesToGo;      // How long before we get to targetColor?

    int frameNumber;     // frame number for animation processing
    float angle;

    // Cell Constructor
    Heart(int t_x, int t_y, int t_size, float t_rate, float t_hue) {
        x = t_x;
        y = t_y;
        size = t_size;
        rate = int(t_rate);
        hue = int(t_hue);
        targetHue = hue;
        frameNumber = 0;
        framesToGo = 0;
        angle = 0;
    }

    void setRate(int t_rate) {
        rate = t_rate;
    }

    void setColour(float t_hue) {
        hue = int(t_hue);
    }

    // Oscillation means increase angle
    void update() {
        angle += 0.001 * rate;
    }

    void display() {
        // Setting noStroke() doubles frame rate (to about 40 on RPi, 120 on
        // low-end Windows tablet; 550+ on iMac 5K)
        stroke(255);
        // noStroke();
        // Color calculated using sine wave
        // fill(127+127*sin(angle), 255, 255);
        fill(hue, 255, 127+127*sin(angle));
        rect(x,y,size,size);
    }
}
