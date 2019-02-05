import numpy as np
from PIL import ImageGrab
import cv2

gameCoords = [670, 34, 1250, 860]
screen = np.array(ImageGrab.grab(bbox=gameCoords))
screen = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

# define range of black color in screen
lower_black = np.array([0, 0, 0])
upper_black = np.array([50, 50, 50])

# lower_black = np.array([80, 54, 17])
# upper_black = np.array([210, 127, 20])



# Threshold the screen image to get only black colors
mask = cv2.inRange(screen, lower_black, upper_black)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(screen, screen, mask=mask)

cv2.imshow('screen', screen)
cv2.waitKey(0)

cv2.imshow('mask', mask)
cv2.waitKey(0)

cv2.imshow('res', res)
cv2.waitKey(0)

cv2.destroyAllWindows()