import cv2
import mediapipe as mp


class handTracker():
    #init for the class
    def __init__(self, mode=False, max_no_hands=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_no_hands = max_no_hands
        self.detection_con = detection_con
        self.track_con = track_con
        #initialising the hand detection features
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.max_no_hands,
                                        min_detection_confidence=self.detection_con,
                                        min_tracking_confidence=self.track_con)

        self.mpDraw = mp.solutions.drawing_utils
    #method for detecting hands in the image and draw the landmarks
    def det_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            # for to pass through each hand
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # draw the connections between the landmarks of the hand
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    #method to get the possition of each landmark and save it in a list
    def pos_lm(self, img, handNo=0, draw=True):

        lm_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            # for to pass through each point of the hand
            for id, lm in enumerate(hand.landmark):
                # dimensions of the image
                height, width, channel = img.shape
                # coordinates of the point
                cx, cy = int(lm.x * width), int(lm.y * height)
                lm_list.append([id, cx, cy])

        return lm_list
    #method to detect the confidence of the algorithm
    def get_confidence(self):
        confidence = []
        if self.results.multi_handedness:
            for hand_info in self.results.multi_handedness:
                confidence.append(hand_info.classification[0].score)
        return confidence
    