import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, queryMousePosition, W, moveMouseTo
import time

for i in list(range(3))[::-1]:
    print(i+1)
    time.sleep(1)

firstOffset = 140
lastOffset = 244
gameCoords = [670, 34, 1250, 860]
firstPos = gameCoords[0] - firstOffset
lastPos = gameCoords[2] - lastOffset
screenRange = lastPos - firstPos

moveMouseTo(firstPos, gameCoords[1])
mousePos = queryMousePosition()

if gameCoords[2] > (mousePos.get("x") + firstOffset) >= gameCoords[0]:
    start = time.time()
    screen = np.array(ImageGrab.grab(bbox=gameCoords))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    cv2.imshow('screen', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    blacks = np.argwhere(screen == 0)
    for index in blacks:
        for i in index:
            print(i)
            print(screen[i])
            time.sleep(0.0001)