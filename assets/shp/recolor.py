#!/usr/bin/python3
from PIL import Image, ImageDraw
import glob
import os



RA2_HOUSE_COLORS = list(range(16,31))



def get_rgb( pal, color_index ) :
    r = pal[ color_index * 3 ]
    g = pal[ color_index * 3 + 1 ]
    b = pal[ color_index * 3 + 2 ]
    return (r, g, b)



def set_rgb( pal, color_index, rgb ) :
    pal[ color_index * 3 ], \
            pal[ color_index * 3 + 1 ], \
            pal[ color_index * 3 + 2 ] = rgb



def mse3( v1, v2 ) :
    s = 0
    for i in range( 3 ) :
        s += (v1[i] - v2[i])**2
    return s/3



def calc_best_match( pal, color, dest ) :
    rgb = get_rgb( pal, color )
    #print( "input:", rgb )

    best = -1
    best_mse = float('inf')

    for d in dest :
        rgb2 = get_rgb( pal, d )
        mse = mse3( rgb, rgb2 )
        #print( "mse with", rgb2, "=", mse )
        if mse < best_mse :
            best_mse = mse
            best = d

    return best



def calc_color_conversion( pal, src, dest ) :
    '''
    for each color in src, match the closest color in dest.
    src = (u, v) where u and v are color, given in palette index.
    dest = (p, q). Same as src.
    '''

    # pal is linearized. just pack them in 3.
    # in RGB, not BGR, fortunately.
    #for i in range( len( pal ) ) :
    #    print( pal[ i ], end=" " )
    #    if i % 3 == 2 :
    #        print()

    result = dict()
    for color in src :
        best_match = calc_best_match( pal, color, dest )
        result[ color ] = best_match
    return result



def replace_color(im, src, dest):
    mapper = calc_color_conversion( im.getpalette(), src, dest )

    # apply
    px = im.load() # pixel access
    for j in range( im.height ) :
        for i in range( im.width ) :
            if px[i, j] in src :
                px[i, j] = mapper[ px[i, j ] ]



def all_red2house_color(im):
    src = [8, 200, 201, 202, 203, 249, 250]
    dest = RA2_HOUSE_COLORS
    replace_color(im, src, dest)



def test_house_color(im):
    '''
    Test house color by modifying house color part of the palette.
    '''
    def replace_palette(im):
        pal = im.getpalette()
        # [16, 31] is RA2 palette house color range.
        for i in range(16, 31+1):
            r, g, b = get_rgb(pal, i)
            set_rgb(pal, i, (0, r, 0))
        set_rgb(pal, 1, (255, 0, 255)) # Shadow to magenta
        im.putpalette(pal)

    replace_palette(im)
    replace_color(im, [204], [0])
    replace_color(im, [197], [1])



def process_shadow(im, shadow_color_index):
    '''
    im: PIL Image.
    Replace anything that's not color index 0 to shadow color.
    '''
    px = im.load() # pixel access
    for j in range(im.height) :
        for i in range(im.width) :
            if px[i, j] != 0:
                px[i, j] = shadow_color_index
    return im



def draw_onto(dest, src):
    '''
    dest, src are PIL images.
    Draws src's what ever is not BG color onto dest.
    Modifies dest.
    '''
    assert dest.height == src.height
    assert dest.width == src.width

    px1 = dest.load()
    px2 = src.load()

    for j in range(dest.height) :
        for i in range(dest.width) :
            if px2[i, j] != 0:
                px1[i, j] = px2[i, j]

    return dest



def example1():
    for i in range(250+1):
        ifname = "stage1/inft {:04d}.png".format(i)
        sfname = "stage1/inft {:04d}.png".format(i + 251)
        ofname = "stage2/inft {:04d}.png".format(i)
        tfname = "test/inft {:04d}.png".format(i)

        sim = Image.open(sfname)
        sim = process_shadow(sim, 1)

        im = Image.open(ifname)
        im = draw_onto(sim, im)
        im.save(ofname)

        test_house_color(im)
        im.save(tfname)



def example2():
    dest = "."
    for fname in glob.glob("cmin/2/cmin*.png"):
        im = Image.open(fname)

        replace_color(im, range(200, 203+1), range(16, 31+1))
        replace_color(im, [8, 250], range(16, 31+1))
        test_house_color(im)

        _, ofname = os.path.split(fname)
        ofname = os.path.join(dest, ofname)
        print(fname, ofname)
        im.save(ofname)
