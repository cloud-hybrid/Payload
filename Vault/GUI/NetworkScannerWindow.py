import sys
import textwrap
from tkinter import *

from Payload.Vault.GUI.HostWindow import HostWindow

from Payload.Vault.Network.Scanner import Scanner
from Payload.Vault.Network.Scanner import Ports

from tkinter import filedialog

import threading

class NetworkScannerWindow(Frame):
  def __init__(self):
    super().__init__()

    self.master.title("Network Scanner")
    self.pack(fill = BOTH, expand = True)

    self.columnconfigure(0, weight = 1)
    self.rowconfigure(0, weight = 1)
    self.rowconfigure(1, weight = 1)
    self.columnconfigure(2, weight = 1)
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

    self.master.config(menu = self.menubar)

    # First Row:
    self.message = Text(self, wrap = "word", width = 28, height = 10, padx = 10, pady = 2.5)
    self.message.insert(INSERT, str(self.information))
    self.message.grid(row = 0, column = 0, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = 5, sticky = "N, S, E, W")

    self.scrollbar_vertical = Scrollbar(self)
    self.scrollbar_vertical.config(command = self.message.yview)
    self.scrollbar_vertical.grid(row = 0, column = 1, rowspan = 1, columnspan = 1, sticky = "N, S, W")

    # --> Sub-Frame
    self.main_frame = Frame(self)
    self.main_frame.grid(row = 0, column = 3, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = (7.5, 0), sticky = "N, S, E, W")

    self.secondary_frame = Frame(self)
    self.secondary_frame.grid(row = 0, column = 4, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = (0, 0), sticky = "N, S, E, W")

    self.online_nodes_label = Label(self.main_frame, text = "Online Nodes")
    self.online_nodes_label.pack(side = "top", padx = (5, 5), pady = (0, 0))
    self.online_nodes_entry = Entry(self.main_frame, justify = "center")
    self.online_nodes_entry.pack(side = "top", padx = (5, 5), pady = (0, 15))
    self.online_nodes = Button(self.secondary_frame, text = "Scan", command = self.thread_GetOnlineNodes)
    self.online_nodes.pack(side = "top", padx = (5, 5), pady = (17.5, 0))

    self.open_ports_label = Label(self.main_frame, text = "Public IP")
    self.open_ports_label.pack(side = "top", padx = (5, 5), pady = (0, 0))
    self.open_ports_entry = Entry(self.main_frame, justify = "center")
    self.open_ports_entry.pack(side = "top", padx = (5, 5), pady = (0, 15))
    self.open_ports_button = Button(self.secondary_frame, text = "Ports", command = self.thread_GetOpenPorts)
    self.open_ports_button.pack(side = "top", padx = (5, 5), pady = (27.5, 0))

    # --> Sub-Frame 

    # self.network_scanner = Button(self.main_frame, text = "Network Scan", command = self.doNothing)
    # self.network_scanner.pack(side = "top", padx = (5, 5), pady = (15, 15))

    # Last Row:

    self.copy = Button(self, text = "Copy", command = self.copy)
    self.copy.grid(row = 49, column = 0, rowspan = 1, columnspan = 2, ipady = 0, ipadx = 0, pady = 5, padx = (0, 0), sticky = "")

    self.home = Button(self, text = "Home", command = self.home)
    self.home.grid(row = 50, column = 0, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = (15, 5), sticky = "W")

  def hyperThread(self):
    pass

  def thread_GetOnlineNodes(self):
    threading.Thread(target = self.getOnlineNodes).start()
  
  def getOnlineNodes(self):
    nodes = Scanner(f"{self.online_nodes_entry.get()}").scan()
    self.message.insert(INSERT, "\n" + "- Online Nodes: " + str(nodes) + "\n")

  def thread_GetOpenPorts(self):
    threading.Thread(target = self.getOpenPorts).start()
  
  def getOpenPorts(self):
    address = self.open_ports_entry.get()
    ports = Ports()
    opened_ports = ports.opened(address)
    self.message.insert(INSERT, "\n" + "- Opened Ports: " + str(opened_ports) + "\n")

  @staticmethod
  def doNothing(self):
    filewin = Toplevel(self)
    button = Button(filewin, text = "Do nothing button")
    button.pack()

  @property
  def information(self):
    property = textwrap.dedent(
      f""" Network Scanner
      """.rstrip() + "\n"
      )

    return property

  def copy(self):
    contents = self.message.get("1.0", "end-1c")
    self.clipboard_clear()
    self.clipboard_append(contents)

  def displayNetworkScannerWindow(self):
    self.destroy()
    display = HostWindow()

  def displayHostWindow(self):
    self.destroy()
    display = HostWindow()

  def home(self):
    from Payload.Vault.GUI.MainWindow import MainWindow

    self.destroy()
    display = MainWindow()

def main():
  interface = Tk()
  display = MainWindow()
  interface.config(menu = display.menubar)
  # interface.geometry("500x500")
  interface.mainloop()

if __name__ == "__main__":
  main()