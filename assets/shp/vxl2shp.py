#!/usr/bin/python3
import shutil
import os
import glob
from PIL import Image, ImageColor, ImagePalette
import cv2
import numpy as np
from recolor import calc_best_match
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

The above looks tedious but it will get rid of manual work.
Since we have manay images to compare, we can tell computer to determine
which is BG and which is house color!
Once you have all these, just run this script to merge them.
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



def crop_center(ifname, rect):
    img = cv2.imread(ifname)
    x, y, xend, yend = rect
    return img[y:yend, x:xend]



def get_bg_housecolor(b, g, r):
    '''
    Given 3 images that have {b, g, r} background,
    tell which are house color and bg.
    '''
    b = b.astype(np.int)
    g = g.astype(np.int)
    r = r.astype(np.int)

    # Average 'em out.
    out = b + g + r
    out //= 3

    # But, house colors and BGs have high color difference.
    diffb = np.absolute(b - out).sum(axis=2)
    diffg = np.absolute(g - out).sum(axis=2)
    diffr = np.absolute(r - out).sum(axis=2)
    diff = diffb + diffg + diffr

    bgs = []
    hcs = []

    h, w, ch = b.shape
    for i in range(h):
        for j in range(w):
            if diff[i, j] > 100:
                # BG, if blue component bigger than others in blue image
                if b[i, j, 0] > b[i, j, 1] :
                    bgs.append((i, j))
                else:
                    hcs.append((i, j))

    return bgs, hcs



def merge(ofname, b, g, r, shadow, pal):
    '''
    Merge images to make a beautiful output vxl2shp automatically.
    pal: IMAGE that holds the palette.
    '''
    bgs, hcs = get_bg_housecolor(b, g, r)

    # Average colors to remove anti-alias artifact.
    out = b.astype(np.int) + g.astype(np.int) + r.astype(np.int)
    out //= 3

    # Lets use PIL to convert them to index color mode.
    cv2.imwrite("tmp.png", out)
    converted = Image.open("tmp.png").quantize(palette=pal)

    # Apply bg color
    px = converted.load()
    for y, x in bgs:
        px[x, y] = 0

    # Apply house color
    hc_dest = range(16, 31+1) # [16, 31] is RA2 house color index
    for y, x in hcs:
        best = calc_best_match(pal.getpalette(), px[x, y], hc_dest)
        px[x, y] = best

    # Apply shadow
    shadow_index = 1 # 1 is shadow, in RA2.
    rows, cols, ch = shadow.shape
    for i in range(rows):
        for j in range(cols):
            # not pure blue in shadow == actual shadow
            if px[j, i] == 0 and shadow[i, j, 0] != 255:
                px[j, i] = shadow_index

    converted.save(ofname)
    print(ofname)



if __name__ == "__main__":
    # setup
    cnt = 32
    name = "cmon"
    odir = "cmon"

    bdir = odir + "/b"
    gdir = odir + "/g"
    rdir = odir + "/r"
    sdir = odir + "/shadow"

    # For me, window decoration is captured ant it is in this rect:
    client_rect = (10, 39, 1610, 939)
    wh = (70, 70) # crop centered, with output area of this size
    rect = calc_rect(client_rect, wh)

    # Image to get palette from (PIL doesn't support palette so well)
    pal = Image.open("ra2unittem.png")

    # copying part
    for i in range(cnt):
        ifname = "K-{:03d}.png".format(i + 1)
        bfname = os.path.join(bdir, ifname)
        gfname = os.path.join(gdir, ifname)
        rfname = os.path.join(rdir, ifname)
        sfname = os.path.join(sdir, ifname)

        b = crop_center(bfname, rect)
        g = crop_center(gfname, rect)
        r = crop_center(rfname, rect)
        s = crop_center(sfname, rect)

        ofname = "{} {:04d}.png".format(name, i)
        ofname = os.path.join(odir, ofname)
        merge(ofname, b, g, r, s, pal)

    os.remove("tmp.png")
