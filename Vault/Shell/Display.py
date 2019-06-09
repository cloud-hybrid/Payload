import os
import sys

class Display(object):
  def __init__(self):
    pass

  @staticmethod
  def header():
    sys.stdout.write("╔═════════════╦═══════════════════════╗".center(os.get_terminal_size().columns))
    sys.stdout.write("║             ║  Server Provisioning  ║".center(os.get_terminal_size().columns))
    sys.stdout.write("║   Payload   ╟───────────────────────╢".center(os.get_terminal_size().columns))
    sys.stdout.write("║             ║     © Cloud Hybrid    ║".center(os.get_terminal_size().columns))
    sys.stdout.write("╟─────────────╨───────────────────────╢".center(os.get_terminal_size().columns))
    sys.stdout.write("║  development.cloudhybrid@gmail.com  ║".center(os.get_terminal_size().columns))
    sys.stdout.write("╟───────────────────────────┬─────────╢".center(os.get_terminal_size().columns))
    sys.stdout.write("║      cloudhybrid.io       │  Snow   ║".center(os.get_terminal_size().columns))
    sys.stdout.write("╚═══════════════════════════╧═════════╝".center(os.get_terminal_size().columns))

  @staticmethod
  def copyright():
    sys.stdout.write("╔══════════════════╦══════════════════╗".center(os.get_terminal_size().columns))
    sys.stdout.write("║ Copyright © 2019 ║ Jacob B. Sanders ║".center(os.get_terminal_size().columns))
    sys.stdout.write("╚══════════════════╩══════════════════╝".center(os.get_terminal_size().columns))
