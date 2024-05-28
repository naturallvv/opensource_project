import cv2, numpy as np
import mediapipe as mp

# 0: Rock, 1: Scissors, 2: Paper
rsp_gesture = { 0: 'rock', 1:'scissors', 2: 'paper'}
train_file = np.genfromtxt('gesture_train.txt', delimiter = ',')
train_angle = train_file[:, :-1].astype(np.float32)
train_label = train_file[:, -1].astype(np.float32)
knn = cv2.ml.KNearest_create()
knn.train(train_angle, cv2.ml.ROW_SAMPLE, train_label)

mp_hands = mp.solutions.hands
mp_drawing_utils = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    max_num_hands = 2,
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
        rsp_result = []

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

            _, ges_res, _, _ = knn.findNearest(np.array([angle], np.float32), 3)

            idx = int(ges_res[0][0])
            if idx in rsp_gesture.keys():
                org = (int(res.landmark[0].x * frame.shape[1]), int(res.landmark[0].y * frame.shape[0]))
                cv2.putText(frame, rsp_gesture[idx].upper(), (org[0], org[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                rsp_result.append({ 'rsp': rsp_gesture[idx], 'org': org })

            mp_drawing_utils.draw_landmarks(frame, res, mp_hands.HAND_CONNECTIONS, 
                                            mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())

            if len(rsp_result) >= 2:
                rsp_winner = None
                rsp_tie = False

                if rsp_result[0]['rsp'] == 'rock': # ROCK
                    if rsp_result[1]['rsp'] == 'rock': rsp_tie = True # & ROCK = TIE
                    elif rsp_result[1]['rsp'] == 'scissors': rsp_winner = 0 # & SCISSORS = WIN
                    elif rsp_result[1]['rsp'] == 'paper': rsp_winner = 1 # & PAPER = LOSE

                elif rsp_result[0]['rsp'] == 'scissors': # SCISSORS
                    if rsp_result[1]['rsp'] == 'rock': rsp_winner = 1 # & ROCK = LOSE
                    elif rsp_result[1]['rsp'] == 'scissors': rsp_tie = True # & SCISSORS = TIE
                    elif rsp_result[1]['rsp'] == 'paper': rsp_winner = 0 # & PAPER = WIN

                elif rsp_result[0]['rsp'] == 'paper': # PAPER
                    if rsp_result[1]['rsp'] == 'rock': rsp_winner = 0 # & ROCK = WIN
                    elif rsp_result[1]['rsp'] == 'scissors': rsp_winner = 1 # & SCISSORS = LOSE
                    elif rsp_result[1]['rsp'] == 'paper': rsp_tie = True # & PAPER = TIE

                if rsp_winner != None:
                    cv2.putText(frame, 'WINNER', (rsp_result[rsp_winner]['org'][0], rsp_result[rsp_winner]['org'][1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                if rsp_tie:
                    for t in range(2):
                        cv2.putText(frame, 'TIE', (rsp_result[t]['org'][0], rsp_result[t]['org'][1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow('RSP GAME', frame)
    if cv2.waitKey(1) & 0xff == 27: break

cap.release()