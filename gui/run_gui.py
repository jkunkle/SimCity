
import tkinter as tk
from tkinter import ttk

def on_click(i,j,event):

    new_color = 'red'
    print (event)
    if event.widget.cget('bg') == 'red':
        new_color='black'
    event.widget.config(bg=new_color)

def main():

    gui = tk.Tk()

    gui_frame = ttk.Frame(gui)

    top_frame = ttk.Frame(gui_frame, width=200, height=10, borderwidth=5)

    left_frame = ttk.Frame(gui_frame, width=10, height=200)

    board_frame = ttk.Frame(gui_frame, width=190, height=190)

    ok = ttk.Button(left_frame, text="Okay")
    cancel = ttk.Button(left_frame, text="Cancel")

    gui_frame.grid(column=0, row=0)
    top_frame.grid(column=0, row=0, rowspan=2)
    left_frame.grid(column=0, row=0, columnspan=2)
    board_frame.grid(column=1, row=1)
    name = ttk.Label(top_frame, text='time')

    ok.grid(column=0, row=0)
    cancel.grid(column=0, row=1)
    name.grid(column=0, row=0)


    for i in range(0, 10):
        for j in range(0, 10):
            L = tk.Label(board_frame,text='test',bg='grey')
            L.grid(row=i,column=j)
            L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j,e))

    gui.mainloop()

if __name__ == '__main__':
    main()
