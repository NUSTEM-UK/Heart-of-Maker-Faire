# Pre-Processing QR codes

QRmaker will batch-create QR codes in the desired quantities, and exports PDFs aligned for label printing.

  python QRmaker.py

## Pre-processing for printing use

The thermal printer requires bytecode arrays for all bitmaps, with a Processing utility to handle the conversion from PNG. Accordingly:

1. Comment out QRmayer.py line 69 to store (not remove) the intermediate PNG files.
2. `mv *.png outputs/` to corral them in a temporary folder
3. On OS X, a suitable rescaling tool is `sips`. The original images are 58px square, so: `sips -Z 116 *.png` will rescale to double size. `-Z` preserves aspect ratio.
4. Run the Processing sketch to batch-convert `.png` to Arduino-friendly `.h` byte arrays. Adjust line 13 to give the full path of your input file directory.
5. `cat *.h > all.h` to concatenate the files. Note that this orders the files unix-style, not OS X-style (so it goes 0, 1, 10, 100, 101, 102, 103... 119, 12, ...). Which presumably isn't an issue since they're being read into a dictionary. Tell me these things are going into a dictionary, Joe.
