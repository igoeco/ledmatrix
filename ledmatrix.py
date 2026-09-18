# microbit-module: ledmatrix@1.0.0
# Author: Ramesh Yerraballi
# Date: Spring 2026
"""
Note: Make sure and upload this file to the microbit everytime a
change is made

    16x16 LED Matrix library
"""
from microbit import *
import neopixel
from random import randint

np = neopixel.NeoPixel(pin0,256)

# 5x8 Bitmap Font - All printable ASCII characters (0x20 to 0x7E)
# Each character is 5 bytes, one byte per column (left to right)
# Within each byte: bit7 = top row, bit0 = bottom row

Font = [
    # Encoding notes:
    # Row layout (bit position): 7=top, 0=bottom
    # Column layout: index 0 = leftmost, index 4 = rightmost

    0x00, 0x00, 0x00, 0x00, 0x00,  # 0x20 SPACE
    0x00, 0x00, 0xBE, 0x00, 0x00,  # 0x21 !
    0x00, 0xE0, 0x00, 0xE0, 0x00,  # 0x22 "
    0x28, 0xFE, 0x28, 0xFE, 0x28,  # 0x23 #
    0x4C, 0x92, 0xFF, 0x92, 0x64,  # 0x24 $
    0xC6, 0xC8, 0x10, 0x26, 0xC6,  # 0x25 %
    0x6C, 0x92, 0xAA, 0x44, 0x0A,  # 0x26 &
    0x00, 0x00, 0xE0, 0x00, 0x00,  # 0x27 '
    0x00, 0x38, 0x44, 0x82, 0x00,  # 0x28 (
    0x00, 0x82, 0x44, 0x38, 0x00,  # 0x29 )
    0x28, 0x10, 0x7C, 0x10, 0x28,  # 0x2A *
    0x10, 0x10, 0x7C, 0x10, 0x10,  # 0x2B +
    0x00, 0x00, 0x06, 0x04, 0x00,  # 0x2C ,
    0x10, 0x10, 0x10, 0x10, 0x10,  # 0x2D -
    0x00, 0x00, 0x06, 0x06, 0x00,  # 0x2E .
    0x02, 0x04, 0x08, 0x10, 0x20,  # 0x2F /

    0x7C, 0x8A, 0x92, 0xA2, 0x7C,  # 0x30 0
    0x00, 0x42, 0xFE, 0x02, 0x00,  # 0x31 1
    0x46, 0x8A, 0x92, 0x92, 0x62,  # 0x32 2
    0x84, 0x82, 0x92, 0xB2, 0xCC,  # 0x33 3
    0x18, 0x28, 0x48, 0xFE, 0x08,  # 0x34 4
    0xE4, 0xA2, 0xA2, 0xA2, 0x9C,  # 0x35 5
    0x3C, 0x52, 0x92, 0x92, 0x0C,  # 0x36 6
    0x80, 0x8E, 0x90, 0xA0, 0xC0,  # 0x37 7
    0x6C, 0x92, 0x92, 0x92, 0x6C,  # 0x38 8
    0x60, 0x92, 0x92, 0x94, 0x78,  # 0x39 9

    0x00, 0x00, 0x36, 0x36, 0x00,  # 0x3A :
    0x00, 0x02, 0x36, 0x34, 0x00,  # 0x3B ;
    0x00, 0x10, 0x28, 0x44, 0x82,  # 0x3C <
    0x28, 0x28, 0x28, 0x28, 0x28,  # 0x3D =
    0x82, 0x44, 0x28, 0x10, 0x00,  # 0x3E >
    0x40, 0x80, 0x9A, 0x90, 0x60,  # 0x3F ?
    0x4C, 0x92, 0xBE, 0x82, 0x7C,  # 0x40 @

    0x3E, 0x48, 0x88, 0x48, 0x3E,  # 0x41 A
    0xFE, 0x92, 0x92, 0x92, 0x6C,  # 0x42 B
    0x7C, 0x82, 0x82, 0x82, 0x44,  # 0x43 C
    0xFE, 0x82, 0x82, 0x82, 0x7C,  # 0x44 D
    0xFE, 0x92, 0x92, 0x92, 0x82,  # 0x45 E
    0xFE, 0x90, 0x90, 0x90, 0x80,  # 0x46 F
    0x7C, 0x82, 0x82, 0x8A, 0xCE,  # 0x47 G
    0xFE, 0x10, 0x10, 0x10, 0xFE,  # 0x48 H
    0x00, 0x82, 0xFE, 0x82, 0x00,  # 0x49 I
    0x04, 0x02, 0x82, 0xFC, 0x80,  # 0x4A J
    0xFE, 0x10, 0x28, 0x44, 0x82,  # 0x4B K
    0xFE, 0x02, 0x02, 0x02, 0x02,  # 0x4C L
    0xFE, 0x40, 0x38, 0x40, 0xFE,  # 0x4D M
    0xFE, 0x20, 0x10, 0x08, 0xFE,  # 0x4E N
    0x7C, 0x82, 0x82, 0x82, 0x7C,  # 0x4F O
    0xFE, 0x90, 0x90, 0x90, 0x60,  # 0x50 P
    0x7C, 0x82, 0x8A, 0x84, 0x7A,  # 0x51 Q
    0xFE, 0x90, 0x98, 0x94, 0x62,  # 0x52 R
    0x64, 0x92, 0x92, 0x92, 0x4C,  # 0x53 S
    0xC0, 0x80, 0xFE, 0x80, 0xC0,  # 0x54 T
    0xFC, 0x02, 0x02, 0x02, 0xFC,  # 0x55 U
    0xF8, 0x04, 0x02, 0x04, 0xF8,  # 0x56 V
    0xFC, 0x02, 0x1C, 0x02, 0xFC,  # 0x57 W
    0xC6, 0x28, 0x10, 0x28, 0xC6,  # 0x58 X
    0xC0, 0x20, 0x1E, 0x20, 0xC0,  # 0x59 Y
    0x86, 0x9A, 0x92, 0xB2, 0xC2,  # 0x5A Z

    0x00, 0xFE, 0x82, 0x82, 0x00,  # 0x5B [
    0x20, 0x10, 0x08, 0x04, 0x02,  # 0x5C backslash
    0x00, 0x82, 0x82, 0xFE, 0x00,  # 0x5D ]
    0x20, 0x40, 0x80, 0x40, 0x20,  # 0x5E ^
    0x01, 0x01, 0x01, 0x01, 0x01,  # 0x5F _
    0x00, 0x80, 0x40, 0x20, 0x00,  # 0x60 `

    0x04, 0x2A, 0x2A, 0x2A, 0x1E,  # 0x61 a
    0xFE, 0x12, 0x22, 0x22, 0x1C,  # 0x62 b
    0x1C, 0x22, 0x22, 0x22, 0x14,  # 0x63 c
    0x1C, 0x22, 0x22, 0x12, 0xFE,  # 0x64 d
    0x1C, 0x2A, 0x2A, 0x2A, 0x18,  # 0x65 e
    0x10, 0x7E, 0x90, 0x80, 0x40,  # 0x66 f
    0x18, 0x25, 0x25, 0x25, 0x3E,  # 0x67 g
    0xFE, 0x10, 0x10, 0x10, 0x0E,  # 0x68 h
    0x00, 0x12, 0x5E, 0x02, 0x00,  # 0x69 i
    0x04, 0x02, 0x22, 0xBC, 0x00,  # 0x6A j
    0xFE, 0x08, 0x14, 0x22, 0x00,  # 0x6B k
    0x00, 0x82, 0xFE, 0x02, 0x00,  # 0x6C l
    0x3E, 0x20, 0x18, 0x20, 0x3E,  # 0x6D m
    0x3E, 0x20, 0x20, 0x20, 0x1E,  # 0x6E n
    0x1C, 0x22, 0x22, 0x22, 0x1C,  # 0x6F o
    0x3F, 0x28, 0x28, 0x28, 0x10,  # 0x70 p
    0x10, 0x28, 0x28, 0x28, 0x3F,  # 0x71 q
    0x3E, 0x10, 0x20, 0x20, 0x10,  # 0x72 r
    0x12, 0x2A, 0x2A, 0x2A, 0x04,  # 0x73 s
    0x20, 0xFC, 0x22, 0x02, 0x04,  # 0x74 t
    0x3C, 0x02, 0x02, 0x04, 0x3E,  # 0x75 u
    0x38, 0x04, 0x02, 0x04, 0x38,  # 0x76 v
    0x3C, 0x02, 0x0C, 0x02, 0x3C,  # 0x77 w
    0x22, 0x14, 0x08, 0x14, 0x22,  # 0x78 x
    0x39, 0x05, 0x05, 0x05, 0x3E,  # 0x79 y
    0x22, 0x26, 0x2A, 0x32, 0x22,  # 0x7A z

    0x00, 0x10, 0x6C, 0x82, 0x00,  # 0x7B {
    0x00, 0x00, 0xFE, 0x00, 0x00,  # 0x7C |
    0x00, 0x82, 0x6C, 0x10, 0x00,  # 0x7D }
    0x20, 0x40, 0x30, 0x10, 0x20,  # 0x7E ~
#   Special patterns mapped here:
    0x18, 0x44, 0x04, 0x44, 0x18,  # 8 \b smile
    0x38, 0x44, 0x22, 0x44, 0x38,  # 9 \t heart
    0x18, 0x18, 0x00, 0x18, 0x18,  # 10 \l eyes
    0x18, 0x18, 0x00, 0x18, 0x18,  # 11 \v eyes
#    0x20, 0x40, 0x30, 0x10, 0x20,  # 12 \f
]

