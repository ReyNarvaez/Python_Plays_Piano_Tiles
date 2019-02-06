import cv2
import numpy as np
from PIL import ImageGrab
from pathlib import Path

# initialize the list of reference points and boolean indicating
# whether isCalculating is being performed or not
storedCoordinates = [(883, 267), (1195, 616)]
coordinatesFileName = "coordinates.txt"
isCalculating = False
image = None
imageFileName = "fullScreen.jpg"


# Checks if coordinates file exists, if true reads the content, else return false
def readCoordinatesFile():
    file = Path(coordinatesFileName)
    if file.is_file():
        file = open(coordinatesFileName, "r")
        print("Coordinates File Found")
        if file.mode == 'r':
            print("Reading Coordinates")
            content = file.read()
            if not content:
                print("File Is Empty")
                return False
            else:
                content = content.split(",")
                if content.__len__() != 4:
                    print("Coordinates Are Not Complete")
                    return False
                else:
                    print("Reading File Completed")
                    assignCoordinates(content)
                    return True
    else:
        return False


# Assigns and formats content read from the coordinates file
def assignCoordinates(content):
    global storedCoordinates
    storedCoordinates = [(parseStrToInt(content[i]), parseStrToInt(content[i + 1])) for i in range(0, len(content), 2)]


def parseStrToInt(string):
    return int(string)


# Converts coordinates to format that is expected
def convertCoordinates():
    convertedCoordinates = []
    for coord in storedCoordinates:
        convertedCoordinates.append(coord[0])
        convertedCoordinates.append(coord[1])
    return convertedCoordinates


# Writes coordinates taken from screen to the file
def writeCoordinatesToFile():
    file = open(coordinatesFileName, "a+")
    x1 = storedCoordinates[0][0]
    y1 = storedCoordinates[0][1]
    x2 = storedCoordinates[1][0]
    y2 = storedCoordinates[1][1]

    content = str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2)
    file.write(content)
    file.close()


# Click event that handles and track mouse location
def clickEvent(event, x, y, flags, param):
    # grab references to the global variables
    global storedCoordinates, isCalculating, image

    # if the left mouse button was clicked, record the starting (x, y) storedCoordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        storedCoordinates = [(x, y)]
        isCalculating = True

    # check to see if the left mouse button was released, record the ending (x, y) storedCoordinates
    elif event == cv2.EVENT_LBUTTONUP:
        storedCoordinates.append((x, y))
        isCalculating = False
        # draw a rectangle around the region of interest
        cv2.rectangle(image, storedCoordinates[0], storedCoordinates[1], (0, 255, 0), 2)
        cv2.imshow("image", image)


# Takes a screenshot of the game and handles the click event
def getGameCoordinates():
    print("*******************RECORD COORDINATES*******************")
    print("Click And Drag The Mouse To Select The Desired Game Area")
    print("Press R To Retake Coordinates")
    print("Press S To Save Coordinates")
    print("********************************************************")

    global image
    # take full screen screenshot, clone it, and setup the mouse callback function
    cv2.imwrite(imageFileName, np.array(ImageGrab.grab()))
    image = cv2.imread(imageFileName)

    clone = image.copy()
    cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("image", clickEvent)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the isCalculating region
        if key == ord("r"):
            print("Retaking Coordinates")
            image = clone.copy()

        # if the 's' key is pressed, break from the loop
        elif key == ord("s"):
            print("Saving Coordinates")
            writeCoordinatesToFile()
            break

    # close all open windows
    cv2.destroyAllWindows()


# Returns the coordinates whether from the file or the ones taken by the user
def getStoredCoordinates():
    hasCoordinates = readCoordinatesFile()

    if not hasCoordinates:
        print("Coordinates File Not Found\nPreparing To Record Coordinates")
        getGameCoordinates()

    return convertCoordinates()

getStoredCoordinates()
