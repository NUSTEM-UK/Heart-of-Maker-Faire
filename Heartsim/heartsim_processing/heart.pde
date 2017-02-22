// A Cell object
class Heart {
    // A cell object knows about its location in the grid
    // as well as its size with the variables x,y,w,h
    float serial;        // Which number heart am I?
                         // (is that actually necessary?)
    float x,y;           // x,y location
    float w,h;           // width and height
    int[] frames;        // animation frames (array)
    int hue;             // What colour are we?
    int targetHue;       // Colour we're transitioning to
    int framesToGo;      // How long before we get to targetColor?

    int frameNumber;     // frame number for animation processing

    // Cell Constructor
    Heart(float t_serial, float t_x, float t_y, float t_w, float t_h,
          int[] t_frames, int t_hue) {
        serial = t_serial;
        x = t_x;
        y = t_y;
        w = t_w;
        h = t_h;
        frameNumber = 0;
        frames = t_frames;
        hue = t_hue;
        targetHue = hue;
        framesToGo = 0;
    }

    // Oscillation means increase angle
    void iterate(timestep) {
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
