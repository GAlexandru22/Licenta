import cv2
import numpy as np
import Hand_Recognition as Hr
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
#init of the variables
vol = 0
volBar = 400
#audio divice init
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

#taking the maximum and minimum limits of the volume
minVol = volume.GetVolumeRange()[0]
maxVol = volume.GetVolumeRange()[1]
def VolumeControl(lm_list, img):

    x1, y1 = lm_list[4][1], lm_list[4][2]
    x2, y2 = lm_list[8][1], lm_list[8][2]
    cv2.line(img, (x1, y1), (x2, y2),(255, 0, 255), 3)
    length = math.hypot(x2 - x1, y2 - y1)

    print("length between fingers: {}".format(length))
    vol = np.interp(length, [30, 300], [minVol, maxVol])
    volBar = np.interp(length, [50, 300], [400, 150])
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, "Volume", (50, 430), 2, 1, (0, 255, 0), 2)
    print("Volume in dB: {}".format(vol))
    volume.SetMasterVolumeLevel(vol, None)

