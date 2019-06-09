#!/usr/bin/env python3.7.3
# ........................................................................... #
# (c) 2019, Jacob B. Sanders <development.cloudhybrid@gmail.com>
# GNU General Public License v3.0: https://opensource.org/licenses/GPL-3.0

METADATA = {
  "Module" : "ExecutionHost",
  "Package" : "IaaS",
  "Version" : "0.2",
  "Status": "beta"
  }

DOCUMENTATION = """
Module: ExecutionHost
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
  - [ ] Check the self.execution_platform return types for the different types of operating systems. 
"""

EXAMPLES = """
- TBD
"""

import os
import sys
import pwd
import time
import shlex
import getpass
import argparse
import platform
import tempfile
import textwrap
import threading
import subprocess
import warnings

try: 
  import pexpect
  from pexpect import pxssh
except ImportError:
  print("Warning: Pexpect is not installed")

try: 
  import paramiko
except ImportError:
  print("Warning: Paramiko is not installed")

warnings.filterwarnings(action = "ignore", module = ".*paramiko.*")

class ExecutionHost(object):
  def __init__(self, username: str, email:str, password: str, address: str):
    self.username = username
    self.email = email
    self.password = password
    self.address = address

    self.executing_platform = platform.system()

  def sshKeyCheck(self):
    """ Check if SSH keys have been created and stored in the default location (OS-dependent). """
    if self.executing_platform == "Darwin" or self.executing_platform == "Linux":
      ssh_key = self.LinuxSSHDirectory
      if os.path.exists(str(ssh_key) + "id_rsa.pub"):
        return True
      else:
        return False
        print("NO KEYS")
    else:
      print("Troubleshoot this on a Windows Machine.")

  def sshKeyGeneration(self):
    command = f"ssh-keygen -t rsa -C '{self.email}' -f '{self.LinuxSSHDirectory}id_rsa' -N ''"

    stream = subprocess.Popen(shlex.split(command),
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 15)
    print(output)

  def sshCopyID(self):
    """ Note: Use of an SSH Banner will confuse the buffer -- causing the command to fail. """

    # Add finally block that tests if keys are already installed. 

    try:
      command = f"ssh-copy-id -i {self.LinuxSSHDirectory}id_rsa.pub {self.username}@{self.address}"
      child_process = pexpect.spawn(command, timeout = 15)
      child_process.expect("password: ")
      child_process.expect(pexpect.EOF)
      child_process.close()
    except:
      print("Key's Already Installed. Maybe (:")

  def checkVirtualizationCompatability(self):
    """ Check if the server supports hardware virtualization. """

    command = f"egrep -c '(vmx|svm)' /proc/cpuinfo"

    stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", "egrep -c '(vmx|svm)' /proc/cpuinfo"],
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 15)[0]
    output = str(output)
    output = output.strip()
    output = int(output)

    if output >= 1:
      return True
    else:
      return False

  def checkAccelerationCompatability(self):
    """ Check if the server supports KVM hardware acceleration. """

    command = "which kvm-ok"

    stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", command],
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 15)[0]
    output = str(output).split()

    if len(output) == 0:
      command = "sudo apt install cpu-checker"

      stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", command],
        shell = False,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True)

      command = "sudo kvm-ok"

      stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", command],
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

      stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", command],
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

  def enableVirtualizationSoftware(self):
    command = "sudo service libvirtd start"

    stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", command],
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output_libvirtd = stream.communicate()[0]

    command = "sudo update-rc.d libvirtd enable"

    stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", command],
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

    stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", command],
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate(timeout = 60)[0]
    output = str(output).split()
    output = output[-7:]
    output = " ".join(output)
    output = output.strip()

    if output != None:
      return True
    else:
      return False
  
  def upgradeVirtualizationHost(self):
    """ Upgrade the VirtualizationHost's installed packages. """

    command = "sudo apt upgrade -y"

    stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", command],
      shell = False,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      universal_newlines = True)

    output = stream.communicate()[0]
    if output != None:
      return True

  def updateSudoPermissions(self):
    strings = f"{self.username} ALL=(ALL) NOPASSWD: ALL"
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

  def authorizeRSAKey(self):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(self.address, 22, self.username, self.password)

    shell = client.invoke_shell()
    
    command = f"sudo cat /tmp/id_rsa.pub > /home/{self.username}/.ssh/authorized_keys"
    (stdin, stdout, stderr) = client.exec_command(command)
    for line in stdout.readlines():
      print(line)

    shell.close()
    client.close()

  def transferRSAKey(self, background = False):
    if self.executing_platform == "Windows":
      if self.ssh_key != "NULL":
        command = f"pscp -pw {self.password} {self.ssh_key} {self.username}@{self.address}:/tmp"
      else:
        command = f"pscp -pw {self.password} {self.WindowsRSAKey} {self.username}@{self.address}:/tmp"
      stream = subprocess.run(command)
    elif self.executing_platform == "Linux" or self.executing_platform == "Darwin":
      log_file = tempfile.mktemp()
      log_file = open(log_file, "w")

      ssh_parameters = "-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no"

      if background == True:
        ssh_parameters += " -f"

      if self.ssh_key != "NULL":
        command = f"scp {ssh_parameters} {self.ssh_key} {self.username}@{self.address}:~/.ssh"
      else:
        command = f"scp {ssh_parameters} {self.WindowsRSAKey} {self.username}@{self.address}:~/.ssh"

      child_process = pexpect.spawn(command, timeout = 60)
      child_process.expect(["password: "])
      child_process.sendline(self.password)
      child_process.logfile = log_file
      child_process.expect(pexpect.EOF)
      child_process.close()

      log_file.close()

      log_file_read = open(log_file, "r")
      output = log_file_read.read()
      output.close()

      if child_process != 0:
        raise Exception(log_file_read.read())

  @staticmethod
  def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

  @property
  def NamespaceUser(self):
    """ Returns the Username of the current user in either local or remote environments. """

    if self.executing_platform == "Darwin" or self.executing_platform == "Linux":
      return pwd.getpwuid(os.getuid())[0]
    else:
      print("Troubleshoot this on Windows")

  @property
  def LinuxSSHDirectory(self):
    property = f"/Users/{self.NamespaceUser}/.ssh/"
    return property

  @property
  def WindowsRSAKey(self):
    property = f"C:\\Users\\{self.NamespaceUser}\\.ssh\\id_rsa.pub"
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

    stream = subprocess.Popen(["ssh", "-t", f"{self.username}@{self.address}", command],
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

    stream = subprocess.Popen(["ssh", f"{self.username}@{self.address}", command],
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
  def defaultSSHdConfiguration(self):
    property = """
      # This is the sshd server system-wide configuration file.  See
      # sshd_config(5) for more information.

      # This sshd was compiled with PATH=/usr/bin:/bin:/usr/sbin:/sbin

      # The strategy used for options in the default sshd_config shipped with
      # OpenSSH is to specify options with their default value where
      # possible, but leave them commented.  Uncommented options override the
      # default value.

      #Port 22
      #AddressFamily any
      #ListenAddress 0.0.0.0
      #ListenAddress ::

      #HostKey /etc/ssh/ssh_host_rsa_key
      #HostKey /etc/ssh/ssh_host_ecdsa_key
      #HostKey /etc/ssh/ssh_host_ed25519_key

      # Ciphers and keying
      #RekeyLimit default none

      # Logging
      #SyslogFacility AUTH
      #LogLevel INFO

      # Authentication:

      #LoginGraceTime 2m
      #PermitRootLogin prohibit-password
      #StrictModes yes
      #MaxAuthTries 6
      #MaxSessions 10

      #PubkeyAuthentication yes

      # The default is to check both .ssh/authorized_keys and .ssh/authorized_keys2
      # but this is overridden so installations will only check .ssh/authorized_keys
      AuthorizedKeysFile	.ssh/authorized_keys

      #AuthorizedPrincipalsFile none

      #AuthorizedKeysCommand none
      #AuthorizedKeysCommandUser nobody

      # For this to work you will also need host keys in /etc/ssh/ssh_known_hosts
      #HostbasedAuthentication no
      # Change to yes if you don't trust ~/.ssh/known_hosts for
      # HostbasedAuthentication
      #IgnoreUserKnownHosts no
      # Don't read the user's ~/.rhosts and ~/.shosts files
      #IgnoreRhosts yes

      # To disable tunneled clear text passwords, change to no here!
      #PasswordAuthentication yes
      #PermitEmptyPasswords no

      # Change to no to disable s/key passwords
      #ChallengeResponseAuthentication yes

      # Kerberos options
      #KerberosAuthentication no
      #KerberosOrLocalPasswd yes
      #KerberosTicketCleanup yes
      #KerberosGetAFSToken no

      # GSSAPI options
      #GSSAPIAuthentication no
      #GSSAPICleanupCredentials yes

      # Set this to 'yes' to enable PAM authentication, account processing,
      # and session processing. If this is enabled, PAM authentication will
      # be allowed through the ChallengeResponseAuthentication and
      # PasswordAuthentication.  Depending on your PAM configuration,
      # PAM authentication via ChallengeResponseAuthentication may bypass
      # the setting of "PermitRootLogin without-password".
      # If you just want the PAM account and session checks to run without
      # PAM authentication, then enable this but set PasswordAuthentication
      # and ChallengeResponseAuthentication to 'no'.
      #UsePAM no

      #AllowAgentForwarding yes
      #AllowTcpForwarding yes
      #GatewayPorts no
      #X11Forwarding no
      #X11DisplayOffset 10
      #X11UseLocalhost yes
      #PermitTTY yes
      #PrintMotd yes
      #PrintLastLog yes
      #TCPKeepAlive yes
      #PermitUserEnvironment no
      #Compression delayed
      #ClientAliveInterval 0
      #ClientAliveCountMax 3
      #UseDNS no
      #PidFile /var/run/sshd.pid
      #MaxStartups 10:30:100
      #PermitTunnel no
      #ChrootDirectory none
      #VersionAddendum none

      # no default banner path
      #Banner none

      # override default of no subsystems
      Subsystem	sftp	/usr/libexec/sftp-server

      # Example of overriding settings on a per-user basis
      #Match User anoncvs
      #	X11Forwarding no
      #	AllowTcpForwarding no
      #	PermitTTY no
      #	ForceCommand cvs server
      """
    
    return property

  @property
  def preseed_lamp_wordpress(self):
    property = textwrap.dedent(
      f"""
      d-i debconf/priority string critical
      d-i auto-install/enable boolean true

      # --- Language Settings --- #
      d-i debian-installer/language string en
      d-i debian-installer/country string US
      d-i debian-installer/locale string en_US

      # --- Keyboard Overwrites --- #
      d-i console-setup/ask_detect boolean false
      d-i keyboard-configuration/xkb-keymap select us

      # --- Network Configuration --- #
      d-i netcfg/choose_interface select auto
      d-i netcfg/disable_autoconfig boolean true
      d-i netcfg/dhcp_failed note
      d-i netcfg/dhcp_options select Configure network manually
      # ------ > Static Network Settings
      d-i netcfg/get_ipaddress string {self.address}
      d-i netcfg/get_netmask string 255.255.0.0
      d-i netcfg/get_gateway string 192.168.1.1
      d-i netcfg/get_nameservers string 192.168.1.1
      d-i netcfg/confirm_static boolean true
      # ------ > Hostname
      d-i netcfg/get_hostname string {self.hostname}
      d-i netcfg/get_domain string vaultcipher.com

      # --- Prevent Wireless Prompt --- #
      d-i netcfg/wireless_wep string

      # --- Mirrors --- #
      d-i mirror/country string manual
      d-i mirror/http/hostname string us.archive.ubuntu.com
      d-i mirror/http/directory string /ubuntu
      d-i mirror/http/proxy string

      # --- Account Setup --- #
      # ------ > Root
      d-i passwd/root-login boolean true
      d-i passwd/root-password password {self.password}
      d-i passwd/root-password-again password {self.password}
      # ------ > Default User
      d-i passwd/user-fullname string {self.username}
      d-i passwd/username string {self.username}
      d-i passwd/user-password password {self.password}
      d-i passwd/user-password-again password {self.password}
      # ------ > Allow Weak Password
      d-i user-setup/allow-password-weak boolean true
      # ------ > Home Encryption
      d-i user-setup/encrypt-home boolean false

      # --- Time --- #
      d-i clock-setup/utc boolean true
      d-i time/zone string US/Eastern
      d-i clock-setup/ntp boolean true

      # --- Disk Partitioning --- #
      d-i partman-auto/method string lvm
      d-i partman-lvm/device_remove_lvm boolean true
      d-i partman-md/device_remove_md boolean true
      d-i partman-lvm/confirm boolean true
      d-i partman-lvm/confirm_nooverwrite boolean true
      d-i partman-auto/choose_recipe select atomic
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true
      d-i partman-md/confirm boolean true
      d-i partman-partitioning/confirm_write_new_label boolean true
      d-i partman/choose_partition select finish
      d-i partman/confirm boolean true
      d-i partman/confirm_nooverwrite boolean true

      # --- Package Installations --- #
      tasksel tasksel/first multiselect lamp-server
      d-i pkgsel/include string openssh-server net-tools curl software-properties-common wget curl

      # --- Update Policy --- #
      d-i pkgsel/update-policy select none
      d-i pkgsel/updatedb boolean true

      # --- Post Setup Configuration --- #
      d-i grub-installer/only_debian boolean true
      d-i grub-installer/with_other_os boolean true

      # --- Reboot --- #
      d-i finish-install/reboot_in_progress note

      # --- Late-Stage Commands --- #
      d-i preseed/late_command string in-target sed -i "s/^#PermitRootLogin.*\$/PermitRootLogin yes/g" /etc/ssh/sshd_config; \\
      in-target wget -O /tmp/provision.sh "https://unixvault.com/provision_lamp_wordpress.sh" --no-check-certificate; \\
      in-target chmod +x /tmp/provision.sh; \\
      in-target echo "{self.username} ALL=(ALL)  NOPASSWD:ALL" >> /etc/sudoers;
      in-target /bin/bash /tmp/provision.sh {self.username} {self.hostname}; \\
      """
    ).strip()
    
    return property

  def setup(self):
    print("Host Cores: " + str(host.Cores))
    print("Virtualization Capable: " + str(host.checkVirtualizationCompatability()))
    print("Acceleration Capable: " + str(host.checkAccelerationCompatability()))

    print("Updated: " + str(host.updateVirtualizationHost()))
    print("Upgraded: " + str(host.upgradeVirtualizationHost()))

    print("KVM Package Installed: " + str(host.installVirtualizationSoftware()))
    print("KVM Package Enabled: " + str(host.enableVirtualizationSoftware()))

    print("Host Network Interfaces: " + str(host.NetworkInterfaces))

def main():
  host = ExecutionHost("snow", "development.cloudhybrid@gmail.com", "Kn0wledge!", "192.168.0.1")

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

  print("Host Network Interfaces: " + str(host.NetworkInterfaces))

if __name__ == "__main__":
  main()