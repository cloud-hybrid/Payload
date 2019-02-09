"""
@Infrastructure
  ?   Permissions      - /tmp must be writable by user running the        - Required  : (Type)
                          - installation.
                       - User must be a part of the KVM group.
                       - [--disk path=...] directory must be owned by User.
@Documentation
  [To-Do]   - Change Preseed variable name to Injection.
  [To-Do]   - Change @property, command to different, more descriptive name.
  [To-Do]   - Change install() to vps()
"""

import os
import sys
import time
import textwrap
import tempfile
import subprocess
import pkgutil

import threading as Threading
from multiprocessing import Process, Queue

from Payload.Vault.Shell.Terminal import Terminal
from Payload.Vault.Shell.CMD import CMD
from Payload.Vault.Installation import Source

from Payload.Vault.Installation.Progress import Progress
from Payload.Vault.Installation.Preseed import Preseed

EXECUTIONS = {
  "VPS" : "Installer(self).VPS(self)", 
  "ISO": "Installer(self).ISO(self)", 
  "PRESEED" : "Installer(self).PRESEED(self)", 
  "PERMISSIONS" : "Installer(self).PERMISSIONS(self)"
}

vDIRECTORY = "/mnt/vCloud-1/Infrastructure/Virtual-Machines/"

class Installer(object):
  @staticmethod
  def aSYNCHRONIZE(self):
    STACK = Queue()

    for index, execution in EXECUTIONS.items():
      STACK.put(execution)
      vThread = Threading.Thread(target = eval(execution), args = ())
      vThread.daemon = True
      vThread.start()

  @staticmethod
  def VPS(self):
    directory = "C:\\Users\\Development\\Documents\\Payload\\Vault\\Installation\\Source\\"
    file = "create-VPS.sh"
    script = directory + file

    script = open(script, "w+")
    script.write(self.kernal)
    script.close()

    with tempfile.NamedTemporaryFile(delete = False) as conversion:
      for line in open(str(directory + file), "rb") :
        line = line.rstrip()
        conversion.write(line + "\n".encode())
    conversion.close()

    os.rename(str(directory + file), str(f"{directory + file}"[:-3] + ".backup"))
    os.rename(conversion.name, f"{directory + file}")
    
    Installer(self).SCP(self, f"{directory + file}", "snow", "192.168.1.5", vDIRECTORY)

  @staticmethod
  def ISO(self):
    directory = "C:\\Users\\Development\\Documents\\Payload\\Vault\\Installation\\Source\\"
    file = "Bionic-Server.iso"

    Installer(self).SCP(self, f"{directory + file}", "snow", "192.168.1.5", vDIRECTORY)

  @staticmethod
  def PRESEED(self):
    directory = "C:\\Users\\Development\\Documents\\Payload\\Vault\\Installation\\Source\\"
    file = "preseed.cfg"
    script = directory + file

    script = open(script, "w+")
    script.write(Preseed("windows", "Knowledge", "192.168.1.101", Preseed.HOSTNAME).preseed_minimal)
    script.close()
  
    Installer(self).SCP(self, f"{directory + file}", "snow", "192.168.1.5", vDIRECTORY)

  @staticmethod
  def SCP(self, source, user, client, directory):
    command = textwrap.dedent(
    f"""
    scp {source} {user}@{client}:{directory}
    """.strip()
    )

    Terminal(command).terminal()
  
  def __init__(self, seed: str, ram = 512, cpu = 1, server = "192.168.1.5"):
    self.Preseed = seed
    self.RAM = ram
    self.vCores = cpu
    self.Server = server

    # self.ttyUser = user
    # self.ttyPassword = password(hashed)

  def install(self, type = None):
    Terminal("""ssh snow@192.168.1.5 -t "sudo chown snow -R /tmp" """).execute()

    # print(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))

    # Installer(self).ISO(self)
    # Installer(self).PRESEED(self)
    # Installer(self).setupPermissions(self)
    # Installer(self).VPS(self)
    Installer(self).aSYNCHRONIZE(self)
  @property
  def kernal(self):
    RAM = self.RAM
    CPU = self.vCores

    PRESEED = "preseed.cfg"
    ISO = "Bionic-Server.iso"
    # ISO = "/tmp/Bionic-Server.iso"
    # ISO = os.path.dirname(os.path.normpath(__file__)) + "\\Source\\" + "Bionic-Server.iso"
    # ISO = os.path.dirname(os.path.realpath(__file__)) + "/_Images/" + "Bionic-Server.iso"
    # ISO = "ftp://192.168.1.60:2121/Bionic-Server.iso"
    # ISO = "http://mirrors.rit.edu/ubuntu/dists/bionic/main/installer-amd64/"
    MIRROR = "http://mirrors.rit.edu/ubuntu/dists/bionic/main/installer-amd64/"
    # DISK = f"{Windows-Test}"

    slash = "\\"

    command = textwrap.dedent(
      f"""virt-install {slash}
      --nographics {slash}
      --name {Preseed.HOSTNAME} {slash}
      --ram {RAM} {slash}
      --disk path={vDIRECTORY}{Preseed.HOSTNAME}.qcow2,size=10 {slash}
      --location "{vDIRECTORY}{ISO}" {slash}
      --initrd-inject={vDIRECTORY}{PRESEED} {slash}
      --vcpus {CPU} {slash}
      --os-type linux {slash}
      --os-variant ubuntu18.04 {slash}
      --autostart {slash}
      --extra-args="console=ttyS0,19200"
      """
    ).strip()

    return command

  @staticmethod
  def PERMISSIONS(self):
    Terminal("""ssh snow@192.168.1.5 -t "sudo chown snow -R /tmp" """).execute()

    Terminal(f"""ssh snow@192.168.1.5 -t "sudo chown snow -R {vDIRECTORY}" """).execute()
    Terminal(f"""ssh snow@192.168.1.5 -t "sudo chmod 755 {vDIRECTORY}" """).execute()
    Terminal(f"""ssh snow@192.168.1.5 -t "sudo chmod a+x {vDIRECTORY}create-VPS.sh" """).execute()

  @staticmethod
  def SCP(self, source, user, client, directory):
    command = textwrap.dedent(
    f"""
    scp {source} {user}@{client}:{directory}
    """.strip()
    )

    # CMD().execute(command)
    Terminal(command).execute()
    
  @staticmethod
  def ttyExecute(server, script):
    """ 
    @Description
    ? Internal method that executes a installer()-related command on a remote location using a file either created or 
        stored locally. The the process is executed by puTTY. puTTY should be pre-installed (create check statement), and 
        password should be passed in by command line before program execution (when creating the Installer() object) and 
        then be hashed.
    @Parameters
    ? Script --> The [os.path.dirname(os.path.normpath(__file__)) + \ + location] of the script.
    """

    tty_command = f"putty -ssh -l snow -pw Kn0wledge! -m {script} {server}"

    Terminal(tty_command).display()
    #CMD().console(tty_command)