#!/usr/bin/python3
import shutil
import os
import glob
from PIL import Image
'''
Convert voxel to shp, using Garion's VXL2SHP map.
(In-game map!!!)
I modded it to automatically set focus to each unit so that
you can take screenshots periodically.

Disable pixel doubling!

With vxl2shp map...
Take screenshots of the color settings x unit setting

(without shadow)
1. bg = b, house color = FFFF00
2. bg = g, house color = FF00FF
3. bg = r, house color = 00FFFF

Then make another set, rendering shadow only, with blue BG.

To render shadow/unit only, go to Mods.Common\Graphics\VoxelRenderable.cs:125
Game.Renderer.WorldRgbaSpriteRenderer.DrawSprite(renderProxy.ShadowSprite...)
Game.Renderer.WorldRgbaSpriteRenderer.DrawSprite(renderProxy.Sprite...)
Comment them out as you wish.

You'll get 4 settings x 32 rotating images.

1. Make screenshots of units
2. Use gimp to mass apply palette to ra2-unittem.pal
   If you use BIMP, then gimp-image-convert-indexed is what you are looking for.
   You have to create RA2 palette for gimp to use prior to this though.
'''



def calc_rect(rect, wh):
    x1, y1, x2, y2 = rect

    W = x2 - x1
    H = y2 - y1

    w, h = wh
    assert W > w
    assert H > h
    x = int((W - w) / 2)
    y = int((H - h) / 2)

    x += x1
    y += y1
    return (x, y, x + w, y + h)



def crop_center(ifname, ofname, rect):
    img = Image.open(ifname)
    img2 = img.crop(rect)
    img2.save(ofname)



def crop_centers(wildcard, wh):
    for fname in glob.glob(wildcard):
        crop_center(fname, wh)



if __name__ == "__main__":
    # setup
    name = "cmin"
    idir = "cmin"
    odir = "cmin"
    cnt = 32
    offset = 8

    # For me, window decoration is captured ant it is in this rect:
    client_rect = (10, 39, 1610, 939)
    wh = (70, 70) # crop centered, with output area of this size
    rect = calc_rect(client_rect, wh)

    # copying part
    for i in range(cnt):
        ifname = "K-{:03d}.png".format(i + 1)
        ofname = "{} {:04d}.png".format(name, i)
        ifname = os.path.join(idir, ifname)
        ofname = os.path.join(odir, ofname)
        print(ifname, "\t", ofname)
        crop_center(ifname, ofname, rect)
