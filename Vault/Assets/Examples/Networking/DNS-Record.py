from requests import get

import sys
import subprocess

def self():
  IP = get('https://api.ipify.org').text

  return IP

def host(HOST):
  command = f"dig +short {HOST}"
  execution = subprocess.run(command, shell = True, stdout = subprocess.PIPE)
  IP = execution.stdout.decode('utf-8').rstrip("\n\r")
  return IP

def main():
  HOST = sys.argv[1]

  HOST = host(HOST)
  SELF = self()

  if HOST != SELF:
    print("Error: DNS Record Mismatch")
  else:
    print(f"Success: Host Record --> {HOST}")


if __name__ == "__main__":
  main()