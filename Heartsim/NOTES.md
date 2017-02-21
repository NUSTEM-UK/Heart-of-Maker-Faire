# Heartsim rolling notes

## Performance

Basic test code (as of 2017-02-09) takes about 58sec to push 12 cells / 60 pixels for 5000 frames. Which is fairly hopeless. Using the `fastopc` library rather than `opc` reduces this to 18.6 secs.

Running the default version under pypy results in a run time of 3.3 secs (~2 secs user). Which is rather more palatable. Unfortunately, the version of `pypy` in the Raspberry Pi repositories is very out of date (v4.0.1), and most of the `numpy` compatibility work has been done subsequently.

As a result, we'll need to explore installing a more recent `pypy`, which in turn involves finally wrapping our heads around `virtualenv`. Then, there are two routes to installing `numpy` under `pypy`: see [this page](http://pypy.org/download.html). My hunch: the `NumPyPy` route may be beneficial in our case, unless we do all our list processing in `numpy` arrays (which may be beneficial anyway).

...but for the moment, let's stick with the base `opc` library, execute under `pypy`, and assume we're going to run multiple executables from a single Pi (and/or multiple Pis). We're getting close to being able to run this under Python rather than having to port to Processing.

On the other hand, running under Processing would also give us a neat-o visualisation. Hmm.

## Dev push 2017-02-21

New thinking: to test this without building the whole darned installation, a visualisation would be *really* helpful. So let's refocus our efforts on Processing.

[...]

Well, that was a washout, what with all the car MOT nonsense.

### Getting set up with Processing

Following [Adafruit guide](https://learn.adafruit.com/led-art-with-fadecandy/tools-and-parts). Today, I'm working on Quintain (Mac Pro).

* [Processing 3](https://processing.org) installed.
* [FadeCandy release 02](https://github.com/scanlime/fadecandy/releases/tag/package-02) (download the 'source code', and there's an OS X binary in `/bin`)

Run the FadeCandy server, and we're good. Note that the `OPC.pde` module needs an edit to work under P3: change line 30 to:

    registerMethod("draw", this);
