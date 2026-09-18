# mytetris.py
# Author: Ramesh Yerraballi
# Date: Spring 2026
# Built directly on neopixel library
# ----------
# Main entry point for the Tetris game on ubit with a 16x16 led matrix
# Controls:
#   move piece left or right by tilting ubit
#   A       – rotate piece 90° clockwise
#   B       – hard-drop (instantly fall to bottom)
#   Press both A and B to restart
#
# The game board is a 16-row × 16-column grid stored as a 2-D list of
# integers (0 = empty, 1 = locked/occupied).
from microbit import *
import neopixel
from random import randint
import radio

np = neopixel.NeoPixel(pin0, 256)

# This spos is only for tetris
# x and y are swapped and when you swap them x is backwards
def spos(x, y):  # for a serpentine raster
    x = 15-x
    if y & 0x1:  # is X odd
        pos = y * 16 + (16 - 1 - x)
    else:  # x is even
        pos = y * 16 + x
    return 255-pos

def DrawPixel(x, y, r=None, g=None, b=None):
    if r is None:
        r = randint(0, 60)
    if g is None:
        g = randint(0, 60)
    if b is None:
        b = randint(0, 60)
    np[spos(x, y)] = (r, g, b)

def ClearPixels():
    for pixel_id in range(0, len(np)):
        # Assign the current LED to 0
        np[pixel_id] = (0, 0, 0)

def selectPiece():
    pc = randint(1, 100) % 5
    return pc

def updateScore(x, score):
    score = score + x
    return score

def checkRowEmpty(rowno, sc):
    for i in range(16):
        if (sc[rowno][i] == 1):
            return 1   # found an occupied cell top of board is filled
    return 0
def checkRowFull(rowno, sc):
    # Scan every column in the row; if any cell is empty the row isn't full
    for i in range(16):
        if (sc[rowno][i] == 0):
            return 1
    for i in range(rowno - 1, -1, -1):
        for j in range(16):
            sc[i + 1][j] = sc[i][j]

    return 0

def displayBoard(sc, bl):
    # Board rows
    for i in range(16):
        for j in range(16):
            if (sc[i][j] == 0 and ([i, j] not in bl)):
                #print(i, j, end = '\n')
                DrawPixel(i, j, 0, 0, 0)
            else:
                #print(i, j, end = '\n')
                DrawPixel(i, j)
    np.show()
    return

def checkPiecePos(x, y, sc):
    # If the cell is outside the valid board area, treat it as blocked
    if (x > 15 or x < 0 or y < 0 or y > 15):
        return 1
    return sc[x][y]

def rotate(sc, bl):
    # Separate every cell's row and column index into two lists
    rs = []
    cs = []
    for i in bl:
        rs.append(i[0])
        cs.append(i[1])

    mnr = 20
    mnc = 20
    mxr = 0
    mxc = 0

    for i in rs:
        mnr = i if i < mnr else mnr
        mxr = i if mxr < i else mxr

    for i in cs:
        mnc = i if mnc > i else mnc   # update minimum column
        mxc = i if mxc < i else mxc   # update maximum column

    tmp = [[0 for x in range(mxc - mnc + 1)] for y in range(mxr - mnr + 1)]

    for i in bl:
        xc = i[0] - mnr
        yc = i[1] - mnc
        tmp[xc][yc] = 1

    nbl = list(zip(*tmp[::-1]))

    # Check whether any cell of the rotated piece would be blocked
    ch = 0
    for i in range(mxr - mnr + 1):
        for j in range(mxc - mnc + 1):
            if (nbl[j][i] == 1):
                ch = ch + checkPiecePos(mnr + j, mnc + i, sc)

    ret = []
    if (ch != 0):
        return ret

    for i in range(mxr - mnr + 1):
        for j in range(mxc - mnc + 1):
            if (nbl[j][i] == 1):
                ret.append([mnr + j, mnc + i])

    return ret

def moveRight(sc, bl):
    ch = 0
    # Check the cell to the right of every piece cell
    for p in bl:
        ch = ch + checkPiecePos(p[0], p[1] + 1, sc)

    if (ch == 0):  # all right-side neighbours are free
        for p in bl:
            p[1] = p[1] + 1   # shift each cell's column index right by 1

    return 0

