"""
Remote-Host Object for KVM-Based Hosting

Host.py serves as the mothership for our cloud-provisioning tool. This 
module is responsible for securing remote connections, creating 
required services (SQL, Reverse-Proxies, Email, Webservers, etc.) & 
hosting our Virtual Private Servers (VPS).

@Structure
  Host(object):
    :Parameters:
      - user          :     (String)     :     Host login name
      - server        :     (String)     :     Local IP address
      - OS            :     (String)     :     TBD

@Dependencies
  - TBD

@Attributes
  - N/A : (None) : N/A

@Functions
    - function(input:type): 
      ...

@General
  - Contact: development.cloudhybrid@gmail.com (Snow)
  - Documentation: https://github.com/cloud-hybrid/Payload
  - Website: https://vaultcipher.com/

@Development
  - [ ] Implement linux & windows port in single python program.
  - [ ] Use OS to check Host and Remote-Host operating system and
          return information for error checking in global namespace.
  - [ ] Create a LocalHost, and rename this file to RemoteHost, and 
          transfer applicable functions/properties accordingly. 
  - [ ] Create MailServer object.
"""

import os
import time
import subprocess
import smtplib
import textwrap

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from Payload.Vault.Shell.CMD import CMD

class Host(object):
  mail_server = "smtp.gmail.com"
  mail_port = 587
  def __init__(
    self,
    user = None, 
    password = None, 
    server = None, 
    local_OS = None, 
    remote_OS = None, 
    email_sender = None, 
    email_recipient = None,
    key = None
  ):
    self.user = user
    self.password = password
    self.server = server
    self.local_OS = local_OS
    self.remote_OS = remote_OS
    self.sender = email_sender
    self.recipient = email_recipient

    if key == None:
      self.SSH_key = Host.windowsSSH_Directory
    else:
      self.SSH_key = key

  def copySSHKey(self):
    username = self.user
    password = self.password
    ip_address = self.server
    key = self.SSH_key

    command = f"ssh -t {username}@{ip_address} sudo cat /tmp/id_rsa.pub > /home/snow/.ssh/authorized_keys" 
    subprocess.run(command)

  def transerSSHKey(self):
    username = self.user
    password = self.password
    ip_address = self.server
    key = self.SSH_key

    command = f"pscp -pw {password} {key} {username}@{ip_address}:/tmp"
    
    print("Transferring: " + command)
    subprocess.run(command)
    time.sleep(15)
    self.copySSHKey()

  # def emailPrivateKey(self):
  #   server = smtplib.SMTP(Host.mail_server, Host.mail_port)
  #   server.starttls()
  #   server.login(self.eMail[0], self.eMail[1])

  #   private_key = open('/home/snow/.ssh/id_rsa_vps', 'r')

  #   mail = MIMEMultipart()
  #   mail["From"] = self.eMail[0]
  #   mail["To"] = self.eMail[2]
  #   mail["Subject"] = "Private Key"

  #   content = private_key.read()
  #   mail.attach(MIMEText(content, "plain"))

  #   file = "id_rsa"
  #   attachment = open("/home/snow/.ssh/id_rsa_vps", "r")

  #   meta = MIMEBase('application', 'octet-stream')

  #   meta.set_payload((attachment).read())

  #   encoders.encode_base64(meta)

  #   meta.add_header('Content-Disposition', "attachment; filename= %s" % file)

  #   mail.attach(meta)

  #   email = mail.as_string()

  #   server.sendmail("development.cloudhybrid@gmail.com", "jsanders4129@gmail.com", email)

  #   server.quit()

  #   private_key.close()
  #   attachment.close()
  
  def emailPrivateKey_windows(self):
    server = smtplib.SMTP(Host.mail_server, Host.mail_port)
    server.starttls()
    server.login(self.sender, "Kn0wledge!")

    scp_command = "scp snow@192.168.0.5:~/.ssh/id_rsa_vps " + f"C:\\Users\\{Host.currentUser()}\\AppData\\Local\\Temp\\"

    CMD().execute(scp_command)

    time.sleep(5)

    private_key = open(f"C:\\Users\\{Host.currentUser()}\\AppData\\Local\\Temp\\" + "id_rsa_vps", "r")

    mail = MIMEMultipart()
    mail["From"] = self.sender
    mail["To"] = self.recipient
    mail["Subject"] = "Private Key"

    content = private_key.read()
    mail.attach(MIMEText(content, "plain"))

    attachment = open(f"C:\\Users\\{Host.currentUser()}\\AppData\\Local\\Temp\\" + "id_rsa_vps", "r")

    meta = MIMEBase('application', 'octet-stream')

    meta.set_payload((attachment).read())

    encoders.encode_base64(meta)

    meta.add_header('Content-Disposition', "attachment; filename= %s" % "id_rsa")

    mail.attach(meta)

    email = mail.as_string()

    server.sendmail(self.sender, self.recipient, email)

    server.quit()

    private_key.close()
    attachment.close()

    os.remove(f"C:\\Users\\{Host.currentUser()}\\AppData\\Local\\Temp\\" + "id_rsa_vps")
  
  @staticmethod
  def windowsTempPermissions():
    temp_directory = Host().windowsTEMP

    read_access =  os.access(temp_directory, os.R_OK)
    write_access = os.access(temp_directory, os.W_OK)
    execution_access = os.access(temp_directory, os.X_OK)

    permissions =  {"Read" : read_access, "Write" : write_access, "Execution" : execution_access}
    return permissions

  @staticmethod
  def currentUser():
    current_user = os.getlogin()
    return current_user

  @staticmethod
  def setSSHPermissions(user, address, port = 22):
    for command in Host().SSHPermissions:
      try:
        subprocess.run(f"ssh -p {port} {user}@{address}" + " " + "sudo" + " " + str(command))
        #print(f"ssh -p {port} {user}@{address}" + " " + "sudo" + " " + str(command))
      except:
        print("Unsuccessful: " + f"ssh -p {port} {user}@{address}" + " " + "sudo" + " " + str(command))


  @property
  def windowsTEMP(cls):
    property = f"C:\\Users\\{Host.currentUser()}\\AppData\\Local\\Temp"
    return property

  @property
  def windowsSSH_Directory(cls):
    property = f"C:\\Users\\{Host.currentUser()}\\.ssh\\"
    return property

  @property
  def linuxTEMP(cls):
    property = "/var/tmp/"
    return property

  @property
  def privateKey(cls):
    key = "id_rsa"
    return key

  @property
  def temporaryKey(cls):
    key = "id_rsa_vps"
    return key

  @property
  def SSHConfiguration(cls):
    property = textwrap.dedent(
      f"""
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
        LogLevel INFO

        # Authentication:

        #LoginGraceTime 2m
        PermitRootLogin yes
        StrictModes no
        MaxAuthTries 6
        #MaxSessions 10

        PubkeyAuthentication yes

        # Expect .ssh/authorized_keys2 to be disregarded by default in future.
        # AuthorizedKeysFile .ssh/authorized_keys .ssh/authorized_keys2

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

        # Change to yes to enable challenge-response passwords (beware issues with
        # some PAM modules and threads)
        ChallengeResponseAuthentication no

        # Kerberos options
        #KerberosAuthentication no
        #KerberosOrLocalPasswd yes
        #KerberosTicketCleanup yes
        #KerberosGetAFSToken no

        # GSSAPI options
        #GSSAPIAuthentication no
        #GSSAPICleanupCredentials yes
        #GSSAPIStrictAcceptorCheck yes
        #GSSAPIKeyExchange no

        # Set this to 'yes' to enable PAM authentication, account processing,
        # and session processing. If this is enabled, PAM authentication will
        # be allowed through the ChallengeResponseAuthentication and
        # PasswordAuthentication.  Depending on your PAM configuration,
        # PAM authentication via ChallengeResponseAuthentication may bypass
        # the setting of "PermitRootLogin without-password".
        # If you just want the PAM account and session checks to run without
        # PAM authentication, then enable this but set PasswordAuthentication
        # and ChallengeResponseAuthentication to 'no'.
        UsePAM yes

        #AllowAgentForwarding yes
        #AllowTcpForwarding yes
        #GatewayPorts no
        X11Forwarding yes
        #X11DisplayOffset 10
        #X11UseLocalhost yes
        #PermitTTY yes
        PrintMotd no
        #PrintLastLog yes
        #TCPKeepAlive yes
        #UseLogin no
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
        # Allow client to pass locale environment variables
        AcceptEnv LANG LC_*

        # override default of no subsystems
        Subsystem       sftp    /usr/lib/openssh/sftp-server
        """
    )

    return property

  @property
  def SSHPermissions(cls):
    property = [
      "chmod 700 ~/.ssh",
      "chmod 644 ~/.ssh/id_rsa.pub",
      "chmod 644 ~/.ssh/authorized_keys",
      "chmod 644 ~/.ssh/known_hosts",
      "chmod 600 ~/.ssh/id_rsa"
    ]

    return property
# vProfile.print_stats()