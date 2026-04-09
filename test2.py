import cv2
import numpy as np
import mediapipe as mp

handsm = mp.solutions.hands
drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

canvas = None
prev_x, prev_y = None, None

def finger_states(hand):

    index_tip = hand.landmark[8]
    index_pip = hand.landmark[6]

    middle_tip = hand.landmark[12]
    middle_pip = hand.landmark[10]

    index_up = index_tip.y > index_pip.y
    middle_up = middle_tip.y > middle_pip.y

    return index_up, middle_up


with handsm.Hands(
    max_num_hands = 1,
    model_complexity = 0,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.7
) as hands:
    
    while True:

        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)

        if canvas is None:
            canvas = np.zeros_like(frame)

        small = cv2.resize(frame, (320, 240))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        mode = "none"

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:

                h,w,_ = frame.shape
                fingertip = hand.landmark[8]
                x,y = int(fingertip.x *frame.shape[1]), int(fingertip.y *frame.shape[0])

                index_up, middle_up = finger_states(hand)

                if index_up and middle_up:
                    state = "draw"
                elif index_up and not middle_up:
                    state = "move"
                else:
                    state = "none"
                
                cv2.circle(frame, (x,y), 12, (241,218,165), -1)

                if mode == "paint":
                    if prev_x is not None and prev_y is not None:
                        cv2.line(canvas, (prev_x, prev_y), (x,y), (0,0,255), 8)
                    else:
                        prev_x, prev_y = None, None
                prev_x = x
                prev_y = y
        else:
            prev_x, prev_y = None, None
            
        combined = cv2.addWeighted(frame, 0.7, canvas, 1, 0)
        cv2.putText(combined, f"Mode: {mode}", (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
        cv2.imshow("Air Paint", combined)

        if cv2.waitKey(0) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()

