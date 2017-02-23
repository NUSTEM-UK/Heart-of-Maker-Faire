// A Cell object
class Heart {
    // external global: frames[]
    // A cell object knows about its location in the grid
    // as well as its size with the variables x,y,w,h

    int x,y;             // x,y location
    int size;            // width and height
    float rate;            // Target heartrate
    // int[] frames;        // animation frames (array)
    int hue;             // What colour are we?
    int targetHue;       // Colour we're transitioning to
    int framesToGo;      // How long before we get to targetColor?
    int mag;           // Current brightness
    int numFrames;      // Total number of frames in animation

    float step;           // step for animation processing
    int currentAnimFrame; // current animation frame
    float angle;

    // Cell Constructor
    Heart(int t_x, int t_y, int t_size, float t_rate, float t_hue) {
        x = t_x;
        y = t_y;
        size = t_size;
        rate = t_rate;
        this.setRate(rate);
        hue = int(t_hue);
        targetHue = hue;
        // step = float(rate)/240.0 * (60.0/4.0);
        currentAnimFrame = 0;
        framesToGo = 0;
        angle = 0;
        mag = 78;
        numFrames = frames.length;
    }

    void setRate(float t_rate) {
        rate = t_rate;
        // step for animation; correct for oversampling of animation data
        step = rate/240.0 * (60.0/4.0);
    }

    void setColour(float t_hue) {
        hue = int(t_hue);
    }

    // Oscillation means increase angle
    void update() {
        currentAnimFrame += round(step);
        currentAnimFrame = currentAnimFrame % numFrames;
        mag = frames[currentAnimFrame];
        // angle += 0.001 * rate;
    }

    void display() {
        // Setting noStroke() doubles available frame rate (to about 40 on RPi,
        // 120 on low-end Windows tablet; 550+ on iMac 5K)
        stroke(255);
        // noStroke();
        // fill(127+127*sin(angle), 255, 255);
        fill(hue, 255, mag);
        rect(x,y,size,size);
    }
}