def DrawPixel(x, y, r=None,g=None,b=None):
    if r is None:
        r = randint(0, 255)
    if g is None:
        g = randint(0, 255)
    if b is None:
        b = randint(0, 255)
    np[spos(x, y)] = (r, g, b)

def DrawChar(x, y, ch, r=None,g=None,b=None):
    special = 0
    if ch in ['\b', '\t', '\l', '\v', '\f']:
        c = ord('~') - 32 + ord(ch) - 7
        special = 1
    else:
        c = ord(ch) - 32 # ord('A')
    for i in range(0, 6):
        if (i == 5) :
            line = 0x0
        else :
            line = Font[(c*5)+i]
        for j in range(0,8):
            if (line & 0x1) :
                if special == 0:
                    DrawPixel(x+i, y+j, r,g,b)
                else:
                    DrawPixel(x+i, y+j)
            else :
                DrawPixel(x+i, y+j, 0,0,0)
            line >>= 1
def spos(x, y):  # for a serpentine raster
    if x & 0x1:  # is X odd
        pos = x * 16 + (16 - 1 - y)
    else:  # x is even
        pos = x * 16 + y
    return 255-pos

def DrawVLine(x,y,w,r=None,g=None,b=None):
    for i in range(y,y+w):
        DrawPixel(x,i,r, g, b)


