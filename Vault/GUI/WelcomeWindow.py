import sys
import textwrap
from tkinter import *

from HostWindow import HostWindow

class WelcomeWindow(Frame):

  def __init__(self):
    super().__init__()

    self.master.title("Vault")
    self.pack(fill = BOTH, expand = True)

    self.columnconfigure(0, weight = 1)
    # self.columnconfigure(1, weight = 1)

    # Menu:
    self.menubar = Menu(self)
    filemenu = Menu(self.menubar, tearoff = 0)
    filemenu.add_command(label = "New", command = self.doNothing)
    filemenu.add_command(label = "Open", command = self.doNothing)
    filemenu.add_command(label = "Save", command = self.doNothing)
    filemenu.add_command(label = "Save as...", command = self.doNothing)
    filemenu.add_command(label = "Close", command = self.doNothing)

    filemenu.add_separator()

    filemenu.add_command(label = "Exit", command = self.master.destroy)

    self.menubar.add_cascade(label = "File", menu = filemenu)

    editmenu = Menu(self.menubar, tearoff = 0)
    editmenu.add_command(label = "Undo", command = self.doNothing)

    editmenu.add_separator()

    editmenu.add_command(label = "Cut", command = self.doNothing)
    editmenu.add_command(label = "Copy", command = self.doNothing)
    editmenu.add_command(label = "Paste", command = self.doNothing)
    editmenu.add_command(label = "Delete", command = self.doNothing)
    editmenu.add_command(label = "Select All", command = self.doNothing)

    self.menubar.add_cascade(label = "Edit", menu = editmenu)
    self.helpmenu = Menu(self.menubar, tearoff = 0)
    self.helpmenu.add_command(label = "Help Index", command = self.doNothing)
    self.helpmenu.add_command(label = "About...", command = self.doNothing)
    self.menubar.add_cascade(label = "Help", menu = self.helpmenu)

    # First Row:
    self.welcome_message = Text(self, wrap = "word", width = 50, padx = 10, pady = 2.5)
    self.welcome_message.insert(INSERT, str(self.preseed))
    self.welcome_message.grid(row = 1, column = 0, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = 5, sticky = "N, S, E, W")

    self.scrollbar_vertical = Scrollbar(self)
    self.scrollbar_vertical.config(command = self.welcome_message.yview)
    self.scrollbar_vertical.grid(row = 1, column = 1, rowspan = 1, columnspan = 1, sticky = "N, S, W")


    # Last Row:
    self.next = Button(self, text = "Next", command = self.start)
    self.next.grid(row = 50, column = 0, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = 5, sticky = "E")

  @staticmethod
  def doNothing(self):
    filewin = Toplevel(self)
    button = Button(filewin, text = "Do nothing button")
    button.pack()

  @property
  def preseed(self):
    seed = textwrap.dedent(
      f"""
      Welcome to Vault Cipher's Open Source Server Provisioning toolset.
      """.rstrip()
      )

    return seed

  def start(self):
    self.destroy()
    display = HostWindow()
    
def main():
  interface = Tk()
  display = WelcomeWindow()
  interface.config(menu = display.menubar)
  # interface.geometry("500x500")
  interface.mainloop()

if __name__ == "__main__":
  main()