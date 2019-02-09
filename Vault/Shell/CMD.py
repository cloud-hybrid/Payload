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
    script = "console.bat"
    
    content = textwrap.dedent(
f"""
@echo off
start cmd /k "{command}"
""".strip()
    )

    script = open(script, "w+")
    script.write(content)
    script.close()

    time.sleep(2.5)

    process = subprocess.call("console.bat", shell = True)

  @staticmethod
  def execute(command):
    script = "execute.bat"
    
    content = textwrap.dedent(
f"""
@echo off
start cmd /c "{command}"
""".strip()
    )

    script = open(script, "w+")
    script.write(content)
    script.close()

    time.sleep(2.5)

    process = subprocess.call("execute.bat", shell = True)
