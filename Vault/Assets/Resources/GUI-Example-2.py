from tkinter import *
from tkinter.ttk import Frame, Button, Label, Style

class Menu(Frame):
  def __init__(self):
    super().__init__()

    self.master.title("Vault Payload")
    self.pack(fill = BOTH, expand = True)

    self.columnconfigure(1, weight = 1)
    self.columnconfigure(3, pad = 7)
    self.rowconfigure(3, weight = 1)
    self.rowconfigure(5, pad = 7)
    
    v_User = Label(self, text = "VPS Username")
    v_User.grid(row = 0, column = 0, columnspan = 2, pady = 4, padx = 5)

    area = Entry (self)
    area.grid(row = 1, column = 0, columnspan = 2, padx = 5, sticky = E+W+S+N)
    
    activate = Button(self, text = "Execute")
    activate.grid(row = 1, column = 3)

    # close = Button(self, text = "Close", command = self.master.destroy)
    # close.grid(row = 2, column = 3, pady = 4)
    
    help_button = Button(self, text = "Help")
    help_button.grid(row = 5, column = 0, padx = 5)
  
def main():
  GUI = Tk()
  GUI.geometry("350x300+300+300")
  menu = Menu()
  GUI.mainloop()
  

if __name__ == '__main__':
  main()