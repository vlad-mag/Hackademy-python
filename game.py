from tkinter import *
import random
import time

# variabile globale pentru scor
score1 = 0
score2 = 0

tk = Tk() # creeaza window-ul pentru aplicatie
tk.title("Pong Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.config(bg='black')
canvas.pack()
tk.update() 

canvas.create_line(250,0,250,400,fil='white')

class Ball:
    def __init__(self, canvas, color, paddle1, paddle2):
        self.canvas = canvas
        self.paddle1 = paddle1
        self.paddle2 = paddle2
        self.id = canvas.create_oval(10,10,25,25,fill=color)
        self.canvas.move(self.id, 233, 180)
        starts = [-3,3]
        random.shuffle(starts) #directia de start este random
        self.x = starts[0] #primul element din lista randomizata este atribuit miscarii pe orizontala
        self.y = -3 #miscarea verticala este in sus prin aceasta valoare
        self.canvas_height = self.canvas.winfo_height() # pentru a verifica daca bila atinge partea de sus sau de jos
        self.canvas_width = self.canvas.winfo_width() # pentru a verifica daca bila atinge partea stanga sau dreapta
        
    def score(self, val):
        global score1, score2
        if val:
            score1 += 1
        else:
            score2 += 1
        canvas.delete("score1_text") 
        canvas.create_text(125, 40, text='Score: ' + str(score1), font=('Arial', 30), fill='white', tag="score1_text")
        canvas.delete("score2_text")  
        canvas.create_text(375, 40, text='Score: ' + str(score2), font=('Arial', 30), fill='white', tag="score2_text")
        
    
    def draw(self):
        # 0 stanga, 1 sus, 2 dreapta, 3 jos
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0: #daca ajunge la marginea de sus a canvas-ului
            self.y = 3 #incepe sa se miste in jos
        if pos[3] >= self.canvas_height: #daca ajunge la marginea de jos a canvas-ului
            self.y = -3 #incepe sa se miste in sus
        if pos[0] <= 0: #margine stanga
            self.x = 3
            self.score(False)
        if pos[2] >= self.canvas_width: #margine dreapta
            self.x = -3
            self.score(True)
        if self.hit_paddle1(pos) == True: #daca mingea loveste paddle1
            self.x = 3
        if self.hit_paddle2(pos) == True: #daca mingea loveste paddle2
            self.x = -3

    def hit_paddle1(self, pos):
        paddle_pos = self.canvas.coords(self.paddle1.id)
        if pos[1] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
            if pos[0] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                return True
            return False
    
    def hit_paddle2(self, pos):
        paddle_pos = self.canvas.coords(self.paddle2.id)
        if pos[1] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
            if pos[2] >= paddle_pos[0] and pos[2] <= paddle_pos[2]:
                return True
            return False
        
class Paddle:
    def __init__(self, canvas, color, x_start, y_start, key_left, key_right):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x_start, y_start, x_start + 30, y_start + 100, fill=color)
        self.y = 0 # viteza pe vericala
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.key_left = key_left
        self.key_right = key_right
        # bind-urile pentru a misca paletele
        self.canvas.bind_all(f'<KeyPress-{self.key_left}>', self.start_move_left)
        self.canvas.bind_all(f'<KeyRelease-{self.key_left}>', self.stop_move_left)
        self.canvas.bind_all(f'<KeyPress-{self.key_right}>', self.start_move_right)
        self.canvas.bind_all(f'<KeyRelease-{self.key_right}>', self.stop_move_right)
        self.move_left = False
        self.move_right = False
        
    def draw(self):
        if self.move_left:
            self.canvas.move(self.id, 0, -3)
        elif self.move_right:
            self.canvas.move(self.id, 0, 3)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.move_left = False
            self.move_right = False
            self.canvas.move(self.id, 0, -pos[1])
        elif pos[3] >= self.canvas_height:
            self.move_left = False
            self.move_right = False
            self.canvas.move(self.id, 0, self.canvas_height - pos[3])
            
    def start_move_left(self, evt):
        self.move_left = True
        
    def stop_move_left(self, evt):
        self.move_left = False
        
    def start_move_right(self, evt):
        self.move_right = True
        
    def stop_move_right(self, evt):
        self.move_right = False
        
paddle1 = Paddle(canvas, 'blue', 0, 150, 'w', 's')
paddle2 = Paddle(canvas, 'red', 470, 150, 'Up', 'Down')
ball = Ball(canvas, 'orange', paddle1, paddle2)

def restart_game():
    global score1, score2, paddle1, paddle2, ball
    score1 = 0
    score2 = 0
    canvas.delete("all")
    paddle1 = Paddle(canvas, 'blue', 0, 150, 'w', 's')
    paddle2 = Paddle(canvas, 'red', 470, 150, 'Up', 'Down')
    ball = Ball(canvas, 'orange', paddle1, paddle2)
    canvas.create_line(250, 0, 250, 400, fill='white')
    canvas.create_text(125, 40, text='Score: ' + str(score1), font=('Arial', 30), fill='white', tag="score1_text")
    canvas.create_text(375, 40, text='Score: ' + str(score2), font=('Arial', 30), fill='white', tag="score2_text")
    ball.x = 3  
    ball.y = -3
    time.sleep(3)
    tk.update()
    
while 1:
    if score1 < 5 and score2 < 5:
        ball.draw()
        paddle1.draw()
        paddle2.draw()
    
    if score1 == 5:
        canvas.create_text(250, 200, text='Player 1 WON! Game Over', font=('Arial', 30), fill='green')
        tk.after(1, restart_game)  
    elif score2 == 5:
        canvas.create_text(250, 200, text='Player 2 WON! Game Over', font=('Arial', 30), fill='green')
        tk.after(1, restart_game) 
    # update real time al elementelor din GUI
    tk.update_idletasks() 
    tk.update()
    time.sleep(0.01)
    