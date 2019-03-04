#SR4.py
#Por Luis Diego Fernandez
#v-1.20.20objMaker

import sys
import math
import struct
import bmp_maker

# image attributes
width = 600
height = 600
x_to_paint = 1
y_to_paint = 1
bits_per_pixel = 32

print("BMP image maker")

# prepare image
newBmpImage = bmp_maker.bmpImage()
newBmpImage.glCreateWindow(width, height)
newBmpImage.glViewPort(x_to_paint,y_to_paint,200,200)
newBmpImage.glClearColor(0,0,0)
newBmpImage.glClear()

# render object
newBmpImage.glObjReader('deer',2000,0.5,0)

# create image file
newBmpImage.glFinish()

print("\nDone")
