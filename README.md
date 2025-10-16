# 🪨📄✂️ Rock–Paper–Scissors AI (MediaPipe + OpenCV)

Play **Rock–Paper–Scissors** against an adaptive AI using your **webcam** and **hand gestures**!  
The AI learns your habits over time using different machine learning strategies — from simple frequency counting to Markov and N-gram models.

---

## 🎮 Features

- 🖐️ Real-time hand gesture detection using **MediaPipe Hands**
- 🧠 Multiple AI strategies:
  - **AIDecayFreq** – learns recent habits with exponential decay  
  - **AiMarkov1** – predicts based on your last move (Markov chain)  
  - **AINgram** – predicts based on short move sequences (N-gram model)
- ⏳ Round phases with countdown and result display  
- 🏆 Live scoring & visual feedback  
- ⚡ Fast, lightweight, and pure Python

---

## 📂 Project Structure

```
RPS-using-mediaPipe/
│
├── webcam.py       # main game loop (camera input, gesture detection, UI)
├── prediction.py   # AI prediction models (adaptive strategies)
└── README.md       # project info
```

---

## 🧰 Requirements

- Python **3.10+**
- **OpenCV**
- **MediaPipe**
- **NumPy** (optional)

Install them easily:
```bash
pip install opencv-python mediapipe numpy
```

---

## 🚀 Run the Game

```bash
python webcam.py
```

Then:

1. Position your hand clearly in front of your webcam  
2. Wait for the countdown  
3. Show a gesture:  
   - ✊ **Rock**  
   - ✋ **Paper**  
   - ✌️ **Scissors**  
4. See if the AI can beat you!

> Press **ESC** to reset the score or exit.

---

## 🧠 How the AI Works

| Model | Strategy | Description |
|--------|-----------|-------------|
| **AIDecayFreq** | Exponential moving average | Learns recent player behavior while forgetting older patterns |
| **AiMarkov1** | First-order Markov chain | Predicts next move based on your last move |
| **AINgram** | N-gram pattern learning | Detects short move sequences (like “rock → paper → scissors”) and predicts what comes next |

Each model estimates the probability of your next move and plays the counter-move that beats it.  
The system can easily be extended with neural networks or reinforcement learning.

---

## 🧩 Possible Upgrades

- 🎨 Add GUI or sound effects  
- 🧬 Use a small neural net trained on hand landmarks  
- 📊 Add data visualization for player patterns  

