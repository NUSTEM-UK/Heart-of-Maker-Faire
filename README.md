# Heart-of-Maker-Faire
NUSTEM's installation piece for Maker Faire UK 2017. [More details on our website](https://nustem.uk/heartofmakerfaire/) (or, indeed, [on the official Raspberry Pi blog](https://www.raspberrypi.org/blog/heart-maker-faire/). WooT!). There's also a [film of the installation](https://www.youtube.com/watch?v=Er-b1X5HWGI).

We've never quite got around to tidying up in here, so it's a bit of a mess. It would, I think, be rather tricky for anyone to replicate the installation just from this repo. As a brief guide:

### /Heartsim/heartsim_processing
This is the main visualisation, written in Processing. The code ran on two Pis, each controlling half the LED array via via FadeCandy boards. In principle a single Pi would be up to the job, but in practice we struggled to get FadeCandies to talk to Pis via USB hubs. We needed six FadeCandies, so... two Pis. Drat.

Updates arrive at the simulation Pis via MQTT (crazy, we know, but we had the code lying around...), with a backup/emergency restore by pulling data from the SQL server.

### /ScanPi
The logging/control stations. The sequence of operations went:

* Participant writes message on tracing paper, and scunches it up into a jar.
* Jar lid has QR code, scanned by Picamera on control station.
* Control station allocates shelf space and temporary colour, broadcasting latter over MQTT.
* Participant's dials in their heart rate at the control station.
* Control station broadcasts change of beat frequency (over MQTT), and logs change in database.

Then...

### /WatchController
...once the jar is on the shelf, Wemos D1 mini-based controllers are used to clear the colour allocation. The Heartsim code rotates the LED colour to red, and the control stations are cleared to reuse the temporary colour.

### Other code
I *think* everything else here is intermediate code, experiments, and so on. There's a partial Python implementation of the FadeCandy control code, for example, which ran far too slowly to be useful for the scale we envisaged.


## TODO
Tidy the heck up.
