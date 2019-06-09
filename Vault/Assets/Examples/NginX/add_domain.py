#!/usr/bin/env python3

import os
import sys
import datetime
import subprocess

Time = datetime.datetime.now()

def restart(backup, record):
  command = "sudo nginx -s reload"

  try:
    subprocess.check_output(command, shell = True)
  except subprocess.CalledProcessError as e:
    print(e.output)

    with open(backup, "r") as file:
      data = file.read()
    
    with open(record, "w") as file:
      file.write(data)

def update(domain, record):
  with open(record, "r") as file:
    data = file.read()

  data = data.replace(".com;", f".com {domain} *.{domain};")

  with open(record, "w") as file:
    file.write(data)

def backup(backup_folder, record):
  time = Time.strftime("%Y-%m-%d-%H:%M:%S")
  backup = backup_folder + record + "." + "backup-" + time

  with open(record, "r") as file:
    data = file.read()

  with open(backup, "w+") as file:
    file.write(data)

  return os.path.abspath(backup)

def main():
  domain = sys.argv[1]
  record = sys.argv[2]
  folder = sys.argv[3] + "/"

  backup_file = backup(folder, record)

  update(domain, record)

  print(backup_file)

  restart(backup_file, os.path.abspath(record))

if __name__ == "__main__":
  main()