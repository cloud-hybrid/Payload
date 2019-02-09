"""
@Infrastructure
  ↳   SSH-Keys    - SSH keys must be set from the         - Required  : (RSA-Key)
                  | - host --> client.
                  | - For testing purposes, add SSH
                  | - keys to and from localhost.
@Parameters
  ↳   Server      - The IP address or verified hostname   - Required  : (Command-Line)
                  | - of the target server hosting the
                  | - VPS. Defaults to localhost.
@Documentation
  [Note]    - When packaging the program, {script} may not work correct. The path relative
            - to its execution potentially could be the problem.
  [To-Do]   - Update @Parameters

"""

import smtplib
import time 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from Payload.Vault.Shell.CMD import CMD

class Host(object):
  def __init__(self, user, server, os, email):
    self.user = user
    self.server = server
    self.OS = os
    self.eMail = email

  @staticmethod
  def email_private_key(self):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(self.eMail[0], self.eMail[1])

    private_key = open('/home/snow/.ssh/id_rsa_vps', 'r')

    mail = MIMEMultipart()
    mail["From"] = self.eMail[0]
    mail["To"] = self.eMail[2]
    mail["Subject"] = "Private Key"

    content = private_key.read()
    mail.attach(MIMEText(content, "plain"))

    file = "id_rsa"
    attachment = open("/home/snow/.ssh/id_rsa_vps", "r")

    meta = MIMEBase('application', 'octet-stream')

    meta.set_payload((attachment).read())

    encoders.encode_base64(meta)

    meta.add_header('Content-Disposition', "attachment; filename= %s" % file)

    mail.attach(meta)

    email = mail.as_string()

    server.sendmail(self.eMail[0], self.eMail[2], email)

    server.quit()

    private_key.close()
    attachment.close()

  @staticmethod
  def email_private_key_windows(self):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(self.eMail[0], self.eMail[1])

    scp_command = """scp snow@192.168.0.5:~/.ssh/id_rsa_vps ."""

    CMD().execute(scp_command)

    time.sleep(10)

    private_key = open('id_rsa_vps', 'r')

    mail = MIMEMultipart()
    mail["From"] = self.eMail[0]
    mail["To"] = self.eMail[2]
    mail["Subject"] = "Private Key"

    content = private_key.read()
    mail.attach(MIMEText(content, "plain"))

    file = "id_rsa_vps"
    attachment = open(file, "r")

    meta = MIMEBase('application', 'octet-stream')

    meta.set_payload((attachment).read())

    encoders.encode_base64(meta)

    meta.add_header('Content-Disposition', "attachment; filename= %s" % file)

    mail.attach(meta)

    email = mail.as_string()

    server.sendmail(self.eMail[0], self.eMail[2], email)

    server.quit()

    private_key.close()
    attachment.close()