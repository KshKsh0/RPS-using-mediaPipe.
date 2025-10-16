import random
from collections import defaultdict, deque, Counter
import math, random
MOVES = ["rock","paper","scissors"]
BEATS = {"rock":"paper","paper":"scissors","scissors":"rock"}
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



# try to imporve it 
class AIDecayFreq():
    def __init__(self, half_life):
        self.counts= {m:0.0 for m in MOVES}
        self.half_life= half_life
        self.time= 0
    
    def predict_distribution(self):
        s = sum(self.counts.values()) + 1e-9 # if 0 it will be 1e-9
        return {m:self.counts[m] / s   for m in MOVES}
    
    def choose(self):
        probs=self.predict_distribution()
        target= max(probs , key= probs.get)
        return BEATS[target]
    
    
    def update(self, user_move):
        self.time+=1
        decay = .5 **(1 / self.half_life)
        for m in MOVES:
            self.counts[m] *=decay
        self.counts[user_move]+=1
    
    
#try markov model (first order)
class AiMarkov1:
    def __init__(self, laplace = .5):
        self.trans= {a : {b : laplace for b in MOVES} for a in MOVES}
        self.last_user= None
    def choose(self):
        if self.last_user is None:
            return random.choice(MOVES)
        row = self.trans[self.last_user]
        next_user =max(row , key = row.get) # maximize p(next | last_user)
        return BEATS[next_user]
    
    def update(self , user_move):
        if self.last_user is not None:
            self.trans[self.last_user][user_move]+=1.0
        self.last_user= user_move
        
        
    
#trying now N_gram model 2
class AINgram:
    def __init__(self):
        self.ctx2 = defaultdict(lambda: {m:0.5 for m in MOVES})  # P(x|u_{t-2},u_{t-1})
        self.ctx1 = defaultdict(lambda: {m:0.5 for m in MOVES})  # P(x|u_{t-1})
        self.freq = {m:0.5 for m in MOVES}
        self.history = deque([], maxlen=2)

    def _argmax(self, d):
        return max(d, key=d.get)

    def choose(self):
        if len(self.history)==2:
            pred = self._argmax(self.ctx2[tuple(self.history)])
        elif len(self.history)==1:
            pred = self._argmax(self.ctx1[self.history[0]])
        else:
            pred = self._argmax(self.freq)
        return BEATS[pred]

    def update(self, user_move):
        if len(self.history)==2:
            self.ctx2[tuple(self.history)][user_move] += 1.0
        if len(self.history)>=1:
            self.ctx1[self.history[-1]][user_move] += 1.0
        self.freq[user_move] += 1.0
        self.history.append(user_move)
             
            