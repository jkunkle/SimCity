from tkinter import *
 
button_list = ['dummy']
class button_box :
    def __init__ (self, button, ID_number) :
        self.ID_number = ID_number
        self.button = button
 
    def clicked (self, event) :
        self.button
        print (f'You pressed button number {self.ID_number}')
 
root = Tk ()
 
button_number = 1
for y in range (5) :
    for x in range (9) :
        button = Button (width = 1, height = 1, padx=0, pady=0, bd=0)
        button['background'] = 'green'
        #button.config (bg='green', fg='green')
        button.grid (row = y, column = x)
        button_list.append (button_box (button, button_number))
        button.bind ('<Button-1>', button_list[button_number].clicked)
        button_number += 1
 
mainloop ()
