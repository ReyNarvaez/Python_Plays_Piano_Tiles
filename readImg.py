import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, queryMousePosition, W, moveMouseTo
import time

gameCoords = [663, 42, 1260, 1025]

screen = np.array(ImageGrab.grab(bbox=gameCoords))
screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
# cv2.imshow('screen', screen)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def readBlack(Screen):
    for y in reversed(range(len(Screen))):
        for x in range(len(Screen[y])):
            if Screen[y][x] < 20:
                moveMouseTo(x + gameCoords[0], y + gameCoords[1])


readBlack(screen)