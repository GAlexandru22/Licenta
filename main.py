import cv2
import time
import Hand_Recognition as Hr
import Volume_Control
import Brightness_Control
import Mute_Unmute

#dimensions of the window
wCam, hCam = 1280, 720

#initialising the camera input
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

#initialising the class for hand tracking and landmark recognition
detector = Hr.handTracker()

#FPS initialization
cTime = 0
pTime = 0
#menu initialization
menu = 0
cooldown = 0
def index_up(list):
    index_tip = list[8]
    index_pip = list[5]
    return index_tip[2] < index_pip[2]

def middle_up(list):
    middle_tip = list[12]
    middle_pip = list[9]
    return middle_tip[2] < middle_pip[2]

def ring_up(list):
    ring_tip = list[16]
    ring_pip = list[13]
    return ring_tip[2] < ring_pip[2]

def pinky_up(list):
    pinky_tip = list[20]
    pinky_pip = list[17]
    return pinky_tip[2] < pinky_pip[2]



while True:
    success, img = cap.read()
    #getting the hands from the image
    img = detector.det_hands(img)
    #getting the list of landmarks
    list = detector.pos_lm(img)
    cv2.rectangle(img, (50, 600), (350, 650), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, "Show your hand", (50, 630), 2, 1, (255, 255, 255), 2)

    if list:
        if index_up(list) and not middle_up(list) and not ring_up(list) and not pinky_up(list):
            menu = 1
            cooldown = 200
        elif index_up(list) and not middle_up(list) and not ring_up(list) and pinky_up(list):
            menu = 2
            cooldown = 200
        elif not index_up(list) and not middle_up(list) and not ring_up(list) and pinky_up(list):
            menu = 3
            cooldown = 200
        elif index_up(list) and middle_up(list) and ring_up(list) and pinky_up(list):
            menu = 0



        if cooldown > 0:
            cooldown -= 1

        if menu == 1:
            Volume_Control.VolumeControl(list, img)
        elif menu == 2:
            Brightness_Control.BrightnessControl(list, img)
        elif menu == 3:
            Mute_Unmute.Mute_Unmute(pinky_up(list), img)
        elif menu == 0:
            # cv2.putText(img, "please select a gesture", (50, 120), 3, 1,(255, 0, 255),2)

            print('accuracy {}'.format(detector.get_confidence()))
    # fps calculations
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # fps drawn on the image
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
