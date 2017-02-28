from gimpfu import *

def calc_color_conversion( im, src, dest ) :
    '''
    for each color in src, match the closest color in dest.
    src = (u, v) where u and v are color, given in palette index.
    dest = (p, q). Same as src.
    '''
    pal = pdb.gimp_image_get_colormap(im)
    (cnt, pal) = pal
    assert cnt == 3*256

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



def remove_house_color( img ) :
    pdb.gimp_image_undo_group_start(img)
    drawable = pdb.gimp_image_get_active_drawable(img)
    if not drawable :
        print( "No active drawable (layers, etc)" )

    is_selected, x1, y1, x2, y2 = pdb.gimp_selection_bounds(img)
    if not is_selected :
        print( "Nothing selected" )
        return

    src = [ x for x in range( 80, 96 ) ] # house color is 80 -- 95.
    dest = [ x for x in range( 0, 256 ) ] # all colors
    for c in src :
        dest.remove( c )
    # remove house colors from dest.
    mapper = calc_color_conversion( img, src, dest )

    # apply for selected.
    for j in range( y1, y2+1 ) :
        for i in range( x1, x2+1 ) :
            num_channels, pixel = pdb.gimp_drawable_get_pixel( drawable, i, j )
            assert len( pixel ) == 1
            px = pixel[ 0 ]
            if px in src :
                px = mapper[ px ]
                pdb.gimp_drawable_set_pixel(drawable, i, j, num_channels, (px,))

    # put the result back to gimp
    pdb.gimp_drawable_update(drawable, x1, y1, x2, y2) # update UI.
    pdb.gimp_image_undo_group_end(img)
    pdb.gimp_displays_flush() # Not sure what this does.



def house_colorize( img ) :
    pdb.gimp_image_undo_group_start(img)
    drawable = pdb.gimp_image_get_active_drawable(img)
    if not drawable :
        print( "No active drawable (layers, etc)" )

    is_selected, x1, y1, x2, y2 = pdb.gimp_selection_bounds(img)
    if not is_selected :
        print( "Nothing selected" )
        return

    src = [ x for x in range( 0, 256 ) ] # all colors
    dest = [ x for x in range( 80, 96 ) ] # house color is 80 -- 95.
    src.remove( 0 ) # 0 is transparency.
    src.remove( 4 ) # 4 is shadow color.

    mapper = calc_color_conversion( img, src, dest )

    # apply for selected.
    for j in range( y1, y2 ) :
        for i in range( x1, x2 ) :
            num_channels, pixel = pdb.gimp_drawable_get_pixel( drawable, i, j )
            assert len( pixel ) == 1
            px = pixel[ 0 ]
            if px in src :
                px = mapper[ px ]
                pdb.gimp_drawable_set_pixel(drawable, i, j, num_channels, (px,))

    # put the result back to gimp
    pdb.gimp_drawable_update(drawable, x1, y1, x2, y2) # update UI.
    pdb.gimp_image_undo_group_end(img)
    pdb.gimp_displays_flush() # Not sure what this does.



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

###
###
###
# How to use this thing.
# Place this script in Python\Lib of gimp or something:
# C:\Program Files\GIMP 2\Python\Lib
# (on windows.)
# C:\Program Files\GIMP 2\Python\Lib\shp.py (I soft linked it as shp.py)
#
# Run pythonfu console in gimp.
# You can import by typing
# "import shp".
# into the console.
# If you modify the script. you can
# "reload(shp)" to make python reload the script.
#
# To work on images:
# "imgs = gimp.image_list()"
# type just "imgs" to the console (or type "print(imgs)") to see what you are working on.
# img = imgs[ 0 ] # select one.
#
# If you need more gimp supported functions, click browse and search.
# To use stuff there, such as
# gimp-context-get-foreground
# you need to change - to _ and prefix it with pdb:
# pdb.gimp_context_get_foreground(...)
# Easy way: just double click on the browser. DANG.
#
# Well, enough explanation.
