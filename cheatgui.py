from tkinter import *


class Gui:
    def __init__(self, window):
        self.window = window

        self.frame_guess = Frame(self.window)
        self.label_guess = Label(self.frame_guess, text="Guess: ")
        self.label_guess.pack(side='left')
        self.input_guess = Entry(self.frame_guess, width=20)
        self.input_guess.pack(side='left')
        self.frame_guess.pack(anchor='w', padx=10, pady=10)

        self.frame_color = Frame(self.window)
        self.color_1 = Button(self.window, command=print("1"), bg="black")
        self.color_1.pack(side='left')
        self.color_2 = Button(self.window, command=print("2"), bg="black")
        self.color_2.pack(side='left')
        self.color_3 = Button(self.window, command=print("3"), bg="black")
        self.color_3.pack(side='left')
        self.color_4 = Button(self.window, command=print("4"), bg="black")
        self.color_4.pack(side='left')
        self.color_5 = Button(self.window, command=print("5"), bg="black")
        self.color_5.pack(side='left')
        self.frame_color.pack(anchor='w', padx=10, pady=10)

        self.save_button = Button(self.window, text="SAVE", command=self.submit_data)
        self.save_button.pack(pady=10)

                                  
    def swap_color(self):
        self.button