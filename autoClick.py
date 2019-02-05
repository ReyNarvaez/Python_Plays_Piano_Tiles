import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, holdClick, holdClickV2, releaseClick, queryMousePosition, W, moveMouseTo
import time
import keyboard


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


# Debug method to read specific column to print each pixel value. To define Min/Max black identifiers
def readColumn(column):
    x1 = gameCoords[0] + gameBlocks[column]
    y1 = gameCoords[1]
    x2 = x1 + blockLength
    y2 = gameCoords[3]
    coordinates = [x1, y1, x2, y2]
    coordinates = trimColums(coordinates)
    screen = np.array(ImageGrab.grab(bbox=coordinates))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    # 69
    for y in reversed(range(len(screen))):
        if isBlack(screen[y][0]):
            print("value: " + str(screen[y][0]) + " Is Black")
        else:
            print("value: " + str(screen[y][0]))
        moveMouseTo(x1, y + round(coordinates[1]))
        time.sleep(0.1)


# Method to identify if a block/pixel is black
def isBlack(value):
    return blackMinIdentifier <= value <= blackMaxIdentifier


# Reads the column from bottom to top until it finds the first black pixel and clicks it
def clickBlock(X, Column):

    x1 = gameCoords[0] + gameBlocks[Column]
    y1 = gameCoords[1]
    x2 = x1 + blockLength
    y2 = gameCoords[3]
    coordinates = [x1, y1, x2, y2]
    coordinates = trimColums(coordinates)
    screen = np.array(ImageGrab.grab(bbox=coordinates))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # cv2.imwrite("testImages/column" + str(X) + ".jpg", screen)

    for y in reversed(range(len(screen))):
        if isBlack(screen[y][0]):
            releaseClick()
            holdClickV2()
            # time.sleep(1)
            return
        moveMouseTo(X, y + round(coordinates[1]))
        # time.sleep(0.1)


# Since we already now where's the black pixel, move the mouse to that location and click it
def clickBlockV2(X):
    moveMouseTo(X, heightOffset)
    releaseClick()
    holdClickV2()


# Method that verifies if we should click the block and if so, it triggers the click method
def shouldClick(Screen, X, Column, counter):
    print("checkscreen")
    global startCounter
    for i in range(lineHeight):
        print("value:" + str(Screen[i][X]))
        if isBlack(Screen[i][X]):
            if counter == 0:
                startCounter += 1
                # Game reads and find the first black block to click before pressing start
                pressStart()
            # clickBlock(X + gameCoords[0], Column)
            clickBlockV2(X + gameCoords[0])
            # moveMouseTo(X + gameCoords[0], lineCoords[1])
            # time.sleep(0.001)
            return True
    # moveMouseTo(X + gameCoords[0], lineCoords[1])
    # time.sleep(0.001)
    return False


# Method to define what to do when it shouldn't click a block
def dontClick(i, counter):
    print("block " + str(i) + " shouldClick: FALSE")


# Method that reads the line with it's corresponding coordinates
def readLine(counter):

    # If the game reads the first line and it doesn't finds a black block in the line coordinates it presses start
    if counter == 1 and startCounter == 0:
        pressStart()

    screen = np.array(ImageGrab.grab(bbox=lineCoords))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    global lastBlockClicked

    print("===================================ITERATION:" + str(counter) + "===================================")
    for i in range(len(gameBlocks)):
        if lastBlockClicked != i:
            if shouldClick(screen, gameBlocks[i], i, counter):
                lastBlockClicked = i
                print("block " + str(i) + " shouldClick: TRUE")
                return False
            else:
                dontClick(i, counter)
        else:
            dontClick(i, counter)

    return False


# Kill switch to end the program
def isKillSwitch():
    if keyboard.is_pressed('k'):  # if key 'k' is pressed
        print('*****************************************KILL SWITCH*****************************************')
        return True


# Method that presses the start button
def pressStart():
    mousePos = queryMousePosition()
    click(mousePos.get("x"), mousePos.get("y"))
    time.sleep(0.2)

# Method to get the game coordinates via user clicks
def getGameCoordinates():

    image = cv2.imread("test.jpg")

    if image is None:
        cv2.imwrite("fullScreen.jpg", np.array(ImageGrab.grab()))
        image = cv2.imread("fullScreen.jpg")
        clone = image.copy()
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", recordCoordinates)

        while True:
            # display the image and wait for a keypress
            cv2.imshow("image", image)
            key = cv2.waitKey(1) & 0xFF

            if gameCoordsRecorded:
                break

        # close all open windows
        cv2.destroyAllWindows()

coords = []
image = None
gameCoordsRecorded = False

# Method to record coordinates on click
def recordCoordinates(event, x, y, flags, param):
    # grab references to the global variables
    global coords
    global image

    # if the left mouse button was clicked, record the starting (x, y) coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append(x)
        coords.append(y)

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        coords.append(x)
        coords.append(y)

        screen = np.array(ImageGrab.grab(bbox=coords))
        cv2.imshow('screen', screen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# Start the process
def start():

    start = time.time()
    time.clock()

    elapsed = 0
    stopProgram = False
    counter = 0

    while elapsed < 10000:

        if isKillSwitch():
            break

        stopProgram = readLine(counter)

        if stopProgram:
            break

        counter += 1
        elapsed = time.time() - start
        # print("loop cycle time: %f, seconds count: %02d" % (time.clock(), elapsed))


# Max Black value identifier when searching for black pixels
blackMaxIdentifier = 115

# Min Black value identifier when searching for black pixels
blackMinIdentifier = 18

# Height offset in which we will read black pixels
heightOffset = 500

# Number of pixels in height we will read to search for black pixels
lineHeight = 1

# Coordinates used for OpenCV to analyze game screen
gameCoords = [663, 42, 1260, 1025]

# Coordinates of the line we're gonna search black pixels in
lineCoords = [gameCoords[0], gameCoords[3] - heightOffset - lineHeight, gameCoords[2], (gameCoords[3] - heightOffset)]
print("Game Coordinates:")
print(gameCoords)

print("Line Coordinates")
print(lineCoords)
gameLength = gameCoords[2] - gameCoords[0]
gameHeight = gameCoords[3] - gameCoords[1]

# Each black block 
blockLength = round(gameLength/4)
blockHeight = round(gameHeight/4)

# Coordinates of the Columns corresponding to each block
column1 = [0, blockLength]
column2 = [column1[1], blockLength*2]
column3 = [column2[1], blockLength*3]
column4 = [column3[1], blockLength*4]

gameColumns = [column1, column2, column3, column4]
print("Block Coordinates")
print(gameColumns)

# X coordinates for each block location
block1 = round(blockLength/4)
block2 = block1 + blockLength
block3 = block2 + blockLength
block4 = block3 + blockLength

gameBlocks = [block1, block2, block3, block4]
print("Blocks X Coordinates")
print(gameBlocks)

# Variable to optimize search times by skipping the columns if it has been already read
lastBlockClicked = -1

# Variable to count each line read
startCounter = 0

# start()
# getGameCoordinates()
# readColumn(1)
