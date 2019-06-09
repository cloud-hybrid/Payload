import os
import sys
import time
import textwrap
import subprocess
from tkinter import *

from tkinter import filedialog

import threading

# Transfer ssh-based commands to Host()

# Create a an authorized_keys file locally and then upload server. 

class HostWindow(Frame):
  def __init__(self):
    super().__init__()

    self.master.title("Remote-Host Configuration")
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
    self.message = Text(self, wrap = "word", width = 30, height = 10, padx = 10, pady = 2.5)
    self.message.insert(INSERT, str(self.information))
    self.message.grid(row = 0, column = 0, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = 5, sticky = "N, S, E, W")

    self.scrollbar_vertical = Scrollbar(self)
    self.scrollbar_vertical.config(command = self.message.yview)
    self.scrollbar_vertical.grid(row = 0, column = 1, rowspan = 1, columnspan = 1, sticky = "N, S, W")

    self.host_frame = Frame(self)
    self.host_frame.grid(row = 0, column = 3, rowspan = 1, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = (7.5, 15), sticky = "N, S, E, W")

    self.IP_label = Label(self.host_frame, text = "Host IP Address")
    self.IP_label.pack(side = "top", fill = X)
    self.IP_address = Entry(self.host_frame, justify = "center")
    self.IP_address.pack(side = "top", fill = X)

    self.username_label = Label(self.host_frame, text = "Username")
    self.username_label.pack(side = "top", fill = X, pady = (10, 0))
    self.username = Entry(self.host_frame, justify = "center")
    self.username.pack(side = "top", fill = X)

    self.password_label = Label(self.host_frame, text = "Password")
    self.password_label.pack(side = "top", fill = X, pady = (10, 0))
    self.password = Entry(self.host_frame, justify = "center", show = "*")
    self.password.pack(side = "top", fill = X)

    self.SSH_label = Label(self.host_frame, text = "SSH Key Location")
    self.SSH_label.pack(side = "top", fill = X, pady = (10, 0))
    self.SSH_key = Button(self.host_frame, text = "Browse", command = self.fileBrowse)
    self.SSH_key.pack(side = "top")
    self.SSH_entry = Entry(self.host_frame, justify = "center")
    self.SSH_entry.pack(side = "top", fill = X, pady = (5, 0))

    # Last Row:
    self.home = Button(self, text = "Home", command = self.home)
    self.home.grid(row = 50, column = 0, rowspan = 14, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = (15, 5), sticky = "W")

    self.configure = Button(self, text = "Configure", command = self.hyperThread)
    self.configure.grid(row = 50, column = 3, rowspan = 14, columnspan = 1, ipady = 0, ipadx = 0, pady = 5, padx = 5, sticky = "")

  def hyperThread(self):
    threading.Thread(target = self.transerSSHKey).start()

  def home(self):
    from Payload.Vault.GUI.MainWindow import MainWindow

    self.destroy()
    display = MainWindow()

  def interactive_shell(self):
    ip_address = self.IP_address.get()
    username = self.username.get()
    password = self.password.get()

    command = f"plink {ip_address} -l {username} -pw {password} "   
    print(command)
    threading.Thread(target = subprocess.run(command))

  def fileBrowse(self):
    filename = filedialog.askopenfilename()
    self.SSH_entry.insert(0, str(filename))

  @staticmethod
  def doNothing(self):
    filewin = Toplevel(self)
    button = Button(filewin, text = "Do nothing button")
    button.pack()

  @staticmethod
  def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

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
