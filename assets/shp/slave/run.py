#!/usr/bin/python3
#!/usr/bin/python3
from PIL import Image, ImageDraw
import glob
import os
from recolor import replace_color

dest = "."

for fname in glob.glob("in/*.png"):
    im = Image.open(fname)

    replace_color(im, range(112, 123+1), range(80, 95+1))

    _, ofname = os.path.split(fname)
    ofname = os.path.join(dest, ofname)
    print(fname, ofname)
    im.save(ofname)
