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

from Payload.Vault.Installation.Progress import Progress
from Payload.Vault.Installation.Preseed import Preseed
from Payload.Vault.Installation.Installer import Installer
from Payload.Vault.Shell.Terminal import Terminal
from Payload.Vault.Shell.Display import Display
from Payload.Vault.Shell.CMD import CMD
from Payload.Vault.Network.Host import Host
from Payload.Vault.Network.VPS import VPS
from Payload.Vault.Network.Gateway import Gateway
from Payload.Vault.Network.Proxy import Proxy

vDIRECTORY = "/mnt/vCloud-1/Infrastructure/Virtual-Machines/"

def resource_path(relative_path):
  base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
  return os.path.join(base_path, relative_path)

def main():
  source = resource_path("Bionic-Server.iso")

  v_Host = Host(input.h_User, input.h_IP, input.h_OS, input.Gmail)
  v_VPS = VPS(input.v_User, input.v_Password, input.v_IP, input.v_Type, input.v_RAM, input.v_CPU, input.Domain, input.SSL)
  v_VPS.hostname = v_VPS.name 
  v_Gateway = Gateway(input.g_User, input.g_IP)
  v_Proxy = Proxy(input.p_User, input.p_IP)
  v_Preseed = Preseed(v_VPS.user, v_VPS.password, v_VPS.IP, Preseed.HOSTNAME)
  Preseed.HOSTNAME = v_VPS.hostname

  v_Installer = Installer(source, v_VPS.RAM, v_VPS.CPUs, v_VPS.IP)
  v_Installer.install()

  CMD().execute(f"""ssh snow@192.168.1.5 -t "sudo {vDIRECTORY}create-VPS.sh" """)

  v_Gateway.updateDNS(v_VPS)
  v_Gateway.createUser(v_VPS)

  v_Proxy.updateProxy(v_VPS)

  if v_Host.OS == "linux":
    v_VPS.start(v_VPS.hostname)

  if v_VPS.type == "lamp_wordpress":
    v_Installer.install_wordpress_database(v_VPS.password, v_VPS.IP)

  if v_VPS.FQDN != "N/A" and v_VPS.FQDN != None:
    command = f"""ssh {v_Proxy.user}@{v_Proxy.IP} "sudo wget -O /tmp/add-domain.py 'https://unixvault.com/proxy/add-domain.py' --no-check-certificate && sudo chmod +x /tmp/add-domain.py && sudo /tmp/add-domain.py {v_VPS.hostname} {v_VPS.FQDN}" """
    Terminal(command).run()

  # if v_Host.OS == "Windows":
  #   v_Host.email_private_key_windows(v_Host)
  # else:
  #   v_Host.email_private_key(v_Host)
  
  v_Host.email_private_key_windows(v_Host)


class GUI(Frame):
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
    self.v_Password_entry.insert(0, "Knowledge")
    self.v_Password_button = Button(self, text = "Show", command = self.showPassword)
    self.v_Password_button.grid(row = 1, column = 3, padx = 5)

    self.v_IP = Label(self, text = "VPS IP-Address")
    self.v_IP.grid(row = 2, column = 0, columnspan = 1, pady = 4, padx = 5, ipadx = 5)
    self.v_IP_entry = Entry(self, justify = "center")
    self.v_IP_entry.grid(row = 3, column = 0, columnspan = 1, padx = 5, sticky = E+W+S+N)

    self.activate = Button(self, text = "Execute", command = self.executePayload)
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
    v_User = self.v_User_entry.get()
    v_Password = self.v_Password_entry.get()
    v_IP = self.v_IP_entry.get()

    input.v_User = v_User
    input.v_Password = v_Password
    input.v_IP = v_IP

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

  parser.add_argument("--Gmail", nargs = "+", type = str, default = ["development.cloudhybrid@gmail.com", "Kn0wledge!", "jsanders4129@gmail.com"], required = False)

  parser.add_argument("--GUI", type = str, default = True, required = False)

  input = parser.parse_args()

  if input.GUI == True:
    Display().header()
    Display().copyright()

    interface = Tk()
    logo = resource_path("Vault.ico")
    interface.iconbitmap(logo)
    display = GUI()
    interface.mainloop()
  else:
    if input.v_IP or input.v_User == None:
      print("Invalid Input")
      quit()
    else:
      print("Executing Injections".center(os.get_terminal_size().columns))
      main()
