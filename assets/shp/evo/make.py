#!/usr/bin/python3
from PIL import Image, ImageDraw
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

        for d in dest :
            rgb2 = get_rgb( d )
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



def remove_house_color( im ) :
    px = im.load() # pixel access

    src = [ x for x in range( 80, 96 ) ] # house color is 80 -- 95.
    dest = [ x for x in range( 0, 256 ) ] # all colors
    for c in src :
        dest.remove( c )
    # remove house colors from dest.
    mapper = calc_color_conversion( im, src, dest )

    # apply
    for j in range( im.height ) :
        for i in range( im.width ) :
            if px[i, j] in src :
                px[i, j] = mapper[ px[i, j ] ]



def house_colorize( im ) :
    src = [ x for x in range( 0, 256 ) ] # all colors
    dest = [ x for x in range( 80, 96 ) ] # house color is 80 -- 95.
    src.remove( 0 ) # 0 is transparency.
    src.remove( 4 ) # 4 is shadow color.

    mapper = calc_color_conversion( im, src, dest )

    # apply
    px = im.load() # pixel access
    for j in range( im.height ) :
        for i in range( im.width ) :
            if in_rect( i, j, (46, 31, 13, 16) ) and px[i, j] in src :
                px[i, j] = mapper[ px[i, j ] ]
            elif in_rect( i, j, (8, 1, 23, 6) ) and px[i, j] in src :
                px[i, j] = mapper[ px[i, j ] ]



def bld_colorize( im ) :
    src = [ x for x in range( 0, 256 ) ] # all colors
    dest = [ x for x in range( 128, 144 ) ] # grey shades are in 128 -- 143.
    src.remove( 0 ) # 0 is transparency.
    src.remove( 4 ) # 4 is shadow color.

    mapper = calc_color_conversion( im, src, dest )

    # apply
    px = im.load() # pixel access
    for j in range( im.height ) :
        for i in range( im.width ) :
            if px[i, j] in src :
                px[i, j] = mapper[ px[i, j ] ]



if __name__ == "__main__" :
    #im = Image.open( "evobld 0000.png" )
    #bld_colorize( im )
    #house_colorize( im )
    #remove_house_color( im )
    #im.save( "tmp.png" )

    # max size of 0, 0, 43, 42, to cover left big rock.
    left_rect_height = 42 # /3 = 14 frames

    # max size of 46, 31, 13, 16.
    right_rect_height = 16 # /4 = 4 frames

    for i in range( 18 ) :
        frame = Image.open( "evomake.png" )

        rect1 = (0, 0, 44, left_rect_height+1)
        rect2 = (46, 31, 46+13+1, 31+left_rect_height+1)

        # draw rect.
        draw = ImageDraw.Draw( frame )
        draw.rectangle( rect1, fill=0 )
        draw.rectangle( rect2, fill=0 )

        if left_rect_height > 0 :
            left_rect_height -= 3
        if left_rect_height <= 0 :
            if right_rect_height > 0 :
                right_rect_height -= 4

        frame.save( "evomake {:04d}.png".format( i ) )
