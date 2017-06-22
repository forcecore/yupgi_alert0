#!/usr/bin/python3
from PIL import Image, ImageDraw



if __name__ == "__main__" :
    rect_height = 112

    i = 0
    while rect_height > 0:
        frame = Image.open( "mbk 0000.png" )

        rect = (0, 0, 144, rect_height)

        # draw rect.
        draw = ImageDraw.Draw( frame )
        draw.rectangle( rect, fill=0 )


        frame.save( "mbkmake {:04d}.png".format( i ) )

        rect_height -= 4
        i += 1
