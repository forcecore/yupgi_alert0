#!/usr/bin/python3
from PIL import Image
import glob
import os


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

    def get_rgb( color ) :
        r = pal[ color * 3 ]
        g = pal[ color * 3 + 1 ]
        b = pal[ color * 3 + 2 ]
        return (r, g, b)

    def mse3( v1, v2 ) :
        s = 0
        for i in range( 3 ) :
            s += (v1[i] - v2[i])**2
        return s/3

    def calc_best_match( color, dest ) :
        rgb = get_rgb( color )
        #print( "input:", rgb )

        best = -1
        best_mse = float('inf')

        for d in range( dest[0], dest[1]+1 ) :
            rgb2 = get_rgb( d )
            mse = mse3( rgb, rgb2 )
            #print( "mse with", rgb2, "=", mse )
            if mse < best_mse :
                best_mse = mse
                best = d

        return best

    result = dict()
    for color in range( src[0], src[1]+1 ) :
        best_match = calc_best_match( color, dest )
        result[ color ] = best_match
    return result


def in_rect( x, y, rect ) :
    u, v, w, h = rect
    p = u + w
    q = v + h

    return u <= x and x < p and v <= y and y < q


def in_head_area( x, y ) :
    if in_rect( x, y, (21, 6, 6, 5) ) :
        return True
    return False


def in_body_area( x, y ) :
    if in_rect( x, y, (21, 18, 6, 11) ) :
        return True
    return False


def colorize( fname, ofname ) :
    im = Image.open( fname )
    px = im.load() # pixel access

    # map faction colors to black and white. I don't want player color,
    # except for small part.
    conv_map_grey = calc_color_conversion( im, (80, 95), (128, 143) )
    conv_map_fire = calc_color_conversion( im, (80, 95), (200, 207) )

    # access individual pixels
    for j in range( im.height ) :
        for i in range( im.width ) :
            if in_head_area( i, j ) :
                # leave head as player color
                continue
            elif in_body_area( i, j ) :
                # make area of player color body fire color
                if 80 <= px[i, j] and px[i, j] <= 95 :
                    px[i, j] = conv_map_fire[ px[i, j] ]
            else :
                # make rest of the player color grey.
                if 80 <= px[i, j] and px[i, j] <= 95 :
                    px[i, j] = conv_map_grey[ px[i, j] ]

    # Lets save.
    im.save( ofname )

if __name__ == "__main__" :
    # input directory name 12 means that the unit is facing 12 O'clock.
    # You group the images.
    # You specify what area to colorize by modifying
    # in_body_area, in_head_area function.
    for fname in glob.glob( "./ant1 0073.png" ) :
        _, ofname = os.path.split( fname )
        ofname = os.path.join( "tmp", ofname )
        colorize( fname, ofname )
        print( ofname )
