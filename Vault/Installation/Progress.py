"""
Argument(s):
@Payload:
  __Payload       - Required  : (__init__)

  --proxy         - Required  : [server, hostname, location]
"""

import os
import sys
import time

class Progress(object):
  def __init__(self, executions, interactive = False, iteration = 0, total = None, prefix = '', suffix = '', decimals = 1, length = 40, fill = '█'):
    self.executions = executions
    self.interactive = interactive

    self.iteration = iteration
    self.prefix = prefix
    self.suffix = suffix
    self.decimals = decimals
    self.length = length
    self.fill = fill

    self.total = executions

  def display(self):
    sys.stdout.write("╔═════════════╦═══════════════════════╗".center(os.get_terminal_size().columns))
    sys.stdout.write("║             ║  © Vault Cipher LLC.  ║".center(os.get_terminal_size().columns))
    sys.stdout.write("║   Payload   ╟───────────────────────╢".center(os.get_terminal_size().columns))
    sys.stdout.write("║             ║   Jacob B. Sanders    ║".center(os.get_terminal_size().columns))
    sys.stdout.write("╟─────────────╨───────────────────────╢".center(os.get_terminal_size().columns))
    sys.stdout.write("║     developer.vault@gmail.com       ║".center(os.get_terminal_size().columns))
    sys.stdout.write("╟───────────────────────────┬─────────╢".center(os.get_terminal_size().columns))
    sys.stdout.write("║    git.vaultcipher.com    │  snow   ║".center(os.get_terminal_size().columns))
    sys.stdout.write("╚═══════════════════════════╧═════════╝".center(os.get_terminal_size().columns))

    print("Initializing Security Handshake".center(os.get_terminal_size().columns), end = "\r")
    time.sleep(1.5)

    print("Executing Network Payload".center(os.get_terminal_size().columns), end = "\r")
    time.sleep(1.5)

    for index in range(0, self.total):
      self.iteration += 1

      self.percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.iteration / float(self.total)))
      self.filled_length = int(self.length * self.iteration // self.total)
      self.bar = "┃" + self.fill * self.filled_length + '░' * (self.length - self.filled_length) + "┃"

      sys.stdout.write(self.bar.center(int(os.get_terminal_size().columns - 0.5)) + "\r")
      sys.stdout.flush()

      time.sleep(0.225)

      if self.iteration == self.executions:
        print()
