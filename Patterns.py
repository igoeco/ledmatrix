# Tester for the ledmatrix library
# which uses the neopixel library
# Author: Ramesh Yerraballi
# Date: Spring 2026
import radio
from microbit import *
import ledmatrix
from random import randint

# Example usage (call one at a time):
# DrawSpiral()
# DrawSquare()
while True:
    ledmatrix.DrawPlot()
    #ledmatrix.DrawSpiral()
    #ledmatrix.DrawSquares()
    ledmatrix.np.show()

