import sys
import textwrap
from tkinter import *

import inspect
from inspect import getmembers

import tkinter

from Payload.Vault.GUI.HostWindow import HostWindow
from Payload.Vault.GUI.NetworkScannerWindow import NetworkScannerWindow

from tkinter import filedialog



import threading

class MainWindow(Frame):
  HOST_IP_STATUS = False
  HOST_SETUP_STATUS = False
  NETWORK_STATUS = False

  def __init__(self, network_status = None, host_status = None):
    super().__init__()
    # self.config(background = "red")

    self.network_status = network_status
    self.host_status = host_status

    if self.network_status == True:
      MainWindow.NETWORK_STATUS = True

    if self.host_status == True:
      MainWindow.HOST_SETUP_STATUS = True

    self.master.title("vPayload")
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

    self.menubar.add_cascade(label = "Test")
    # self.grip = Label(self, bitmap = "gray25")
    # self.menubar.add_cascade(self.grip)

    self.master.config(menu = self.menubar)

    # First Row:
    self.message = Text(self, wrap = "word", width = 30, height = 20, padx = 10, pady = 2.5)
    self.message.insert(INSERT, str(self.information))
    self.message.grid(row = 0, column = 0, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = 5, sticky = "N, S, E, W")

    self.scrollbar_vertical = Scrollbar(self)
    self.scrollbar_vertical.config(command = self.message.yview)
    self.scrollbar_vertical.grid(row = 0, column = 1, rowspan = 1, columnspan = 1, sticky = "N, S, W")

    # --> Sub-Frame
    self.main_frame = Frame(self)
    self.main_frame.grid(row = 0, column = 3, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = (7.5, 0), sticky = "N, S, E, W")

    self.key_creation = Button(self.main_frame, text = "Key Creation", command = self.doNothing)
    self.key_creation.pack(side = "top", padx = (5, 5), pady = (0, 10))

    self.network_scanner = Button(self.main_frame, text = "Network Scan", command = self.displayNetworkScannerWindow)
    self.network_scanner.pack(side = "top", padx = (5, 5), pady = (10, 10))

    self.host_configuration = Button(self.main_frame, text = "Host Injection", command = self.displayHostWindow)
    self.host_configuration.pack(side = "top", padx = (5, 5), pady = (10, 10))

    self.SQL_setup = Button(self.main_frame, text = "Database", command = self.doNothing)
    self.SQL_setup.pack(side = "top", padx = (5, 5), pady = (10, 10))

    self.VPS_provisioning = Button(self.main_frame, text = "VPS Setup", command = self.doNothing)
    self.VPS_provisioning.pack(side = "top", padx = (5, 5), pady = (10, 10))


    # Indicator Frame
    self.indicator_frame = Frame(self)
    self.indicator_frame.grid(row = 0, column = 4, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = (0, 7.5), sticky = "N, S, E, W")

    if self.network_status == None or self.network_scanner == False and MainWindow.NETWORK_STATUS != True:
      self.network_status_img = PhotoImage(file = "C:\\Users\\Development\\Documents\\Payload\\Vault\\Assets\\Images\\indicator-green-25px.png")
    elif self.network_status == True or MainWindow.NETWORK_STATUS == True:
      self.network_status_img = PhotoImage(file = "C:\\Users\\Development\\Documents\\Payload\\Vault\\Assets\\Images\\indicator-green-25px.png")

    self.network_status_label = Label(self.indicator_frame, image = self.network_status_img)

    self.network_status_label.pack(side = "top", padx = (5, 5), pady = (0, 0))

    if self.host_status == None or self.host_status == False and MainWindow.HOST_SETUP_STATUS != True:
      self.host_status_img = PhotoImage(file = "C:\\Users\\Development\\Documents\\Payload\\Vault\\Assets\\Images\\indicator-green-25px.png")
    elif self.host_status == True or MainWindow.HOST_SETUP_STATUS == True:
      self.host_status_img = PhotoImage(file = "C:\\Users\\Development\\Documents\\Payload\\Vault\\Assets\\Images\\indicator-green-25px.png")
    
    self.host_status_label = Label(self.indicator_frame, image = self.host_status_img)

    self.host_status_label.pack(side = "top", padx = (5, 5), pady = (15, 0))

    # Last Row:

    self.close = Button(self, text = "close", command = self.master.destroy)
    self.close.grid(row = 50, column = 0, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = (15, 5), sticky = "W")

  def hyperThread(self):
    pass

  @staticmethod
  def doNothing(self):
    filewin = Toplevel(self)
    button = Button(filewin, text = "Do nothing button")
    button.pack()

  @property
  def information(self):
    property = textwrap.dedent(
      f"""
      Requirements:
      - Local-Host needs plink installed.
      - Remote-Host needs to have SSH enabled.
      - Uses port 22
      - SSH key created using Open SSH.
      - Need Root access.
      [ ] Create SSH key
      [ ] Create option to specify port
      """.rstrip()
      )

    return property

  def displayHostWindow(self):
    self.destroy()
    display = HostWindow()

  def displayNetworkScannerWindow(self):
    self.destroy()
    display = NetworkScannerWindow()

  def home(self):
    from Payload.Vault.GUI.MainWindow import MainWindow

    self.destroy()
    display = MainWindow()