#!/usr/bin/python3.7
# ........................................................................... #
# (c) 2019, Jacob B. Sanders <development.cloudhybrid@gmail.com>
# GNU General Public License v3.0: https://opensource.org/licenses/GPL-3.0

"""
@General-Information
  - Creator: Snow
  - Contributors: N/A
  - Website: https://vaultcipher.com
  - Description: N/A

@Objects
  ↳ Scanner         - Type: (Object)      - Required  : (N/A)
      ↳ @Arguments
          ↳ CIDR                          - Required	: (String)      - Default: (N/A)
              ↳	Note: This variable is passed into the self.network variable, 
                      ipaddress.ip_network() function. 
              ↳ Example: 192.168.1.0/24
      ↳ @Variables
          ↳ network                       - Required	: (Array)      - Default: ipaddress.ip_network(self.CIDR)
              ↳	Note: Creates a list of IP Addresses in a given range
      ↳ @Functions
          ↳ scan()      - Attempts to ping each IP on the network given a range
                          and appends/prints any online nodes.
                        - Calls HyperThread to create a seperate thread to display progress bar.

  ↳ HyperThread     - Type: (Thread)      - Required  : (threading.Thread)
      ↳ @Arguments
          ↳ Name                          - Required	: (String)      - Default: (N/A)
              ↳	Note: Arbitrary name to use for printing thread.info() information
      ↳ @Functions
          ↳ run()       - Runs implicitly from HyperThread's parent class
                          and appends/prints any online nodes.
                        - Creates a seperate thread to display progress bar.

@Documentation
  ipaddress.ip_network()          - https://docs.python.org/3/howto/ipaddress.html
  subprocess()                    - https://docs.python.org/3/library/subprocess.html
  threading                       - https://docs.python.org/3/library/threading.html
"""

import sys
import time
import subprocess
import ipaddress
import threading

from subprocess import Popen, PIPE

import socket
from contextlib import closing

# from dataclasses import dataclass, field
from typing import List

class Scanner(object):
  @property
  def status(self):
    status = False
    return status

  def __init__(self, CIDR: str):
    self.CIDR = CIDR
    self.network = ipaddress.ip_network(self.CIDR)
    self.addresses = []

  # def debug(self):
  #   if self.CIDR == None:
  #     print("ERROR: CIDR attribute has no input")
  #   else:
  #     print(f"CIDR Network: {self.CIDR}")

  #   # Hides the console window
  #   info = subprocess.STARTUPINFO()
  #   info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
  #   info.wShowWindow = subprocess.SW_HIDE

  #   for node in range(len(hosts)):
  #     output = subprocess.Popen(
  #       ['ping', '-n', '1', '-w', '500',str(hosts[node])],
  #       stdout=subprocess.PIPE, 
  #       startupinfo=info
  #     ).communicate()[0]

  #     if "Destination host unreachable" in output.decode('utf-8'):
  #       print(str(hosts[node]), "is Offline")
  #     elif "Request timed out" in output.decode('utf-8'):
  #       print(str(hosts[node]), "is Offline")
  #     else:
  #       print(str(hosts[node]), "is Online")

  def scan(self):
    Scanner.status = True

    HyperThread("Display").start()

    hosts = list(self.network.hosts())

    for node in range(len(hosts)):
      output = subprocess.Popen(
        ['ping', '-n', '1', '-w', '500',str(hosts[node])],
        stdout = subprocess.PIPE
      ).communicate()[0]

      if "Destination host unreachable" in output.decode('utf-8'):
        continue
      elif "Request timed out" in output.decode('utf-8'):
        continue
      else:
        # print(str(hosts[node]), "is Online" + (" " * 10))
        self.addresses.append(str(hosts[node]))

    Scanner.status = False

    print("Network Scan Complete...   " + "✓" + " " * 10)
    time.sleep(1.0)

    return self.addresses

  def scan_online_nodes(self):
    hosts = list(self.network.hosts())

    # Hides the console window
    # info = subprocess.STARTUPINFO()
    # info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # info.wShowWindow = subprocess.SW_HIDE

    for node in range(len(hosts)):
      output = subprocess.Popen(
        ['ping', '-n', '1', '-w', '500', str(hosts[node])],
        stdout = subprocess.PIPE
      ).communicate()[0]

      if "Destination host unreachable" in output.decode('utf-8'):
        continue
      elif "Request timed out" in output.decode('utf-8'):
        continue
      else:
        print(str(hosts[node]), "is Online")

  @staticmethod
  def pingNode(node: str):
    # Hides the console window
    # info = subprocess.STARTUPINFO()
    # info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # info.wShowWindow = subprocess.SW_HIDE

    output = subprocess.Popen(
      ['ping', '-n', '1', '-w', '500', node],
      stdout = subprocess.PIPE
    ).communicate()[0]

    if "Destination host unreachable" in output.decode('utf-8'):
      return False
    elif "Request timed out" in output.decode('utf-8'):
      return False
    else:
      print(node + " is Online")
      return True
  
