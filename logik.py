from collections import deque
from tkinter import*
from menu import*
import random


class Board:                            
    def __init__(self, gamemode, tk, menu):             #konštruktor,deklaruje základné premenné a zapne funkcie create_board a create_buttons ktoré vytvoria hraciu plochu
        self.menu=menu
        self.tk=tk
        self.canvas = Canvas(height= 600, width = 500, bg="white", master=self.tk)
        self.canvas.pack()

        self.gamemode = gamemode
        self.create_board()
        self.create_buttons()

        self.win = False
        self.position=0
        self.round=0
        self.player_1 = 5*[0]
        self.player_2 = 5*[0]
        self.colors_dict = dict()
        self.colors_used = dict()
        colours= ["red","lime","orange","blue","cyan", "yellow", "magenta", "brown"]
        for i in range(1,9):
            self.colors_dict[i]=colours[i-1]
            self.colors_used[i]=6*[0]
        if gamemode == 1:
            self.evp()

    def create_board(self):
        self.p1_text = "player 1"
        self.p2_text = "player 2"
        if self.gamemode == 1:
            self.p1_text = "computer"
        elif self.gamemode == 2:
            self.p2_text = "computer"

        self.canvas.delete("all")
        for i in range (1,5):
            self.canvas.create_line(i*35+50, 50, i*35+50, 400, fill="#c8c8c8")
            self.canvas.create_line(i*35+275, 50, i*35+275 , 400, fill="#c8c8c8")
            self.canvas.create_line(i*35+50, 440, i*35+50 , 475, fill="#c8c8c8")
        for i in range (1,11):
            self.canvas.create_line(50, i*35+50, 225, i*35+50)
            self.canvas.create_line(275, i*35+50, 450, i*35+50)
            self.canvas.create_text(35, i*35+33,text=str(i),font="Times 15 bold")

        self.canvas.create_rectangle(50, 50, 225, 400)
        self.canvas.create_rectangle(275, 50, 450, 400)
        self.canvas.create_rectangle(50, 440, 225, 475)

        self.canvas.create_text(140, 420, font="Times 15 bold", text=self.p1_text)
        self.canvas.create_text(140, 30, font="Times 15 bold", text=self.p2_text)
        
    def create_buttons(self):
        self.b_color_1 = Button(text = "red", command=lambda:self.create_circle(1))
        self.b_color_2 = Button(text = "green", command=lambda:self.create_circle(2))
        self.b_color_3 = Button(text = "orange", command=lambda:self.create_circle(3))
        self.b_color_4 = Button(text = "blue", command=lambda:self.create_circle(4))
        self.b_color_5 = Button(text = "cyan", command=lambda:self.create_circle(5))
        self.b_color_6 = Button(text = "yellow", command=lambda:self.create_circle(6))
        self.b_color_7 = Button(text = "pink", command=lambda:self.create_circle(7))
        self.b_color_8 = Button(text = "brown", command=lambda:self.create_circle(8))

        self.b_delete = Button (text = "delete", command = lambda:self.delete_circle())
        self.b_next_round = Button(text="next round", command = lambda:self.next_round())
        self.b_new_game = Button(text="new game", command = lambda: self.menu.new_game())

        self.b_color_1.pack(side= LEFT)
        self.b_color_2.pack(side= LEFT)
        self.b_color_3.pack(side= LEFT)
        self.b_color_4.pack(side= LEFT)
        self.b_color_5.pack(side= LEFT)
        self.b_color_6.pack(side= LEFT)
        self.b_color_7.pack(side= LEFT)
        self.b_color_8.pack(side= LEFT)

        self.b_new_game.pack(side= RIGHT)
        self.b_next_round.pack(side= RIGHT)
        self.b_delete.pack(side= RIGHT)

    def create_circle(self, color):                 #vykresluje panáčikov, na základe stačeného tlačítka
        if self.position <5 and color not in self.player_1 and self.round == 0:
                self.canvas.create_oval(self.position*35+52, 442, self.position*35+83, 473, fill=self.colors_dict[color], outline= "")
                self.player_1[self.position] = color
                self.position+=1
        elif self.position <5 and color not in self.player_2 and self.round >0:
                self.canvas.create_oval(52+35*self.position,52+35*(self.round-1),83+35*self.position,83+35*(self.round-1), fill=self.colors_dict[color], outline= "")
                self.player_2[self.position] = color
                self.position+=1

    def delete_circle(self):                        #vymaže posledného vykresleného panáčika
        if self.position > 0:
            self.position-=1
            if self.round == 0:
                self.player_1[self.position] = 0
                self.canvas.create_oval(self.position*35+52, 442, self.position*35+83, 473, fill="white", outline= "")
            else:
                self.player_2[self.position] = 0
                self.canvas.create_oval(52+35*self.position,52+35*(self.round-1),83+35*self.position,83+35*(self.round-1), fill="white", outline= "")

    def next_round(self):                           #posúva hru do nového stavu, zapína funkciu na ohodnotenie stavu a zakrýva postupnosť hráča 1
        if self.position == 5:
            if self.round>0:
                self.state_rating()
                if self.gamemode == 2 and self.win == False:
                    self.pve()
            else:
                self.canvas.create_rectangle(50, 440, 225, 475, fill="black", tag="black_box")
                self.round+=1
                self.position=0
                if self.gamemode == 2 and self.win == False:
                    self.pve()

    def state_rating(self):                         #ohodnocuje postupnosť hráča 2, zaznamenáva stav do color dictu
        for i in range(5):
            if self.player_2[i] == self.player_1[i]:            #porovnáva pozíciu a farbu panáčikov, pvykresluje čierny puntík
                self.canvas.create_oval(277+35*i, 52+35*(self.round-1), 308+35*i, 83+35*(self.round-1), fill="black", outline="")
                self.colors_used[self.player_2[i]][0]=1
                self.colors_used[self.player_2[i]][i+1]=1
            elif self.player_2[i] in self.player_1:             #porovnáva či je farba puntíku v postupnosti hráča 1, vykresluje sivý puntík
                self.canvas.create_oval(277+35*i, 52+35*(self.round-1), 308+35*i, 83+35*(self.round-1), fill="grey", outline="")
                self.colors_used[self.player_2[i]][i+1]=-1
                self.colors_used[self.player_2[i]][0]=2
            else:                                               #keď nie je farba použitá, zaznamená si to do color_dictu
                self.colors_used[self.player_2[i]][0]=-1

        if self.player_1 == self.player_2:                      # podmienka pre ukončenie hry
             self.win = True 
             self.end_screen()
        elif self.round == 10:
            self.end_screen()

        self.round+=1
        self.position=0
        self.player_2=5*[0]
        
    def pve (self):                                             #funkcia ktorá hrá za hráča 2, pokiaľ je zapnutý mód pve
        sequence = solver(self.colors_used)
        for i in sequence:
            self.create_circle(i)
        self.next_round()
        
    def evp (self):                                             #funkcia, ktorá hrá za hráča 1, pokiaľ je zapnutý mód evp
        for i in range(5):
            i = random.randint(1,8)
            while i in self.player_1:
                i = random.randint(1,8)
            self.create_circle(i)
        self.next_round()
    
    def end_screen(self):                                       #vykresľuje výhernú obrazovku, vypína tlačítka, vypisuje kto vyhral
        self.canvas.delete("black_box")
        if self.win:
            self.canvas.create_text(250,250,font="Times 50 bold", fill="DarkOrchid4", text=f"{self.p2_text} wins!")
        else:
            self.canvas.create_text(250,250,font="Times 50 bold", fill="DarkOrchid4", text=f"{self.p1_text} wins!")
        
        self.b_color_1["state"] = DISABLED
        self.b_color_2["state"] = DISABLED
        self.b_color_3["state"] = DISABLED
        self.b_color_4["state"] = DISABLED
        self.b_color_5["state"] = DISABLED
        self.b_color_6["state"] = DISABLED
        self.b_color_7["state"] = DISABLED
        self.b_color_8["state"] = DISABLED

        self.b_delete["state"] = DISABLED
        self.b_next_round["state"] = DISABLED

