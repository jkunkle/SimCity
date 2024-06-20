import tkinter as tk

board = [ [None]*10 for _ in range(10) ]

counter = 0

root = tk.Tk()

def on_click(i,j,event):
    global counter
    color = "red" if counter%2 else "black"
    event.widget.config(bg=color)
    #board[i][j] = color
    counter += 1


for i,row in enumerate(board):
    for j,column in enumerate(row):
        L = tk.Label(root,text='test',bg='grey')
        L.grid(row=i,column=j)
        L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j,e))

root.mainloop()