def DrawHLine(x,y,w,r=None,g=None,b=None):
    for i in range(x,x+w):
        DrawPixel(i,y,r, g, b)


def DrawRectangle(x,y,w,h,r=None,g=None,b=None):
    for i in range(0, w):
        for j in range (0, h):
                DrawPixel(x+i, y+j, r,g,b)

def DrawUnfilledRectangle(x,y,w,h,r=None,g=None,b=None):
    DrawVLine(x,y,h,r,g,b)
    DrawHLine(x,y,w,r,g,b)
    DrawVLine(x+w,y,h,r,g,b)
    DrawHLine(x,y+h,w+1,r,g,b)

def DrawBitmap(image, x=0, y=0, w=16, h=16):
    for i in range (0, w):
        for j in range (0, h):
            r = (image[j*16+i] & 0x1F)
            g = ((image[j*16+i] & 0x3E0)>> 5)
            b = ((image[j*16+i] & 0xF800)>> 11)
            DrawPixel(x+i,y+j,r,g,b)

def ClearPixels():
    for pixel_id in range(0, len(np)):
        # Assign the current LED to 0
        np[pixel_id] = (0, 0, 0)

def RandomPixels(pixpercent=100, brightness=100):
    for pixel_id in range(0, len(np)):
        # Assign the current LED to 0
        np[pixel_id] = (0,0,0) if randint(0,100) >= pixpercent else (randint(0, int(brightness*255/100)), randint(0, int(brightness*255/100)), randint(0, int(brightness*255/100)))

