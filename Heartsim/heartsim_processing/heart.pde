// A Cell object
class Heart {
    // external global: frames[]
    // A cell object knows about its location in the grid
    // as well as its size with the variables x,y,w,h

    int heartNumber;        // Which heart am I?
    int x,y;                // x,y location
    int size;               // width and height
    float rate;             // Target heartrate
    // int[] frames;        // animation frames (array)
    int hue;                // What colour are we?
    int targetHue;          // Colour we're transitioning to
    int framesToGo;         // How long before we get to targetColor?
    int mag;                // Current brightness
    int numFrames;          // Total number of frames in animation

    float step;             // step for animation processing
    int currentAnimFrame;   // current animation frame
    float angle;

    // Cell Constructor
    Heart(int t_num, int t_x, int t_y, int t_size, float t_rate, float t_hue) {
        heartNumber = t_num;
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
        if (rate != 0) {
            // step for animation; correct for oversampling of animation data
            step = rate/240.0 * (60.0/4.0);
        } else {
            // We have no assigned heart rate, and we're going to run the
            // default animation at half a frame per frame
            step = 0.5;
        }

    }

    void setColour(float t_hue, float t_duration) {
        targetHue = int(t_hue);
        framesToGo = int(t_duration*60);
        println("Heart ", x, y, " changing to hue ", targetHue);
    }

    // Oscillation means increase angle
    void update() {
        // Cycle brightness animation
        currentAnimFrame += round(step);
        currentAnimFrame = currentAnimFrame % numFrames;
        if (rate != 0) {
            // We have a heart rate, so
            // Pick frame from beat simulation
            mag = frames[currentAnimFrame];
        } else if (hue != defaultHue) {
            // Play higher-range animation for more obvious locating of cell
            mag = framesDefaultHigh[currentAnimFrame];
        } else {
            // We don't have an assigned rate, so
            // Pick frame from default animation
            mag = framesDefault[currentAnimFrame];
        }

        // Handle colour animation
        if (hue != targetHue && framesToGo < 2) {
            hue = targetHue;
            println("Heart ", x, y, " hit targetColour");
        } else if (hue != targetHue && framesToGo != 0) {
            if (targetHue > hue) {
                hue += int((targetHue - hue) / framesToGo);
            } else {
                hue -= int((hue - targetHue) / framesToGo);
            }
            framesToGo--;
        }
    }

    void display() {
        if (renderDirect) {
            for (int i = 0; i < spanLEDs; i++) {
                opc.setPixel( ((heartNumber * spanLEDs) + i), color(hue, 255, mag) );
            }
        } else {
            // Setting noStroke() doubles available frame rate
            // Set noStroke() for Raspberry Pi 60fps.
            if (drawOutlines) {
              stroke(255);
            } else {
              noStroke();
            }
            // fill(127+127*sin(angle), 255, 255);
            fill(hue, 255, mag);
            rect(x,y,size,size);
        }
    }
}
