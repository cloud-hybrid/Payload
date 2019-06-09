#!/usr/bin/env python3.7.3
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
  - TBD

@Development
  - [ ] Look into importing a package that automatically signs into the server without need
        of a security key.
  - [ ] Include pingNode check.
  - [ ] Add check for determining if a GUI for the OS is installed. If not, don't install
        virt-manager under installVirtualizationSoftware().
  - [ ] Check for mysql-connector dependencies on freshly installed system. 
  - [ ] Figure out way to automate update of sudoers file. 
"""

EXAMPLES = """
- TBD
"""

import os
import pwd
import sys
import time
import shlex
import platform
import tempfile
import textwrap
import threading
import subprocess
import warnings

from pathlib import Path

class LinuxMaster(object):
  def __init__(self):
    self.executing_platform = platform.system()

  def checkVirtualizationCompatability(self):
    """ Check if the server supports hardware virtualization. """

    command = "egrep -c '(vmx|svm)' /proc/cpuinfo"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 15)[0]
    output = str(output).strip()
    output = int(output)

    if output >= 1:
      return True
    else:
      return False

  def checkAccelerationCompatability(self):
    """ Check if the server supports KVM hardware acceleration. """

    command = "which kvm-ok"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 15)[0]
    output = str(output).split()

    if len(output) == 0:
      command = "sudo apt install cpu-checker -y"

      stream = subprocess.run(shlex.split(command))

      command = "sudo kvm-ok"

      stream = subprocess.Popen(shlex.split(command),
        shell = False,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True)

      output = stream.communicate(timeout = 15)[0]
      output = str(output).split()
      output = output[-5:]
      output = " ".join(output)
      output = output.strip()

      if output == "KVM acceleration can be used":
        return True
      else:
        return False
    else:
      command = "sudo kvm-ok"

      stream = subprocess.Popen(shlex.split(command),
        shell = False,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True)

      output = stream.communicate(timeout = 15)[0]
      output = str(output).split()
      output = output[-5:]
      output = " ".join(output)
      output = output.strip()

      if output == "KVM acceleration can be used":
        return True
      else:
        return False

  @staticmethod
  def updateSudoPermissions():
    strings = f"{LinuxMaster().username} ALL=(ALL) NOPASSWD: ALL"
    command = f"sudo sh -c 'echo {strings}' >> /etc/sudoers"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    package_output = stream.communicate()[0]
    return package_output

  def installVirtualizationSoftware(self):
    installation_check = True

    for key, package in self.KVMPackages.items():
      command = f"sudo apt install {package} -y"

      stream = subprocess.Popen(shlex.split(command),
        shell = False,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True)

      package_output = stream.communicate()[0]

      if package_output:
        installation_check = True
      else:
        installation_check = False
        break

    if installation_check == True:
      return True
    else:
      return False

  def upgradeVirtualizationHost(self):
    """ Upgrade the VirtualizationHost's installed packages. """

    command = "sudo apt upgrade -y"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate()[0]
    if output != None:
      return True

  def enableVirtualizationSoftware(self):
    command = "sudo service libvirtd start"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output_libvirtd = stream.communicate()[0]

    command = "sudo update-rc.d libvirtd enable"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output_update_rc = stream.communicate()[0]

    if not output_libvirtd and not output_update_rc:
      return True
    else:
      return False

  def updateVirtualizationHost(self):
    """ Update the VirtualizationHost's installed packages. """

    command = "sudo apt update"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 60)[0]
    output = str(output).split()
    output = output[-7:]
    output = " ".join(output)
    output = output.strip()

    if output == "Done All packages are up to date." or output != None:
      return True
    else:
      return False

  def createRSAKey(self):
    command = f"touch /home/{LinuxMaster().username}/.ssh/authorized_keys"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    command = f"touch /home/{LinuxMaster().username}/.ssh/known_hosts"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)
    
    command = f"ssh-keygen -b 4096 -t rsa -f /home/{LinuxMaster().username}/.ssh/id_rsa -N ''"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate()[0]

    if output != None:
      return True

  def configureNetworkBridge(self):
    location = Path("/etc/netplan/cloud.yaml")
    if location.is_file():
      pass
    else:
      print("Host Network Interfaces: " + "\n" + str(self.NetworkInterfaces) + "\n")
      print("Select Network Interface: ")
      interface = input("Network Interface: ")
      static = input("Static IP with CIDR: ")
      gateway = input("Gateway: ")

      configuration = f"""
network:
  version: 2
  renderer: networkd
  ethernets:
    {interface}:
      dhcp4: no
      dhcp6: no
  bridges:
    br0:
      interfaces: [{interface}]
      dhcp4: no
      addresses: [{static}]
      gateway4:  {gateway}
      nameservers:
        addresses: [{gateway}, 8.8.8.8, 8.8.4.4]
"""

      directory = "/tmp/"
      file = "cloud.yaml"
      yaml = str(directory + file)

      yaml = open(yaml, "w+")
      yaml.write(configuration)
      yaml.close()

      command = f"sudo cp /tmp/cloud.yaml /etc/netplan/cloud.yaml"
      subprocess.call(shlex.split(command),
        shell = False,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True)

      command = f"sudo netplan apply"
      subprocess.call(shlex.split(command),
        shell = False,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True)

  @staticmethod
  def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

  def setSSHPermissions(self, ssh = False):
    for command in LinuxMaster().SSHPermissions:
      try:
        stream = subprocess.Popen(shlex.split(command),
          shell = False,
          stdout = subprocess.PIPE,
          stderr = subprocess.PIPE,
          universal_newlines = True)

        output = stream.communicate()[0]
        if output != None:
          return True

      except:
        print("Unsuccessful. Couldn't Set SSH Permissions.")

  @property
  def username(self):
    property = str(pwd.getpwuid(os.getuid())[0])
    return property

  @property
  def NetworkConfiguration(self):
    network_configuration = Path("/etc/netplan/cloud.yaml")
    if network_configuration.is_file():
      return True
    else:
      return False

  @property
  def RSAPublicKey(self):
    property = f"/home/{LinuxMaster().username}/.ssh/id_rsa.pub"
    return property

  @property
  def AptPackages(self):
    property = {
      "Network Interface Tool" : "ifupdown",
      "Static IP-Tables" : "iptables-persistent",
      "Python3 PIP" : "pip3",
      "Network Tools" : "net-tools"
    }

    return property

  @property
  def KVMPackages(self) -> dict:
    property = {
      "Hypervisor" : "qemu",
      "KVM" : "qemu-kvm",
      "Dependencies" : "libvirt-bin",
      "Virtual Bridge Tools" : "bridge-utils",
      "GUI" : "virt-manager"
    }

    return property

  @property
  def DPKGPackages(self):
    property = textwrap.dedent(
      f"""
      TBD
      """
    ).strip()

    return property

  @property
  def PIPPackages(self):
    property = {
      "C-Extension" : "Cython",
      "Language Decoratations" : "decorator",
      "Profiler" : "memory-profiler",
      "SQL Package" : "mysql-connector", 
      "Encoder" : "unicode",
      "Decoder" : "Unidecode",
      "Python Installer" : "PyInstaller",
      "Process Spawner" : "pexpect",
      "Python SSH Package" : "paramiko"
    }

    return property

  @property
  def NetworkInterfaces(self):
    command = "ip link"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 15)[0]
    property = str(output).strip()

    return property

  @property
  def Cores(self) -> int:
    command = "egrep -c '(vmx|svm)' /proc/cpuinfo"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 15)[0]
    output = str(output).strip()
    property = int(output)

    return property

  @property
  def SSHConfiguration(self, port = 22, loglevel = "DEBUG"):
    property = textwrap.dedent(
      f"""
        # --- Networking --- # 
        Port {port}
        AddressFamily any

        # --- Ciphers & Keys --- #
        #RekeyLimit default none

        # --- Logging & Debugging --- #
        LogLevel {loglevel}

        # --- Session & Authentication --- #
        #PasswordAuthentication yes
        LoginGraceTime 10m
        PermitRootLogin yes
        StrictModes no
        MaxAuthTries 5
        PubkeyAuthentication yes
        ChallengeResponseAuthentication no

        # --- PAM --- #
        UsePAM yes

        # --- User Sub-Settings --- #
        X11Forwarding yes
        PrintMotd no
        Banner /etc/sshd/banner.txt
        AcceptEnv LANG LC_*
        Subsystem sftp /usr/lib/openssh/sftp-server
        """
    )

    return property

  @property
  def SSHPermissions(self):
    property = [
      "chmod 700 ~/.ssh",
      "chmod 644 ~/.ssh/id_rsa.pub",
      "chmod 644 ~/.ssh/authorized_keys",
      "chmod 644 ~/.ssh/known_hosts",
      "chmod 600 ~/.ssh/id_rsa"
    ]

    return property

def main():
  host = LinuxMaster()
  host.configureNetworkBridge()

  # print("Host Cores: " + str(host.Cores))

  # print("Virtualization Capable: " + str(host.checkVirtualizationCompatability()))
  # print("Acceleration Capable: " + str(host.checkAccelerationCompatability()))

  # print("Updated: " + str(host.updateVirtualizationHost()))
  # print("Upgraded: " + str(host.upgradeVirtualizationHost()))

  # print("KVM Package Installed: " + str(host.installVirtualizationSoftware()))
  # print("KVM Package Enabled: " + str(host.enableVirtualizationSoftware()))

  #print("Host Network Interfaces: " + str(host.NetworkInterfaces))

  # print("Creating RSA and Directory Files: " + str(host.createRSAKey()))
  # print("Setting .SSH Permissions: " + str(host.setSSHPermissions()))

if __name__ == "__main__":
  main()