def DrawRainbow():
    DrawHLine(0, 0, 16, r=60, g=0, b=0) # Red
    DrawHLine(0, 1, 16, r=60, g=0, b=0) # Red
    DrawHLine(0, 2, 16, r=60, g=0, b=0) # Red
    DrawHLine(0, 3, 16, r=60, g=30, b=0) # Orange
    DrawHLine(0, 4, 16, r=60, g=30, b=0) # Orange
    DrawHLine(0, 5, 16, r=60, g=60, b=0) # Yellow
    DrawHLine(0, 6, 16, r=60, g=60, b=0) # Yellow
    DrawHLine(0, 7, 16, r=30, g=60, b=0) # Green
    DrawHLine(0, 8, 16, r=30, g=60, b=0) # Green
    DrawHLine(0, 9, 16, r=0, g=0, b=60) # Blue
    DrawHLine(0, 10, 16, r=0, g=0, b=60) # Blue
    DrawHLine(0, 11, 16, r=5, g=0, b=30) # Indigo
    DrawHLine(0, 12, 16, r=5, g=0, b=30) # Indigo
    DrawHLine(0, 13, 16, r=35, g=0, b=52) # Violet
    DrawHLine(0, 14, 16, r=35, g=0, b=52) # Violet
    DrawHLine(0, 15, 16, r=35, g=0, b=52) # Violet

def Say(what, lo=None, hr=100, hg=0, hb=100, lr=0, lg=100, lb=0):
    # if lo='' then  what has all 6 letters
    #  otherwise what has 3 and lo has 3
    #if what == '======':
    #    DrawRainbow()
    #    return
    DrawChar(0,8,what[0],hr,hg,hb)
    DrawChar(5,8,what[1],hr,hg,hb)
    DrawChar(10,8,what[2],hr,hg,hb)
    if lo==None:
        DrawChar(0,0,what[3],lr,lg,lb)
        DrawChar(5,0,what[4],lr,lg,lb)
        DrawChar(10,0,what[5],lr,lg,lb)
    else:
        DrawChar(0,0,lo[0],lr,lg,lb)
        DrawChar(5,0,lo[1],lr,lg,lb)
        DrawChar(10,0,lo[2],lr,lg,lb)

def DrawPlot():
    """Simulate a random histogram with 16 columns that rise and fall"""
    # Initialize column heights
    heights = [0] * 16

    while True:
        # Update each column randomly
        for col in range(16):
            # Random change: -1, 0, or +1
            change = randint(-1, 1)
            new_height = heights[col] + change

            # Clamp height between 0 and 16
            new_height = max(0, min(16, new_height))

            # Random color for this column
            r, g, b = randint(50, 255), randint(50, 255), randint(50, 255)

            # If height increased, draw new pixels
            if new_height > heights[col]:
                for row in range(heights[col], new_height):
                    DrawPixel(col, row, r, g, b)
                    np.show()
                    sleep(50)

            # If height decreased, clear pixels
            elif new_height < heights[col]:
                for row in range(new_height, heights[col]):
                    DrawPixel(col, row, 0, 0, 0)
                    np.show()
                    sleep(50)

            heights[col] = new_height

        sleep(50)  # Update rate

