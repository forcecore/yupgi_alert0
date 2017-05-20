#!/usr/bin/python3
import shutil
import os
import glob
from PIL import Image
'''
Converts 360 animation from OS voxel viewer (PPM site) to SHP,
since current implementation of voxel is slow on OpenRA.

1. Open voxel on OS shp editor.
2. Uncheck draw ground, draw sky
3. Tools -> background color -> blue
4. View -> views -> game TS/RA2
5. View -> camera manager -> Yrot = 0.
   In my case the first frame faces left and this script is made for that.
6. Tools -> make 360 degree animation.
   Set size to 600? (as big as you want)
   Frames: 32 (number of facings to export)
   The direction of rotation doesn't really matter too much, as you can
   make OpenRA to have negative values as Facing parameter in your sequences YAML
7. The gif file will be at C:\Program Files (x86)\CnC_Tools\ScreenShots or
   wherever you installed OS voxel viewer.
   Extract the frames. I use Image Magick to do that:
   convert zep_000.gif zep.png
   You get zep-0.png, zep-1.png, ...
8. You still need to apply RA2 palette, XCC mixer doesn't seem to work well.
   Use gimp and BIMP plugin to do that in mass.
   gimp-convert-rgb filter then gimp-image-convert-indexed.
   You need to make custom ra2 palette for gimp prior to this task though.
   Don't check "Remove unused or duplicate color..." option.
'''



def calc_rect(img, wh):
    W, H = img.size
    w, h = wh
    assert W > w
    assert H > h
    x = int((W - w) / 2)
    y = int((H - h) / 2)
    return (x, y, x + w, y + h)



def crop_center(fname, wh):
    img = Image.open(fname)
    rect = calc_rect(img, wh)
    img2 = img.crop(rect)
    img2.save(fname)



def crop_centers(wildcard, wh):
    for fname in glob.glob(wildcard):
        crop_center(fname, wh)



if __name__ == "__main__":
    # setup
    name = "zep"
    idir = "in"
    odir = "out"
    cnt = 32
    offset = 8
    wh = (100, 100) # crop centered, with output area of this size

    # copying part
    for i in range(cnt):
        ifname = "{}-{}.png".format(name, i)
        j = (offset + i) % cnt
        ofname = "{} {:04d}.png".format(name, j)
        ifname = os.path.join(idir, ifname)
        ofname = os.path.join(odir, ofname)
        print(ifname, "\t", ofname)
        shutil.copyfile(ifname, ofname)

    wildcard = os.path.join(odir, "*.png")
    crop_centers(wildcard, wh)
