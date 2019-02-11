from tkinter import *
from tkinter.ttk import Frame, Button, Label, Style

class Menu(Frame):
  def __init__(self):
    super().__init__()

    self.master.title("Vault Payload")
    self.pack(fill = BOTH, expand = True)

    self.columnconfigure(1, weight = 1)
    self.columnconfigure(2, pad = 1)
    
    self.v_User = Label(self, text = "VPS Username")
    self.v_User.grid(row = 0, column = 0, columnspan = 1, pady = 4, padx = 5, ipadx = 5)
    self.v_User_entry = Entry(self, justify = "center")
    self.v_User_entry.grid(row = 1, column = 0, columnspan = 1, padx = 5, sticky = E+W+S+N)

    self.v_Password = Label(self, text = "Password")
    self.v_Password.grid(row = 0, column = 1, columnspan = 1, pady = 4, padx = 5, ipadx = 5)
    self.v_Password_entry = Entry(self, show = "*", justify = "center")
    self.v_Password_entry.grid(row = 1, column = 1, columnspan = 1, padx = 5, sticky = E+W+S+N)
    self.v_Password_button = Button(self, text = "Show", command = self.showPassword)
    self.v_Password_button.grid(row = 1, column = 3, padx = 5)

    self.v_IP = Label(self, text = "VPS IP-Address")
    self.v_IP.grid(row = 2, column = 0, columnspan = 1, pady = 4, padx = 5, ipadx = 5)
    self.v_IP_entry = Entry(self, justify = "center")
    self.v_IP_entry.grid(row = 3, column = 0, columnspan = 1, padx = 5, sticky = E+W+S+N)

    self.activate = Button(self, text = "Execute")
    self.activate.grid(row = 5, column = 1, padx = 5, pady = 10, sticky = E)

    self.close = Button(self, text = "Close", command = self.master.destroy)
    self.close.grid(row = 5, column = 3, padx = 5, pady = 5)
    
    self.help_button = Button(self, text = "Help")
    self.help_button.grid(row = 5, column = 0, padx = 5, pady = 10, sticky = W)

  def showPassword(self):
    text = self.v_Password_entry.get()

    self.v_Password_entry = Entry(self, justify = "center")
    self.v_Password_entry.insert(0, f"{text}")
    self.v_Password_entry.grid(row = 1, column = 1, columnspan = 1, padx = 5)

  def executePayload(self):
    v_User = self.v_User.get()
    # v_Passowrd = self.v_Password.get()
    v_IP = self.v_IP.get()

    





def main():
  GUI = Tk()
  GUI.iconbitmap("Vault.ico")
  menu = Menu()
  GUI.mainloop()


  
if __name__ == "__main__":
  main()