"""
@Description:
↳ The Windows() object takes in the location of a relative script location and uses the
    Windows 10 Command Prompt to execute. The primary function of the object is to
    handle virtual Python (venv) environments without failing as with subprocess, 
    and more importantly, to create asynchronous processes for ease-of-use and 
    performance. 
"""

import os
import sys
import time
import textwrap
import subprocess

from Payload.Host.Linux import Linux

class Windows(object):
  def __init__(self):
    pass

  @staticmethod
  def execute(command):
    directory = "C:\\Temp\\"
    script = "execute.bat"
    
    content = textwrap.dedent(
      f"""
      @echo off
      start cmd /k "{command}"
      """.strip()
    )

    script = open(str(directory + script), "w+")
    script.write(content)
    script.close()

    time.sleep(2.5)

    subprocess.call(str(directory + "execute.bat"), shell = True)

  @staticmethod
  def transfer_rsa_key(source, remote_username, remote_host):
    command = f"scp {source} {remote_username}@{remote_host}:~/.ssh"
    Windows().execute(command)