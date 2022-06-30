import cv2
import mediapipe as mp
from adafruit_servokit import ServoKit
from CamReceiver import CamReceiver

kit = ServoKit(channels=16)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def get_finger_gesture(landmarks, w, h):
    finger_pos = [(landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * h,
                   landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * h),
                  (landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h,
                   landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * h),
                  (landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h,
                   landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * h),
                  (landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * h,
                   landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * h),
                  (landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * h,
                   landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x * w,
                   landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * h)]
    gesture = [0, 0, 0, 0, 0]
    gesture[0] = 1 if finger_pos[0][0] < finger_pos[0][2] else 0
    gesture[1] = 1 if finger_pos[1][1] > finger_pos[1][3] else 0
    gesture[2] = 1 if finger_pos[2][1] > finger_pos[2][3] else 0
    gesture[3] = 1 if finger_pos[3][1] > finger_pos[3][3] else 0
    gesture[4] = 1 if finger_pos[4][1] > finger_pos[4][3] else 0
    return gesture
    

# For webcam input:
width = 320
height = 240
cam = CamReceiver(width, height)
cam.start()

with mp_hands.Hands(
    #model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cv2.waitKey(1) != 27:
        if cam.empty():
            continue

        image = cam.get(True)
        while not cam.empty():
            cam.get(True)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape
        if results.multi_hand_landmarks:
          for hand_landmarks in results.multi_hand_landmarks:
            gesture = get_finger_gesture(hand_landmarks, image_width, image_height)
            #print(gesture)
            a=gesture[0]
            b=gesture[1]
            c=gesture[2]
            d=gesture[3]
            e=gesture[4]
            if(a==1):
                kit.servo[0].angle = 120
            else:
                kit.servo[0].angle = 00
            if(b==1):
                kit.servo[1].angle = 170
            else:
                kit.servo[1].angle = 00
            if(c==1):
                kit.servo[2].angle = 160
            else:
                kit.servo[2].angle = 00
            if(d==1):
                kit.servo[3].angle = 160
            else:
                kit.servo[3].angle = 00
            if(e==1):
                kit.servo[4].angle = 160
            else:
                kit.servo[4].angle = 00
                
            #print("HAND: %d %d %d %d %d" % (gesture[0], gesture[1], gesture[2], gesture[3], gesture[4]))
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

cv2.destroyAllWindows()
