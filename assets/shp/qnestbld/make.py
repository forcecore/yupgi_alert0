#!/usr/bin/python3
from PIL import Image

# open ant nest
nest = Image.open( "qnest 0000.png" )

ants = []
for i in range( 8 ) :
    antf = "a" + str( i ) + ".png"
    ant = Image.open( antf )

    # make color (0,0,0) transparent.
    ant = ant.convert( "RGBA" )
    data = ant.getdata()
    new_data = []
    for val in data :
        if val == ( 0, 0, 0, 255 ) :
            new_data.append( ( 0, 0, 0, 0 ) )
        else :
            new_data.append( val )
    ant.putdata( new_data )

    ants.append( ant )

frames = []

W, H = nest.size

y_offset = 0 # where ant will be
for i in range( 8*3 ) :
    # prepare canvas
    frame = Image.new( 'RGBA', nest.size, color=(0,0,0,255) )

    # paste nest image with opacity.
    mask = Image.new( 'L', nest.size, color=int(i/(8*3) * 255) )
    frame.paste( nest, mask=mask )

    # Paste ant at the center... but with qant descending.
    ant = ants[ i % len( ants ) ]

    x, y = ant.size
    cx = int( ( W - x ) / 2 )
    cy = int( ( H - y ) / 2 ) + int( y_offset )

    frame.paste( ant, (cx, cy), mask=ant )

    ofname = "qnestbld {:04d}.png".format( i )
    frame.save( ofname )

    y_offset += 0.5