# @dataclass
# class Ports(object):
#   PUBLIC_IP: str = "0.0.0.0"
#   HTTP: int = 80
#   HTTP_PROXY: int = 8080
#   HTTPS: int = 443
#   HTTPS_PROXY: int = 4443
#   FTP_COMMAND: int = 20
#   FTP_DATA: int = 21
#   SSH: int = 22
#   SSH_PROXY: int = 22
#   DNS: int = 53
#   SQL = 1433
#   RDP: int = 3389
#   VSFTPD: int = 49000

#   def opened(self, address):
#     open_ports = {}
#     closed_ports = {}

#     if Ports().check(self.HTTP, address) == True:
#       open_ports.update({"HTTP" : str(self.HTTP)})
    
#     if Ports().check(self.HTTP_PROXY, address):
#       open_ports.update({"HTTP Proxy" : str(self.HTTP_PROXY)})
#     if Ports().check(self.HTTPS, address):
#       open_ports.update({"HTTPS" : str(self.HTTPS)})
#     if Ports().check(self.HTTPS_PROXY, address):
#       open_ports.update({"HTTPS Proxy" : str(self.HTTPS_PROXY)})
#     if Ports().check(self.FTP_COMMAND, address):
#       open_ports.update({"FTP Command" : str(self.FTP_COMMAND)})
#     if Ports().check(self.FTP_DATA, address):
#       open_ports.update({"FTP Data" : str(self.FTP_DATA)})
#     if Ports().check(self.SSH, address):
#       open_ports.update({"SSH" : str(self.SSH)})
#     if Ports().check(self.SSH_PROXY, address):
#       open_ports.update({"SSH Proxy" : str(self.SSH_PROXY)})
#     if Ports().check(self.DNS, address):
#       open_ports.update({"DNS" : str(self.DNS)})
#     if Ports().check(self.SQL, address):
#       open_ports.update({"SQL" : str(self.SQL)})
#     if Ports().check(self.RDP, address):
#       open_ports.update({"RDP" : str(self.RDP)})
#     if Ports().check(self.VSFTPD, address):
#       open_ports.update({"VSFTPD" : self.VSFTPD})

#     print("\n" + "Port Scan Complete ✓")

#     return open_ports

#   def check(self, port: int, public_ip: str):
#     host = public_ip
#     connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     connection.settimeout(3)
#     result = connection.connect_ex((host,port))
#     if result == 0:
#       connection.close()
#       print(f"Port {port}: ✓")
#       return True
#     else:
#       connection.close()
#       print(f"Port {port}: X")
#       return False

class HyperThread(threading.Thread):
  def __init__(self, name):
    super(HyperThread, self).__init__()
    self.name = name

  # self.run() gets ran implicitly from HyperThread's parent class
  def run(self):
    # print(f"Initiating New Thread: {self.name}")
    while Scanner.status == True:
      for iterator in '|/-\\': 
        sys.stdout.write("Network Scan in Progress...   " + iterator + "\r")
        time.sleep(0.35)
        sys.stdout.flush()

# Example:
def main():
  print(Scanner("192.168.1.0/24").scan())

  ports = Ports()
  opened_ports = ports.opened()

  print("Opened Ports: ")
  print(opened_ports)

if __name__ == "__main__":
  main()
    