#!/usr/bin/python3.7
# ........................................................................... #
# (c) 2019, Jacob B. Sanders <development.cloudhybrid@gmail.com>
# GNU General Public License v3.0: https://opensource.org/licenses/GPL-3.0

METADATA = {
  "Module" : "VirtualizationHost",
  "Package" : "IaaS",
  "Version" : "0.2",
  "Status": "beta"
  }

DOCUMENTATION = """
Module: VirtualizationHost
Author: Jacob B. Sanders (@cloud-hybrid)
Summary: Module used for configuring KVM-capable hosts.
Documentation: https://vaultcipher.com/

@Description:
 - TBD

@Dependencies
  - tkinter
  - memory_profiler
  - libmysqlclient-dev
  - mysql-connector-python-rf

@Development

"""

EXAMPLES = """
- TBD
"""

import os
import sys
import shlex
import subprocess
import textwrap
import argparse

import cProfile
import threading
import pstats
import io

# from memory_profiler import profile

# from tkinter import *
from argparse import ArgumentParser

from Payload.Vault.IaaS.ExecutionHost import ExecutionHost
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
from Payload.Vault.Database.Connection import Connection
from Payload.Vault.Network.Scanner import Scanner

vDIRECTORY = "/mnt/Virtual-Machines/"

def resource_path(relative_path):
  base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
  return os.path.join(base_path, relative_path)

def main():
  vps_image = resource_path("Bionic-Server.iso")

  # database = Connection(
  #   input.sql_username, 
  #   input.sql_password,
  #   input.sql_server,
  #   input.sql_database
  # )

  # result = database.queryAll()
  # subnet = database.incrementIP()
  # VPS_IP = database.network + str(subnet)

  setup = input("Run First Time Setup on the Virtualization Host? (Y/N): ")
  if str(setup).upper() == "Y":
    host = ExecutionHost(
      username = shell_input.virtualization_host_username,
      email = shell_input.virtualization_host_email,
      password = shell_input.virtualization_host_password,
      address = shell_input.virtualization_host_address
    )

    if host.executing_platform == "Linux" or host.executing_platform == "Darwin" and host.sshKeyCheck() == True:
      host.sshCopyID()
    elif host.sshKeyCheck() == False:
      host.sshKeyGeneration()
      time.sleep(3)
      host.sshCopyID()

    print("Host Cores: " + str(host.Cores))
    print("Virtualization Capable: " + str(host.checkVirtualizationCompatability()))
    print("Acceleration Capable: " + str(host.checkAccelerationCompatability()))

    print("Updated: " + str(host.updateVirtualizationHost()))
    print("Upgraded: " + str(host.upgradeVirtualizationHost()))

    print("KVM Package Installed: " + str(host.installVirtualizationSoftware()))
    print("KVM Package Enabled: " + str(host.enableVirtualizationSoftware()))


  # print("Host Network Interfaces: " + str(host.NetworkInterfaces))

  # print("Network Configuration: " + str(host.NetworkConfiguration))
  # if host.NetworkConfiguration == False:
  #   host.configureNetworkBridge()

  # print("Creating RSA and Directory Files: " + str(host.createRSAKey()))
  # print("Setting .SSH Permissions: " + str(host.setSSHPermissions()))

  # else:
  #   if Scanner.pingNode(input.remote_host_IP):
  #     pass
  #   else:
  #     sys.exit("Failure: Remote Host Unreachable")

    # remote_host = Host(
    #   user = input.remote_host_user, 
    #   password = input.remote_host_password,
    #   server = input.remote_host_IP, 
    #   local_OS = input.local_host_OS,
    #   remote_OS = input.remote_host_OS,
    #   email_sender = input.email[0],
    #   email_recipient = input.email[2]
    # ) 

  # vps_type = "SQL"

  # if vps_type == "SQL":
    # ip_address = input("IP Address: ")
    # ip_address = "192.168.0.80"

    # vps = VPS(
    #   "sql", 
    #   "Kn0wledge!", 
    #   ip_address, 
    #   "SQL", 
    #   input.vps_RAM, 
    #   input.vps_CPU, 
    #   input.Domain, 
    #   input.SSL,
    #   hostname = "SQL-Server")

  # vps = VPS(
  #   input.vps_username, 
  #   input.vps_password, 
  #   VPS_IP, 
  #   input.vps_type, 
  #   input.vps_RAM, 
  #   input.vps_CPU, 
  #   input.Domain, 
  #   input.SSL)

  # database.addVPS(
  #   input.vps_username, 
  #   input.vps_username, 
  #   input.vps_type,
  #   VPS_IP, 
  #   input.vps_RAM, 
  #   input.vps_CPU, 
  #   vps.hostname, 
  #   input.SSL, 
  #   input.email[2]
  # )
  
  # database.disconnect()

  #Preseed.HOSTNAME = vps.hostname
  
  # gateway = Gateway(input.gateway_user, input.gateway_server)
  # proxy = Proxy(input.proxy_user, input.proxy_server)

  # preseed = Preseed(
  #   vps.user,
  #   vps.password,
  #   vps.IP,
  #   Preseed.HOSTNAME
  # )

  # sys.stdout.write(f"{Preseed.HOSTNAME}".center(os.get_terminal_size().columns))

  # installer = Installer(vps_image, vps.RAM, vps.CPUs)

  # installer.install(
  #   vps.type,
  #   vps.user,
  #   vps.password,
  #   vps.IP
  # )

  # CMD().execute(f"""ssh snow@192.168.0.1 -t "sudo {vDIRECTORY}create-VPS.sh" """)

  # command = f"sudo {vDIRECTORY}create-VPS.sh"
  # subprocess.call(shlex.split(command))
  
  # Progress(750).display()

  # gateway.updateDNS(vps)
  # gateway.createUser(vps)

  # proxy.updateProxy(vps)

  # if vps.type == "Wordpress":
  #   installer.install_wordpress_database(vps.password, vps.IP)
  # 
  # if vps.FQDN != "N/A" and vps.FQDN != None:
  #   command = f"""ssh {proxy.user}@{proxy.IP} "sudo wget -O /tmp/add-domain.py 'https://unixvault.com/proxy/add-domain.py' --no-check-certificate && sudo chmod +x /tmp/add-domain.py && sudo /tmp/add-domain.py {vps.hostname} {vps.FQDN}" """
  #   Terminal(command).run()
  
  # remote_host.emailPrivateKey_windows()

  sys.stdout.write("Payload(s) Delivered".center(os.get_terminal_size().columns))

