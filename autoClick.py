import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, queryMousePosition, W, moveMouseTo
import time

#debug method to read black blocks
def readBlack(Screen, Coordinates):
    for y in reversed(range(len(Screen))):
        for x in range(len(Screen[y])):
            if Screen[y][x] < 45:
                moveMouseTo(x + round(Coordinates[0]), y + round(Coordinates[1]))
                time.sleep(0.001)
    # moveMouseTo(x + round(Coordinates[0]), y + round(Coordinates[1]))
    # time.sleep(0.5)

#Clicks the first blackk pixel it finds
def clickBlack(Screen, Coordinates):
    for y in reversed(range(len(Screen))):
        for x in range(len(Screen[y])):
            if Screen[y][x] < 45:
                click(x + round(Coordinates[0]), y + round(Coordinates[1]))
                return

#trims columns to read just bits of the columns instead of the whole screen, boosting efficiency
def trimColums(coords):
    standardColumnLength = 1
    x1 = coords[0]
    halfBlock = blockLength/2
    x1 = x1 + halfBlock - round(standardColumnLength/2)
    x2 = x1 + round(standardColumnLength)
    coords[0] = x1
    coords[2] = x2
    return coords


#reads the screen and gets all the locations of the black blocks and sorts them from lower(in the screen) to highest
def getLowestBlack():
    highestPixel = 10000
    prevhighestPixel = 10000
    sortedBlacks = []
    indexBlacks = []
    columnBlacks = []
    finalOrder = []

    for i in list(range(4))[::+1]:
        x1 = gameCoords[0] + gameColumns[i][0]
        y1 = gameCoords[1]
        x2 = x1 + blockLength
        y2 = gameCoords[3]
        coordinates = [x1, y1, x2, y2]
        coordinates = trimColums(coordinates)
        screen = np.array(ImageGrab.grab(bbox=coordinates))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # readBlack(screen, coordinates)
        prevhighestPixel = highestPixel
        highestPixel = getHighestPixel(screen, coordinates)

        sortedBlacks.append(highestPixel)
        columnBlacks.append(i)
        indexBlacks.append(highestPixel)
        print("columns: " + str(i + 1) + " prevhighestPixel: " + str(prevhighestPixel) + " highestPixel: " + str(
            highestPixel))

        # greater than because the greater the pixel the lowest it's in the screen
    sortedBlacks.sort(reverse=True)

    for i in list(range(4))[::+1]:
        if sortedBlacks[i] != 10000:
            finalOrder.append(columnBlacks[indexBlacks.index(sortedBlacks[i])])
        else:
            finalOrder.append(-1)

    return finalOrder

#gets the highest black pixel(block) in each column
def getHighestPixel(Screen, Coordinates):
    highestPixel = 10000

    for y in range(len(Screen)):
        for x in range(len(Screen[y])):
            if Screen[y][x] < 45:
                # moveMouseTo(x + round(Coordinates[0]), y + round(Coordinates[1]))
                # time.sleep(1)
                highestPixel = y + round(Coordinates[1])
                return highestPixel
        # moveMouseTo(x + round(Coordinates[0]), y + round(Coordinates[1]))
        # time.sleep(0.001)
    return highestPixel


def processColumns(counter):
    columns = getLowestBlack()
    print("sortedColumns: " + str(columns))

    # if all columns return the value 10000 means there's no block in sight
    allNegative = columns.count(10000) == 4

    # if all columns return the value 0 means the whole screen is black and it's game over
    allZeros = columns.count(0) == 4

    if counter > 4:
        counter = 0

    if allNegative:
        print("------------------------------------WAITING FOR BLOCK TO COME DOWN-------------------------------------")
        return False

    if allZeros:
        print("------------------------------------STOP PROGRAM-------------------------------------")
        return True

    for i in list(range(4))[::+1]:

        if columns[i] == -1:
            print("Skip Column: " + str(columns[i]))
            continue
        else:
            print("Reading Column: " + str(columns[i]))

        x1 = gameCoords[0] + gameColumns[columns[i]][0]
        y1 = gameCoords[1]
        x2 = x1 + blockLength
        y2 = gameCoords[3]
        coordinates = [x1, y1, x2, y2]
        coordinates = trimColums(coordinates)
        screen = np.array(ImageGrab.grab(bbox=coordinates))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        clickBlack(screen, coordinates)


def Start():
    #The mouse cursor should be hovering over the game's start button.
    mousePos = queryMousePosition()
    click(mousePos.get("x"), mousePos.get("y"))
    time.sleep(0.1)

    start = time.time()
    time.clock()

    elapsed = 0
    stopProgram = False
    counter = 0
    while elapsed < 10:

        stopProgram = processColumns(counter)

        if stopProgram:
            break

        counter += 1
        elapsed = time.time() - start
        print("loop cycle time: %f, seconds count: %02d" % (time.clock(), elapsed))


# Coordinates used for OpenCV to analyze screen
gameCoords = [663, 42, 1260, 1025]
print(gameCoords)
gameLength = gameCoords[2] - gameCoords[0]
gameHeight = gameCoords[3] - gameCoords[1]

#Each black block 
blockLength = gameLength/4
blockHeight = gameHeight/4

#Columns corresponding to each block
column1 = [0, blockLength]
column2 = [column1[1], blockLength*2]
column3 = [column2[1], blockLength*3]
column4 = [column3[1], blockLength*4]

gameColumns = [column1, column2, column3, column4]
print(gameColumns)

Start()