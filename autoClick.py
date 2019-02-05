import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, holdClick, releaseClick, queryMousePosition, W, moveMouseTo
import time


# debug method to show the whole screen
def showScreen():
    screen = np.array(ImageGrab.grab(bbox=gameCoords))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    cv2.imshow('screen', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# debug method to show screen
def showScreenWithCoordinates(coordinates):
    screen = np.array(ImageGrab.grab(bbox=coordinates))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    cv2.imshow('screen', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# debug method to read black blocks
def readBlack(Screen, Coordinates):
    for y in reversed(range(len(Screen))):
        for x in range(len(Screen[y])):
            if Screen[y][x] < 45:
                moveMouseTo(x + round(Coordinates[0]), y + round(Coordinates[1]))
                time.sleep(0.001)
            # print(Screen[y][x])
            # moveMouseTo(x + round(Coordinates[0]), y + round(Coordinates[1]))
            # time.sleep(0.001)

# Clicks the first black pixel it finds
def clickBlack(Screen, Coordinates, Column):
    for y in reversed(range(len(Screen))):
        for x in range(len(Screen[y])):
            if Screen[y][x] < 45:
                releaseClick()
                holdClick(x + round(Coordinates[0]), y + round(Coordinates[1]))
                return

# trims columns to read just bits of the columns instead of the whole screen, boosting efficiency
def trimColums(coords):
    standardColumnLength = 1
    x1 = coords[0]
    halfBlock = blockLength/2
    x1 = x1 + round(halfBlock) - round(standardColumnLength / 2)
    x2 = x1 + round(standardColumnLength)
    coords[0] = x1
    coords[2] = x2
    return coords

# reads the screen and gets all the locations of the black blocks and sorts them from lower(in the screen) to highest
def getLowestBlack(counter):
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
        # cv2.imshow('screen', screen)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # readBlack(screen, coordinates)
        prevhighestPixel = highestPixel
        blocks = getHighestPixel(screen, coordinates)

        # if blocks.__len__() > 2:
        #     cv2.imwrite(str(i) + "_column" + str(i) + ".jpg",
        #                 cv2.cvtColor(np.array(ImageGrab.grab(bbox=gameCoords)), cv2.COLOR_BGR2GRAY))

        for index in range(len(blocks)):
            sortedBlacks.append(blocks[index])
            columnBlacks.append(i)
            indexBlacks.append(blocks[index])
            print("columns: " + str(i + 1) + " prevhighestPixel: " + str(prevhighestPixel) + " highestPixel: " + str(
                blocks[index]))

    sortedBlacks.sort(reverse=True)

    for i in range(len(sortedBlacks)):
        if sortedBlacks[i] != 10000:
            finalOrder.append(columnBlacks[indexBlacks.index(sortedBlacks[i])])
        else:
            finalOrder.append(-1)

    finalOrder = cleanOrder(finalOrder)

    return finalOrder

# The game can have two black blocks on the same column so we want to remove the second block from our ordered list
def cleanOrder(columns):
    prevColumn = -1
    currentColumn = -1
    popCount = 0
    for i in range(len(columns)):
        i = i - popCount
        currentColumn = columns[i]
        if currentColumn == prevColumn:
            columns.pop(i)
            popCount += 1
        else:
            prevColumn = currentColumn
    return columns


# gets the highest black pixel(block) in each column
def getHighestPixel(Screen, Coordinates):
    blocks = []
    highestPixel = 10000
    lastHigh = 10000
    currHigh = 10000
    switch = True
    prevHighestPixel = -10000

    for y in range(len(Screen)):
        for x in range(len(Screen[y])):
            if Screen[y][x] < 45:

                if not switch:
                    break

                # moveMouseTo(x + round(Coordinates[0]), y + round(Coordinates[1]))
                # time.sleep(1)
                highestPixel = y + round(Coordinates[1])

                if switch:

                    if highestPixel > (prevHighestPixel + blockHeight):
                        blocks.append(highestPixel)
                        switch = False
                        prevHighestPixel = highestPixel
            else:
                # print(Screen[y][x])
                switch = True

        # moveMouseTo(x + round(Coordinates[0]), y + round(Coordinates[1]))
        # time.sleep(0.001)
    return blocks


def processColumns(counter):
    columns = getLowestBlack(counter)
    print("sortedColumns: " + str(columns))

    if columns.__len__() > 7:
        print("------------------------------------STOP PROGRAM-------------------------------------")
        return True

    for i in range(len(columns)):

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
        # print(coordinates)
        screen = np.array(ImageGrab.grab(bbox=coordinates))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite(str(counter) + "_column" + str(i) + "_screen.jpg", screen)
        # cv2.imwrite(str(counter) + "_column" + str(i) + ".jpg", cv2.cvtColor(np.array(ImageGrab.grab(bbox=gameCoords)), cv2.COLOR_BGR2GRAY))
        # cv2.imshow('screen', screen)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # readBlack(screen, coordinates)
        clickBlack(screen, coordinates, columns[i])


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
    while elapsed < 600:

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

# Each black block 
blockLength = gameLength/4
blockHeight = gameHeight/4

# Columns corresponding to each block
column1 = [0, blockLength]
column2 = [column1[1], blockLength*2]
column3 = [column2[1], blockLength*3]
column4 = [column3[1], blockLength*4]

gameColumns = [column1, column2, column3, column4]
print(gameColumns)

Start()
# showScreen()
