import cv2
import Hand_Recognition as Hr
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

device = AudioUtilities.GetMicrophone()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
mic = interface.QueryInterface(IAudioEndpointVolume)

#parameters
wCam, hCam = 1280, 720

def Mute_Unmute(pinky,img):
    if pinky:
        if mic:
            mic.SetMute(False, None)
            cv2.putText(img, "Mic is unmuted", (50, 430), 2, 1, (0, 255, 0), 2)
    else:
        if mic:
            mic.SetMute(True, None)
            cv2.putText(img, "Mic is muted", (50, 430), 2, 1, (0, 255, 0), 2)
