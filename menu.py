from tkinter import*
from logik import*


class Main_menu:
    def __init__(self, tk):     
        self.tk= tk
        self.show_menu()

    def show_menu(self):                        #vytvorí tlačítka na voľbu módu
        b_mode_1 = Button(text = "pvp", command= lambda:self.start_game(0))
        b_mode_2 = Button(text = "evp", command= lambda:self.start_game(1))
        b_mode_3 = Button(text = "pve", command= lambda:self.start_game(2))

        b_mode_1.pack()
        b_mode_2.pack()
        b_mode_3.pack()

    def delete_elements(self):                  #vymaže všetky elementy inštancie tk
        for button in self.tk.winfo_children():
            button.destroy()

    def new_game(self):                         #zapnutie new game, tlačidlom na hracej ploche
        self.delete_elements()
        self.show_menu()

    def start_game(self,gamemode):              #vytvorí inštanciu board, s parametrom gamemode, určuje mód aký sa zapne
        self.delete_elements()
        self.game = Board(gamemode, self.tk, self)

