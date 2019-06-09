import os
import sys
import time
import textwrap
import subprocess

class Linux(object):
  def __init__(self):
    pass

  @property
  def SSH_Configuration(self):
    configuration = textwrap.dedent(
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
      #LogLevel INFO

      # Authentication:

      #LoginGraceTime 2m
      PermitRootLogin yes
      #StrictModes yes
      #MaxAuthTries 6
      #MaxSessions 10

      PubkeyAuthentication yes

      # Expect .ssh/authorized_keys2 to be disregarded by default in future.
      AuthorizedKeysFile      .ssh/authorized_keys .ssh/authorized_keys2

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
      PasswordAuthentication yes
      #PermitEmptyPasswords no

      # Change to yes to enable challenge-response passwords (beware issues with
      # some PAM modules and threads)
      ChallengeResponseAuthentication no

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
      Subsystem sftp  /usr/lib/openssh/sftp-server"""
    ).strip()
    return configuration