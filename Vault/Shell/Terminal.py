"""
Argument(s):
@Payload:
  __Payload       - Required  : (__init__)

  --proxy         - Required  : [server, hostname, location]
"""

import subprocess

class Terminal(object):
  def __init__(self, command):
    self.command = command

  def terminal(self):
    subprocess.run(self.command, shell = True)

  def display(self):
    process = subprocess.run(self.command, shell = True, stdout = subprocess.PIPE)
    result = process.stdout.decode('utf-8').rstrip("\n\r")
    return result

  def run(self):
    process = subprocess.run(self.command, shell = True)
    return process

  def dev(self):
    process = subprocess.run(self.command, shell = True, stdout = subprocess.PIPE)
    result = process.stdout.decode('utf-8').rstrip("\n\r")
    return result

  def execute(self):
    subprocess.run(self.command, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
