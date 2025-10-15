import cv2
import numpy as np
import math
import screen_brightness_control as sbc

#values of the max and minimum brightness
minB = 0
maxB = 100

def BrightnessControl(lm_list, img):
    if lm_list:
        #Taking the values of the points
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]

        #drawing the line between points
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        #Calculating the distance between the 2 points
        length = math.hypot(x2 - x1, y2 - y1)

        brightness = int(np.interp(length, [40, 300], [minB, maxB]))
        bBar = np.interp(length, [50, 300], [400, 150])
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(bBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Brightness", (50, 430), 2, 1, (0, 255, 0), 2)
        sbc.set_brightness(brightness, display=1)

