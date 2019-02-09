"""
@Infrastructure
  ↳   Permissions      - /tmp must be writable by user running the        - Required  : (Type)
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
import platform
import textwrap
import subprocess
import pkgutil

from Payload.Vault.Shell.Terminal import Terminal
from Payload.Vault.Shell.CMD import CMD
from Payload.Vault.Installation import Source
from Payload.Vault.Installation.Progress import Progress

DIRECTORY = "C:\\Windows\\Temp\\"

class Installer(object):

  def __init__(self, seed: str, ram = 512, cpu = 1, server = "192.168.1.5"):
    self.Preseed = seed
    self.RAM = ram
    self.vCores = cpu
    self.Server = server

    # self.ttyUser = user
    # self.ttyPassword = password(hashed)

  def install(self, preseed_type, ISO):
    print(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))
    if platform.system() == "Windows":
      self.WINDOWS(preseed_type, ISO)
    elif platform.system() == "Linux":
      self.LINUX(preseed_type)
    else:
      print("Invalid Operating System")
      quit()

  def WINDOWS(self, preseed_type, ISO):
    script = DIRECTORY + "create-VPS.sh"

    script = open(script, "w+")
    script.write(self.kernal)
    script.close()

    time.sleep(2.5)
    print("Payload Installation".center(os.get_terminal_size().columns), end = "\r")

    # Installer(self).SCP(self, ISO, "snow", "192.168.1.5", "/mnt/vCloud-1/Infrastructure/Virtual-Machines/")
    Installer(self).SCP(self, "C:\\Users\\Development\\Documents\\Payload\\Vault\\Installation\\Source\\Bionic-Server.iso", "snow", "192.168.1.5", "/mnt/vCloud-1/Infrastructure/Virtual-Machines/")
    Progress(10).display()

    SEED = str(DIRECTORY + "preseed.cfg")
    SEED = open(SEED, "w+")
    
    if preseed_type == "basic":
      print("Injecting Basic Payload".center(os.get_terminal_size().columns), end = "\r")
      SEED.write(self.Preseed.preseed_basic)
      SEED.close()
    elif preseed_type == "lamp":
      print("Injecting LAMP Payload".center(os.get_terminal_size().columns), end = "\r")
      SEED.write(self.Preseed.preseed_lamp)
      SEED.close()
    elif preseed_type == "lamp_wordpress":
      print("Injecting LAMP-Wordpress Payload".center(os.get_terminal_size().columns), end = "\r")
      SEED.write(self.Preseed.preseed_lamp_wordpress)
      SEED.close()
    else:
      print("Injecting Minimal Payload".center(os.get_terminal_size().columns), end = "\r")
      SEED.write(self.Preseed.preseed_minimal)
      
      SEED.close()

    Installer(self).SCP(self, str(DIRECTORY + "preseed.cfg"), "snow", "192.168.1.5", "/mnt/vCloud-1/Infrastructure/Virtual-Machines/")
    Progress(5).display()


    # print("Executing Installation".center(os.get_terminal_size().columns), end = "\r")
    # time.sleep(2.5)
    
    #Installer(self).SCP(self, DIRECTORY + "create-VPS.sh", "snow", "192.168.1.5", "/mnt/vCloud-1/Infrastructure/Virtual-Machines/")
    #time.sleep(5)

    Installer(self).ttyExecute(str(DIRECTORY + "create-VPS.sh"), "192.168.1.5")

  def LINUX(self, type = None):
    update_permissions = "sudo chmod 777 -R /tmp/"
    Terminal(update_permissions).execute()

    file_script = "/tmp/create_VPS.sh"

    script = open(file_script, "w+")
    script.write(self.command)
    script.close()

    provision = textwrap.dedent(
    f"""
    ssh snow@localhost "bash -s" -- < {file_script}
    """.strip()
    )

    file_preseed = "/tmp/preseed.cfg"
    preseed = open(file_preseed, "w+")

    if type == "basic":
      print("Injecting Basic Payload")
      preseed.write(self.Preseed.preseed_basic)
      preseed.close()
    elif type == "lamp":
      print("Injecting LAMP Payload")
      preseed.write(self.Preseed.preseed_lamp)
      preseed.close()
    elif type == "lamp_wordpress":
      print("Injecting LAMP-Wordpress Payload")
      preseed.write(self.Preseed.preseed_lamp_wordpress)
      preseed.close()
    else:
      print("Injecting Minimal Payload")
      preseed.write(self.Preseed.preseed_minimal)
      preseed.close()

    time.sleep(1)

    subprocess.call([file_script])

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
    PATH = "/mnt/vCloud-1/Infrastructure/Virtual-Machines/"

    slash = "\\"

    command = textwrap.dedent(
      f"""
      #!/bin/bash
      virt-install {slash}
      --nographics {slash}
      --noautoconsole {slash}
      --name {self.Preseed.hostname} {slash}
      --ram {RAM} {slash}
      --disk path={PATH}{self.Preseed.hostname}.qcow2,size=50 {slash}
      --location "{PATH}{ISO}" {slash}
      --initrd-inject={PATH}{PRESEED} {slash}
      --vcpus {CPU} {slash}
      --os-type linux {slash}
      --os-variant ubuntu18.04 {slash}
      --autostart {slash}
      --extra-args="console=ttyS0, 115200n8 serial"
      """
    ).rstrip()
    return command

  @staticmethod
  def SCP(self, source, user, client, directory):
    command = f"scp {source} {user}@{client}:{directory}".rstrip()

    CMD().execute(command)
    
  @staticmethod
  def ttyExecute(script, server):
    """ 
    @Description
    ↳ Internal method that executes a installer()-related command on a remote location using a file either created or 
        stored locally. The the process is executed by puTTY. puTTY should be pre-installed (create check statement), and 
        password should be passed in by command line before program execution (when creating the Installer() object) and 
        then be hashed.
    @Parameters
    ↳ Script --> The [os.path.dirname(os.path.normpath(__file__)) + \ + location] of the script.
    """

    tty_command = f"putty -ssh -l snow -pw Kn0wledge! -m {script} {server}"

    Terminal(tty_command).display()
    Progress(10).display()