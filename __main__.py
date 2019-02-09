import os
import sys
import subprocess
import textwrap
import argparse
import time

from argparse import ArgumentParser
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE
from subprocess import *

from Payload.Vault.Installation.Progress import Progress
from Payload.Vault.Installation.Preseed import Preseed
from Payload.Vault.Installation.Installer import Installer
from Payload.Vault.Shell.Terminal import Terminal
from Payload.Vault.Shell.Display import Display
from Payload.Vault.Network.Host import Host
from Payload.Vault.Network.VPS import VPS
from Payload.Vault.Network.Gateway import Gateway
from Payload.Vault.Network.Proxy import Proxy

def resource_path(relative_path):
  base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
  return os.path.join(base_path, relative_path)


def main():
  Display().header()
  Display().copyright()
  
  v_Host = Host(input.h_User, input.h_IP, input.h_OS, input.Gmail)
  v_VPS = VPS(input.v_User, input.v_Password, input.v_IP, input.v_Type, input.v_RAM, input.v_CPU, input.Domain, input.SSL)
  v_VPS.hostname = v_VPS.name 
  v_Gateway = Gateway(input.g_User, input.g_IP)
  v_Proxy = Proxy(input.p_User, input.p_IP)
  v_Preseed = Preseed(v_VPS.user, v_VPS.password, v_VPS.IP, v_VPS.hostname)

  v_Installer = Installer(v_Preseed, v_VPS.RAM, v_VPS.CPUs, v_VPS.IP)
  v_Installer.install(v_VPS.type)

  if v_VPS.type == "minimal" or v_VPS.type == "basic":
    if v_Host.OS == "linux":
      Progress(1350).display()
    elif v_Host.OS == "windows":
      Progress(1400).display()
    else: 
      print("Invalid Host Operating System")
      quit()

  elif v_VPS.type == "lamp" or v_VPS.type == "lamp_wordpress":
    if v_Host.OS == "linux":
      Progress(1500).display()
    elif v_Host.OS == "windows":
      Progress(1650).display()
    else: 
      print("Invalid Host Operating System")
      quit()
  else:
    print("Invalid VPS().Type")
    quit()

  if v_Host.OS == "linux":
    v_VPS.start(v_VPS.hostname)
  elif v_Host.OS == "windows":
    v_VPS.remoteStart(v_VPS.hostname, "snow", "192.168.1.5")

  v_Gateway.updateDNS(v_VPS)
  v_Gateway.createUser(v_VPS)

  v_Proxy.update_Proxy(v_VPS)

  if v_VPS.type == "lamp_wordpress":
    v_Installer.install_wordpress_database(v_VPS.password, v_VPS.IP)

  if v_VPS.FQDN != "N/A" and v_VPS.FQDN != None:
    command = f"""ssh {v_Proxy.user}@{v_Proxy.IP} "sudo wget -O /tmp/add-domain.py 'https://unixvault.com/proxy/add-domain.py' --no-check-certificate && sudo chmod +x /tmp/add-domain.py && sudo /tmp/add-domain.py {v_VPS.hostname} {v_VPS.FQDN}" """
    Terminal(command).run()
    
  v_Host.email_private_key_windows(v_Host)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog = "Vault Payload", argument_default = argparse.SUPPRESS)

  parser.add_argument("-D", "--Domain", type = str, default = None, required = False)
  parser.add_argument("--SSL", type = int, default = False, required = False)

  parser.add_argument("--v_User", type = str, required = True)
  parser.add_argument("--v_Password", type = str, default = "Knowledge", required = False)
  parser.add_argument("--v_IP", type = str, required = True)
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

  input = parser.parse_args()

  main()
