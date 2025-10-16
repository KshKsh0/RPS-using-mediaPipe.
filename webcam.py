from collections import Counter, deque
import random
import cv2
import mediapipe as mp
import time
from prediction import AIDecayFreq , AiMarkov1 ,AINgram


Ai= AIDecayFreq(10)
Ai2= AiMarkov1()
Ai3 = AINgram()

WIN_MAP = {
    ("rock", "scissors"): "you",
    ("scissors", "paper"): "you",
    ("paper", "rock"): "you",
    ("scissors", "rock"): "ai",
    ("paper", "scissors"): "ai",
    ("rock", "paper"): "ai",
}

def ai_choice_from_history(history):
  
    if not history:
        return random.choice(["rock", "paper", "scissors"])
    counts = Counter(history)
    likely = counts.most_common(1)[0][0]
    beats = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    return beats[likely]


def decide_winner(user, ai):
    if user == ai:
        return "draw"
    return WIN_MAP.get((user, ai), "draw")

def classify_gesture(landmarks ,w , h):
    TIP = [ 4,8, 12, 16, 20]
    PIP =[3,6, 10, 14, 18]
    pts = [(int(l.x * w), int(l.y * h)) for l in landmarks]
    OF = 0
    for tip , pip  in zip(TIP[1:], PIP[1:]):
        if pts[tip][1] < pts[pip][1] - 10 :
            OF+=1
    if OF== 0:
        return "rock"
    if OF>= 4:
        return "paper"
    if OF == 2:
        return "scissors"
    return None
    
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,      
    max_num_hands=1,             
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

p_time = 0

score_you = 0
score_ai = 0
history = deque(maxlen=8)
last_decision_time = 0
cooldown = 1.0  
phase = "ready"         
phase_start_time = 0
result_display_time = 1.5 
round_cooldown = 2.0      
countdown_time = 1.0       

while True:
    success, img = cap.read()
    if not success:
        break

    h, w = img.shape[:2]
    img = cv2.flip(img, 1)

    user_move = None
    display_text = ""
    now = time.time()

    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)


    if phase == "ready":
        time_since_start = now - phase_start_time

        if time_since_start < countdown_time:
            countdown = int(countdown_time - time_since_start + 1)
            display_text = f"Get ready... {countdown}"
        else:
            # After countdown, read gesture
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    user_move = classify_gesture(hand_landmarks.landmark, w, h)
                    break

            if user_move:
                ai_move = Ai3.choose()
                Ai3.update(user_move)
                winner = decide_winner(user_move, ai_move)
                history.append(user_move)

                if winner == "you":
                    score_you += 1
                elif winner == "ai":
                    score_ai += 1

                display_text = f"You: {user_move} | AI: {ai_move} → {winner.upper()}"
                phase = "result"
                phase_start_time = now  # mark time result started

    # ---- PHASE: RESULT ----
    elif phase == "result":
        display_text = f"Result shown! Next round soon..."
        if now - phase_start_time > result_display_time:
            phase = "ready"
            phase_start_time = now  # restart countdown

    # ---- HUD ----
    cv2.rectangle(img, (0, 0), (w, 60), (0, 0, 0), -1)
    cv2.putText(img, f"Score  You {score_you} : {score_ai} AI",
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, display_text, (10, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # End game condition
    if score_you >= 5 or score_ai >= 5:
        msg = "YOU WIN !" if score_you > score_ai else "AI WINS !" + ' press ESC to restart'
        cv2.rectangle(img, (0, h // 2 - 40), (w, h // 2 + 40), (0, 0, 0), -1)
        cv2.putText(img, msg, (40, h // 2 + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3)

    cv2.imshow('RPS Camera', img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        score_you = 0
        score_ai = 0
