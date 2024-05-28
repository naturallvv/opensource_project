import cv2, numpy as np
import mediapipe as mp
import keyboard

# 0: Rock, 1: Scissors, 2: Paper
train_num = int(input('TRAIN_NUMBER : '))
train_file = open('gesture_train.txt', 'a')

mp_hands = mp.solutions.hands
mp_drawing_utils = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands = 1,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    scs, frame = cap.read()
    if not scs: continue

    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks != None:
        for res in result.multi_hand_landmarks:

            joint = np.zeros((21, 3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            v0 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]
            v1 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]
            v = (v1 - v0) / np.linalg.norm((v1 - v0), axis = 1)[:, np.newaxis]

            v2 = v[[0, 1, 2, 4, 5, 6, 8, 9, 10 ,12, 13, 14, 16, 17, 18], :]
            v3 = v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]
            angle = np.degrees(np.arccos(np.einsum('nt, nt -> n', v2, v3)))

            if keyboard.is_pressed('l'):

                for num in angle:
                    num = round(num, 6)
                    train_file.write(str(num) + ',')

                train_file.write(str(train_num) + '.000000\n')

                print('LEARN')

            mp_drawing_utils.draw_landmarks(frame, res, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('GESTURE_TRAIN', frame)
    if cv2.waitKey(1) & 0xff == 27: break

cap.release()
train_file.close()