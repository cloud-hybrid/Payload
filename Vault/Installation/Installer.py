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
import textwrap
import subprocess
import pkgutil

from Payload.Vault.Shell.Terminal import Terminal
from Payload.Vault.Shell.CMD import CMD
from Payload.Vault.Installation import Source

class Installer(object):
  def __init__(self, seed: str, ram = 512, cpu = 1, server = "192.168.1.5"):
    self.Preseed = seed
    self.RAM = ram
    self.vCores = cpu
    self.Server = server

    # self.ttyUser = user
    # self.ttyPassword = password(hashed)

  def install(self, type = None):
    file_script = "create-VPS.sh"
    # file_script_location = os.path.dirname(os.path.normpath(__file__)) + "\\" + file_script

    # double_slash = "\\" + "\\"

    # file_script_location = file_script_location.replace("\\", double_slash)

    script = open(file_script, "w+")
    script.write(self.kernal)
    script.close()

    time.sleep(0.5)
    print("Executing Injection & Installation".center(os.get_terminal_size().columns), end = "\r")
    time.sleep(0.5)

    ISO = "Source\\" + "Bionic-Server.iso"

    Installer(self).SCP(self, ISO, "snow", "192.168.1.5", "/var/lib/libvirt/images/")

    time.sleep(5)

    SEED = "preseed.cfg"
    SEED = open(SEED, "w+")
    SEED.write(self.Preseed.preseed_minimal)
    SEED.close()

    time.sleep(1.0)

    Installer(self).SCP(self, "preseed.cfg", "snow", "192.168.1.5", "/var/lib/libvirt/images/")

    time.sleep(1.0)

    Installer(self).ttyExecute("192.168.1.5", "create-VPS.sh")

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
    PATH_DEFAULT = "/var/lib/libvirt/images/"

    slash = "\\"

    command = textwrap.dedent(
      f"""
      #!/bin/bash
      virt-install {slash}
      --nographics {slash}
      --noautoconsole {slash}
      --name {self.Preseed.hostname} {slash}
      --ram {RAM} {slash}
      --disk path={PATH_DEFAULT}{self.Preseed.hostname}.qcow2,size=50 {slash}
      --location "{PATH_DEFAULT}{ISO}" {slash}
      --initrd-inject={PATH_DEFAULT}{PRESEED} {slash}
      --vcpus {CPU} {slash}
      --os-type linux {slash}
      --os-variant ubuntu18.04 {slash}
      --autostart {slash}
      --extra-args="console=ttyS0, 115200n8 serial"
      """
    ).strip()
    return command

  @staticmethod
  def SCP(self, source, user, client, directory):
    command = textwrap.dedent(
    f"""
    scp {source} {user}@{client}:{directory}
    """.strip()
    )

    CMD().execute(command)
    
  @staticmethod
  def ttyExecute(server, script):
    """ 
    @Description
    ↳ Internal method that executes a installer()-related command on a remote location using a file either created or 
        stored locally. The the process is executed by puTTY. puTTY should be pre-installed (create check statement), and 
        password should be passed in by command line before program execution (when creating the Installer() object) and 
        then be hashed.
    @Parameters
    ↳ Script --> The [os.path.dirname(os.path.normpath(__file__)) + \ + location] of the script.
    """

    tty_command = textwrap.dedent(
    f"""
    putty -ssh -l root -pw Kn0wledge! -m {script} {server}
    """.strip()
    )

    Terminal(tty_command).display()