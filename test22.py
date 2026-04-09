import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

canvas = None
prev_x, prev_y = None, None
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        if canvas is None:
            canvas = frame.copy() * 0

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            tip = hand.landmark[8]
            pip = hand.landmark[6]

            x, y = int(tip.x * w), int(tip.y * h)
            index_up = tip.y < pip.y

            if index_up:
                if prev_x is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 0, 255), 5)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = None, None

        out = cv2.addWeighted(frame, 1, canvas, 1, 0)
        cv2.imshow("Air Paint", out)

        if cv2.waitKey(1) == 27:  # ESC
            break

except KeyboardInterrupt:
    canvas = None
    print("Ctrl + C → canvas cleared")

finally:
    cap.release()
    cv2.destroyAllWindows()