class State:                                                   #pomocná classa k funkcii solver, ukladá stavy, aby sa mohli vložiť do zásobníku
    def __init__(self, state, position) -> None:
        self.state = state.copy()
        self.position = position

def solver(colors_used):                                       #funkcia, ktorá háda postupnosť
    stack = deque()
    position = 0
    start_state = 5*[0]
    for j in range (5):                                         #najskôr doplní panáčikov, ktorý boli ohodnotený čiernym puntíkom
        for i in range(1,9):    
                if i not in start_state and colors_used[i][0] == 1 and colors_used[i][j+1] == 1:
                    start_state[j] = i
    current_state = start_state.copy()
    while position < 5:                                         #iteruje pokým nenájde stav, kde sú doplnení všetci panáčikovia
        if current_state[position] == 0:                        #ak je už v postupnosti doplnení panáčik (bol ohodnotený čiernym puntíkom) tak túto pozíciu preskakuje
            for i in range(1,9):        
                if i not in current_state and colors_used[i][0] == 0:           # dopĺňa panáčikov ohodnotených šedým puntíkom, na pozíciu kde ešte neboli
                    current_state[position]=i
                    stack.appendleft(State(current_state, position+1))
            for i in range(1,9):    
                if i not in current_state and colors_used[i][0] == 2 and colors_used[i][position+1] == 0:           #doplňuje farbu panáčika, ktorá ešte nebola použitá
                    current_state[position]=i
                    stack.appendleft(State(current_state, position+1))
            state = stack.popleft()                          #vyberá nový state na prehladanie zo zásobníku
            current_state = state.state
            position = state.position
        else:
            position+=1

    return current_state                                          #vracia hotovú postupnosť 