from tkinter import *

def change_color():
    current_color = box.cget("background")
    next_color = "green" if current_color == "red" else "red"
    box.config(background=next_color)
    root.after(1000, change_color)

root = Tk()
box = Text(root, background="green")
box.pack()
change_color()
root.mainloop()