def DrawSpiral():
    """Draw a spiral from center outward, then clear inward, repeat"""
    while True:
        # Store the order of pixels for unwinding
        pixel_order = []

        # Start from center
        x, y = 7, 7  # Center of 16x16 grid (0-indexed, so 7,7 is center-left)
        # Actually center is between pixels, so let's use 8,8 as starting point
        x, y = 8, 8

        # Direction: right, down, left, up
        dx, dy = 1, 0
        steps_in_direction = 1
        steps_taken = 0
        direction_changes = 0

        # Draw spiral outward
        while len(pixel_order) < 256:  # 16x16 = 256 pixels
            if 0 <= x < 16 and 0 <= y < 16:
                DrawPixel(x, y, randint(0, 255), randint(0, 255), randint(0, 255))
                pixel_order.append((x, y))
                np.show()
                sleep(50)

            x += dx
            y += dy
            steps_taken += 1

            # Check if we need to turn
            if steps_taken == steps_in_direction:
                steps_taken = 0
                direction_changes += 1

                # Turn 90 degrees clockwise: right->down->left->up->right
                if dx == 1 and dy == 0:  # right -> down
                    dx, dy = 0, 1
                elif dx == 0 and dy == 1:  # down -> left
                    dx, dy = -1, 0
                elif dx == -1 and dy == 0:  # left -> up
                    dx, dy = 0, -1
                elif dx == 0 and dy == -1:  # up -> right
                    dx, dy = 1, 0

                # Increase steps every 2 direction changes
                if direction_changes % 2 == 0:
                    steps_in_direction += 1

        sleep(50)

        # Clear spiral inward (reverse order)
        for x, y in reversed(pixel_order):
            DrawPixel(x, y, 0, 0, 0)
            np.show()
            sleep(50)
        break
        sleep(50)

def DrawSquares():
    """Draw concentric squares from center outward, then clear inward, repeat"""
    while True:
        # Random color for this sequence
        r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)

        # Store squares for clearing in reverse
        all_pixels = []

        # Draw squares from center (size 0) to edge (size 8)
        for size in range(9):  # 0 to 8
            square_pixels = []
            cx, cy = 7, 7  # Center point (between pixels 7 and 8)

            # Calculate square boundaries
            x1 = cx - size
            y1 = cy - size
            x2 = cx + size + 1
            y2 = cy + size + 1

            # Clamp to grid boundaries
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(16, x2)
            y2 = min(16, y2)

            # Draw top edge
            for x in range(x1, x2):
                if y1 < 16:
                    DrawPixel(x, y1, r, g, b)
                    square_pixels.append((x, y1))
                    np.show()

            # Draw bottom edge
            for x in range(x1, x2):
                if y2 - 1 >= 0 and y2 - 1 != y1:
                    DrawPixel(x, y2 - 1, r, g, b)
                    square_pixels.append((x, y2 - 1))
                    np.show()

            # Draw left edge (excluding corners already drawn)
            for y in range(y1 + 1, y2 - 1):
                if x1 < 16:
                    DrawPixel(x1, y, r, g, b)
                    square_pixels.append((x1, y))
                    np.show()

            # Draw right edge (excluding corners already drawn)
            for y in range(y1 + 1, y2 - 1):
                if x2 - 1 >= 0 and x2 - 1 != x1:
                    DrawPixel(x2 - 1, y, r, g, b)
                    square_pixels.append((x2 - 1, y))
                    np.show()

            all_pixels.append(square_pixels)
            sleep(50)

        sleep(50)

        # Clear squares inward (reverse order)
        for square_pixels in reversed(all_pixels):
            for x, y in square_pixels:
                DrawPixel(x, y, 0, 0, 0)
                np.show()
                sleep(50)

        sleep(50)
