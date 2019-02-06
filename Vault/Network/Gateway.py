"""
@Parameters
  ↳   User       - Username	         - Required	: (String)      - Default:  None
      IP         - IP Address        - Required	: (String)      - Default:  "192.168.0.5"
        ↳	Note: self.password is used for the preseeding. Default should remain the same. 
                Change the Payload script(s) to change the user's password after 
                installation.
      Address    - IP Address        - Required	: (String)      - Default:  None
      Type       - Preseed Type      - Required	: (String)      - Default:  "minimal"
      RAM        - RAM Allocation    - Required	: (Integer)     - Default:  512
      CPUs       - vCPU Allocation   - Required	: (String)      - Default:  1
      Hostname   - Server Name       - Required	: (String)      - Default:  VPS().hostname
      Domain     - FQDN              - Optional : (String)      - Default:  None

@Documentation
  [Function]    - "VPS().hostname" will print out the actual function return hostname.
                - The @property returns a true object property, but is not static
                - accross all VPS() objects. 
"""
import os
import sys
import time
import textwrap

from Payload.Vault.Shell.Terminal import Terminal

class Gateway(object):
  def __init__(self, user, server):
    self.user = user
    self.IP = server

  def update_Gateway_DNS(self, VPS):
    file_script = "update_Gateway_DNS.sh"

    file_script_location = os.path.dirname(os.path.normpath(__file__)) + "\\" + file_script

    double_slash = "\\" + "\\"

    file_script_location = file_script_location.replace("\\", double_slash)

    script = open(file_script_location, "w+")
    script.write(self.gateway_dns_script(VPS))
    script.close()

    time.sleep(1)

    script_location = os.path.dirname(os.path.normpath(__file__)) + "\\" + "update_Gateway_DNS.sh"

    Gateway(self.user, self.IP).ttyExecute("192.168.0.5", script_location)

  def update_Gateway_Users(self, VPS):
    file_script = "update_Gateway_Users.sh"

    file_script_location = os.path.dirname(os.path.normpath(__file__)) + "\\" + file_script

    double_slash = "\\" + "\\"

    file_script_location = file_script_location.replace("\\", double_slash)

    script = open(file_script_location, "w+")
    script.write(self.gateway_user_script(self, VPS))
    script.close()

    time.sleep(1)

    script_location = os.path.dirname(os.path.normpath(__file__)) + "\\" + "update_Gateway_Users.sh"

    Gateway(self.user, self.IP).ttyExecute("192.168.0.5", script_location)

  @staticmethod
  def gateway_dns_script(VPS):
    open = "{"
    close = "}"
    tab = "\t"

    dns = "/etc/hosts"

    script = textwrap.dedent(
      f"""
      #!/bin/bash
      {open}
        echo -e "{VPS.IP}{tab}{VPS.hostname}" >> {dns}
      {close} || {open}
        echo "Target Server does not have ownership of file {dns}"
      {close}
      """
    ).strip()

    return script

  @staticmethod
  def gateway_user_script(self, VPS):
    script = textwrap.dedent(
      f"""
      #!/bin/bash
      sudo useradd -m -d /home/{VPS.user} -s /bin/bash {VPS.user}
      sudo mkdir -p /home/{VPS.user}/.ssh
      sudo touch /home/{VPS.user}/.ssh/authorized_keys

      sudo chown snow -R /home/{VPS.user}
      sudo chmod 777 -R /home/{VPS.user}/.ssh

      ssh-keygen -b 4096 -t rsa -C "" -f /home/{VPS.user}/.ssh/id_rsa -q -N ""

      scp /home/{VPS.user}/.ssh/id_rsa {self.user}@{self.IP}:~/.ssh/id_rsa_vps

      public_key=$(cat /home/{VPS.user}/.ssh/id_rsa.pub)
      
      echo 'command="ssh {VPS.user}@{VPS.hostname}"' $public_key >> /home/{VPS.user}/.ssh/authorized_keys

      sudo chmod -R 700 /home/{VPS.user}/.ssh
      sudo chmod 644 /home/{VPS.user}/.ssh/authorized_keys
      sudo chmod 644 /home/{VPS.user}/.ssh/id_rsa.pub
      sudo chmod 600 /home/{VPS.user}/.ssh/id_rsa
      sudo chown {VPS.user}:{VPS.user} -R /home/{VPS.user}

      """
    ).strip()

    return script

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