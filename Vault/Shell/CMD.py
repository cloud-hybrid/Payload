"""
@Description:
↳ The CMD() object takes in the location of a relative script location and uses the
    Windows 10 Command Prompt to execute. The primary function of the CMD object is
    handle virtual Python (venv) environments without failing as with subprocess, 
    and more importantly, to create asynchronous processes for ease-of-use and 
    performance. 
"""
import os
import sys
import time
import textwrap
import subprocess

class CMD(object):
  def __init__(self):
    pass

  @staticmethod
  def console(command):
    # directory = CMD().MEI()
    directory = CMD().windowsTEMP
    script = "console.bat"
    
    content = textwrap.dedent(
f"""
@echo off
start cmd /c "{command}"
""".strip()
    )

    script = open(directory + script, "w+")
    script.write(content)
    script.close()

    time.sleep(2.5)

    print("CMD")
    process = subprocess.call(directory + "console.bat", shell = True)

  @staticmethod
  def execute(command):
    # directory = str(str(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) + "\\"))
    directory = "C:\\Temp\\"
    script = "execute.bat"
    
    content = textwrap.dedent(
f"""
@echo off
start cmd /c "{command}"
""".strip()
    )

    script = open(str(directory + script), "w+")
    script.write(content)
    script.close()

    time.sleep(2.5)

    subprocess.call(str(directory + "execute.bat"), shell = True)

  @staticmethod
  def MEI():
    directory = str(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) + "\\")
    return str(directory)

  @property
  def windowsTEMP(self):
    directory = "C:\\Temp\\"
    return directory

  @property
  def linuxTEMP(self):
    directory = "/tmp"
    return directory