if __name__ == "__main__":
  # v_profiler = cProfile.Profile()
  # v_profiler.enable()

  parser = argparse.ArgumentParser(prog = "Vault Payload", argument_default = argparse.SUPPRESS)

  parser.add_argument("-L", "--Local", type = bool, default = True, required = False)

  parser.add_argument("-D", "--Domain", type = str, default = None, required = False)
  parser.add_argument("--SSL", type = int, default = False, required = False)

  parser.add_argument("--vps_username", type = str, default = "bionic-test-1006",  required = False)
  parser.add_argument("--vps_password", type = str, default = "Knowledge", required = False)
  parser.add_argument("--vps_type", type = str, default = "minimal", required = False)
  parser.add_argument("--vps_RAM", type = int, default = 512, required = False)
  parser.add_argument("--vps_CPU", type = int, default = 1, required = False)

  parser.add_argument("--sql_username", type = str, default = "root", required = False)
  parser.add_argument("--sql_password", type = str, default = "Kn0wledge!", required = False)
  parser.add_argument("--sql_server", type = str, default = "192.168.1.75", required = False)
  parser.add_argument("--sql_database", type = str, default = "V_PAYLOAD", required = False)

  parser.add_argument("--virtualization_host_username", type = str, default = "snow", required = False)
  parser.add_argument("--virtualization_host_email", type = str, default = "development.cloudhybrid@gmail.com", required = False)
  parser.add_argument("--virtualization_host_password", type = str, default = "Kn0wledge!", required = False)
  parser.add_argument("--virtualization_host_address", type = str, default = "192.168.0.1", required = False)

  parser.add_argument("--remote_host_user", type = str, default = "snow", required = False)
  parser.add_argument("--remote_host_password", type = str, default = "Kn0wledge!", required = False)
  parser.add_argument("--remote_host_IP", type = str, default = "192.168.0.1", required = False)
  parser.add_argument("--remote_host_OS", type = str, default = "linux", required = False)
  parser.add_argument("--local_host_OS", type = str, default = "windows", required = False)

  parser.add_argument("--proxy_user", type = str, default = "snow", required = False)
  parser.add_argument("--proxy_server", type = str, default = "192.168.1.60", required = False)

  parser.add_argument("--gateway_user", type = str, default = "snow", required = False)
  parser.add_argument("--gateway_server", type = str, default = "192.168.0.5", required = False)

  # --email format: [{mail address to be used as sender}, {password used to access sender's mail address}, {recipient's maill address}]
  parser.add_argument("--email", nargs = "+", type = str, default = [
    "development.cloudhybrid@gmail.com", 
    "Kn0wledge!", 
    "jsanders4129@gmail.com"
  ], required = False)

  parser.add_argument("--GUI", type = str, default = False, required = False)

  shell_input = parser.parse_args()

  main()