def Down(sc, bl):
    ch = 0
    # Check the cell directly below each piece cell
    for p in bl:
        ch = ch + checkPiecePos(p[0] + 1, p[1], sc)

    if (ch != 0):
        for p in bl:
            sc[p[0]][p[1]] = 1
        return 1

    for p in bl:
        p[0] = p[0] + 1

    return 0

def moveLeft(sc, bl):
    ch = 0
    # Check the cell to the left of every piece cell
    for p in bl:
        ch = ch + checkPiecePos(p[0], p[1] - 1, sc)

    if (ch == 0):
        for p in bl:
            p[1] = p[1] - 1

    return 0

def draw(sc, bl):
    while (1):
        a = Down(sc, bl)
        if (a == 1):
            return 1


def gameInit():
    score = 0   # player's running score
    ClearPixels()
    np.show()
    return

blcs = [
    [[0, 0], [1, 0], [2, 0], [3, 0]],   # I-piece
    [[0, 0], [0, 1], [1, 1], [1, 2]],   # S-piece
    [[0, 0], [0, 1], [1, 0], [1, 1]],   # O-piece Square
    [[0, 1], [0, 2], [1, 0], [1, 1]],   # Z-piece
    [[0, 1], [1, 0], [1, 1], [1, 2]],   # T-piece
]
cmds = ['rite', 'rite', 'rite', 'left', 'left', 'left', 'left', 'rota', 'left', 'drop']
def build_ops(stay=0, left=0, rite=0, rota=0, drop=0) -> list:
    return (
        ['left'] * left +
        ['rite'] * rite +
        ['rota'] * rota +
        ['drop'] * drop
    )
ops = [
    build_ops(left=8, drop=1),   # I-piece
    build_ops(left=3, rite=1, rota=2, drop=1),   # S-piece
    build_ops(rite=8, drop=1),   # O-piece Square
    build_ops(left=1, rite=3, rota=2, drop=1),   # Z-piece
    build_ops(left=3, rite=3, rota=3, drop=1)    # T-piece
]
f = 0   # first-turn flag: skip the score update on the very first piece
sc = [[0 for x in range(16)] for y in range(16)]
score = 0
gameInit()
selfplay = True  # True
radio.on()

# Main game loop
while (1):
    # Award 10 points for each new piece (skip on first iteration)
    if (f == 0):
        gameInit()
        f = 1
        print('reset game')
        sc = [[0 for x in range(16)] for y in range(16)]
    else:
        score = updateScore(10, score)   # +10 per piece placed

    # Spawn a new piece
    bno = selectPiece()       # randomly pick a piece index 0–4
    bl = []
    bl = [cell[:] for cell in blcs[bno]]
    dropos = randint(2, 8) # column offset (keeps piece fully inside the 16-col board)
    for p in bl:
        p[1] += dropos     # translate each cell's column by the spawn offset
    incoming = "stay"
    st = 0
    while (st == 0):
        if (selfplay == True):
            play = randint(0,15)
            if play < len(ops[bno]):
                incoming = ops[bno][play]
        else: # Read any incoming messages.
            incoming = radio.receive()
        if incoming == "rite":
            moveRight(sc, bl)
        elif incoming == "left":
            moveLeft(sc, bl)
        elif incoming == "rstt":
            # both buttons are pressed: restart
            f = 0
            break
        elif incoming == "pause":
            sleep(2000)
            radio.send('resume')
        elif incoming == "drop":
            # B Pressed: hard-drop the piece straight to the bottom
            # draw() calls Down() repeatedly until the piece locks (returns 1)
            st = st + draw(sc, bl)
        elif incoming == "rota":
            # A Pressed: attempt a 90° clockwise rotation
            newc = rotate(sc, bl)
            if (len(newc) != 0):
                # Rotation succeeded – replace the piece with rotated coordinates
                bl = []
                bl = [cell[:] for cell in newc]
        else:
            # do nothing
            pass

        st = st + Down(sc, bl)
        # Re-render the board after every step
        if f == 1:
            displayBoard(sc, bl)
        else:
            break
        if (selfplay == True):
            sleep(200)
        else:
            sleep(300)

    # Post-lock checks

    # Check whether row 0 (the top of the board) is occupied game over
    if (checkRowEmpty(0, sc) == 1):
        f = 0
        continue
    if (f == 0):
        continue
    for p in bl:
        if (checkRowFull(p[0], sc) == 0):   # 0 means the row WAS full and got cleared
            score = updateScore(100, score)
