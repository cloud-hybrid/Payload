import os
import sys
import subprocess
import textwrap
import argparse
import time

from tkinter import *

from argparse import ArgumentParser
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE
from subprocess import *

from Payload.Host.Windows import Windows

def resource_path(relative_path):
  base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
  return os.path.join(base_path, relative_path)

def main():
  if input.GUI == True:
    interface = Tk()
    logo = resource_path("Vault.ico")
    interface.iconbitmap(logo)
    display = GUI()
    interface.mainloop()

  else:
    if input.IP or input.User == None:
      print("Invalid Input")
      quit()
    else:
      print("Executing Injections".center(os.get_terminal_size().columns))
      main()
      
  source = resource_path("Bionic-Server.iso")

  username = input.User
  address = input.IP
  source = input.Source

  # Create GUI input prompting user for source of RSA key
  Windows().transfer_rsa_key(source, username, address)


class GUI(Frame):
  def __init__(self):
    super().__init__()

    self.master.title("DNS-Payload")
    self.pack(fill = BOTH, expand = True)

    self.columnconfigure(1, weight = 1)
    self.columnconfigure(2, pad = 1)
    
    self.user_label = Label(self, text = "Username")
    self.user_label.grid(row = 0, column = 0, pady = 5, padx = 5)
    self.user_entry = Entry(self, justify = "center")
    self.user_entry.grid(row = 1, column = 0, pady = 5, padx = 5)

    self.activate = Button(self, text = "Transfer", command = self.execute)
    self.activate.grid(row = 1, column = 1, pady = 5, padx = 5)

    self.IP_label = Label(self, text = "Public IP-Address")
    self.IP_label.grid(row = 2, column = 0, pady = 5, padx = 5)
    self.IP_entry = Entry(self, justify = "center")
    self.IP_entry.grid(row = 3, column = 0, pady = 5, padx = 5)

    self.Source_label = Label(self, text = "Source")
    self.Source_label.grid(row = 2, column = 1, pady = 5, padx = 5)
    self.Source_entry = Entry(self, justify = "center")
    self.Source_entry.grid(row = 3, column = 1, pady = 5, padx = 5)
    self.Source_entry.insert(0, "C:\\Users\\Development\\.ssh\\id_rsa.pub")

    self.close = Button(self, text = "Close", command = self.master.destroy)
    self.close.grid(row = 25, column = 1, pady = 5, padx = 5)
    
    self.help_button = Button(self, text = "Help")
    self.help_button.grid(row = 25, column = 0, pady = 5, padx = 5)

  def execute(self):
    input.User = self.user_entry.get()
    input.IP = self.IP_entry.get()
    input.Source = self.Source_entry.get()

    main()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog = "Vault Payload", argument_default = argparse.SUPPRESS)

  parser.add_argument("-D", "--Domain", type = str, default = None, required = False)
  parser.add_argument("--SSL", type = int, default = False, required = False)

  parser.add_argument("--v_User", type = str, default = "bionic",  required = False)
  parser.add_argument("--v_Password", type = str, default = "Knowledge", required = False)
  parser.add_argument("--v_IP", type = str, default = "169.254.0.1", required = False)
  parser.add_argument("--v_Type", type = str, default = "minimal", required = False)
  parser.add_argument("--v_RAM", type = int, default = 512, required = False)
  parser.add_argument("--v_CPU", type = int, default = 1, required = False)

  parser.add_argument("--h_User", type = str, default = "snow", required = False)
  parser.add_argument("--h_IP", type = str, default = "192.168.1.99", required = False)
  parser.add_argument("--h_OS", default = "windows", type = str, required = False)

  parser.add_argument("--p_User", type = str, default = "snow", required = False)
  parser.add_argument("--p_IP", type = str, default = "192.168.1.60", required = False)

  parser.add_argument("--g_User", type = str, default = "snow", required = False)
  parser.add_argument("--g_IP", type = str, default = "192.168.0.5", required = False)

  parser.add_argument("--eMail", nargs = "+", type = str, default = ["development.cloudhybrid@gmail.com", "Kn0wledge!", "development.cloudhybrid@gmail.com"], required = False)

  parser.add_argument("--GUI", type = str, default = True, required = False)

  input = parser.parse_args()

  if input.GUI == True:
    interface = Tk()
    logo = resource_path("Vault.ico")
    interface.iconbitmap(logo)
    display = GUI()
    interface.mainloop()
  else:
    main()