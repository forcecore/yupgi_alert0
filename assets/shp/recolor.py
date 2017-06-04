#!/usr/bin/python3
from PIL import Image, ImageDraw
import glob
import os



def get_rgb( pal, color_index ) :
    r = pal[ color_index * 3 ]
    g = pal[ color_index * 3 + 1 ]
    b = pal[ color_index * 3 + 2 ]
    return (r, g, b)



def set_rgb( pal, color_index, rgb ) :
    pal[ color_index * 3 ], \
            pal[ color_index * 3 + 1 ], \
            pal[ color_index * 3 + 2 ] = rgb



def calc_color_conversion( im, src, dest ) :
    '''
    for each color in src, match the closest color in dest.
    src = (u, v) where u and v are color, given in palette index.
    dest = (p, q). Same as src.
    '''
    pal = im.getpalette()

    # serialized. just pack them in 3.
    # in RGB, not BGR, fortunately.
    #for i in range( len( pal ) ) :
    #    print( pal[ i ], end=" " )
    #    if i % 3 == 2 :
    #        print()

    def mse3( v1, v2 ) :
        s = 0
        for i in range( 3 ) :
            s += (v1[i] - v2[i])**2
        return s/3

    def calc_best_match( color, dest ) :
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

    result = dict()
    for color in src :
        best_match = calc_best_match( color, dest )
        result[ color ] = best_match
    return result



def replace_color(im, src, dest):
    mapper = calc_color_conversion( im, src, dest )

    # apply
    px = im.load() # pixel access
    for j in range( im.height ) :
        for i in range( im.width ) :
            if px[i, j] in src :
                px[i, j] = mapper[ px[i, j ] ]



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



if __name__ == "__main__" :
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
