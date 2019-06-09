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

import sys
import time
import subprocess
import textwrap
import mysql.connector

class Connection(object):
  def __init__(self, username:str, password:str, host:str , database:str):
    self.connection = mysql.connector.connect(
      user = username,
      passwd = password,
      host = host,
      database = database
    )
    self.host = host
    self.network = "192.168.0."

    # console_configuration = subprocess.STARTUPINFO()
    # console_configuration.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # console_configuration.wShowWindow = subprocess.SW_HIDE
    
    check = subprocess.Popen(
      ['ping', '-n', '1', '-w', '500', self.host],
      stdout = subprocess.PIPE
    ).communicate()[0]

    if "Destination host unreachable" in check.decode('utf-8'):
      sys.exit("SQL Host Unreachable")
    elif "Request timed out" in check.decode('utf-8'):
      sys.exit("SQL Request Timed Out")
    else:
      print("Database Online")
      time.sleep(0.5)
      Connection.progress_bar("Securing Connection to Database")

  def disconnect(self):
    Connection.progress_bar("Closing Connection")
    self.connection.close()

  def queryAll(self):
    cursor = self.connection.cursor()
    cursor.execute("SELECT * FROM DEVELOPMENT")
    query = cursor.fetchall()
    return query

  def incrementIP(self):
    Connection.progress_bar("Reserving IP Address")
    data = self.queryAll()
    if not data:
      return "100"
    else:
      for row in data:
        last_row = row

      IP = last_row[4]
      subnet = int(IP[10:])

      if subnet > 200 or subnet < 100:
        print("Database Error")
        quit()
      else:
        return subnet + 1

  def addVPS(self, user:str, password:str, injection:str, ip:str, ram:int, cpu:int, domain:str, ssl:int, email:str):
    Connection.progress_bar("Adding VPS Information to Database")
    cursor = self.connection.cursor()
    command = ("INSERT INTO DEVELOPMENT "
              "(USERNAME, PASSWORD, INJECTION, IP, RAM, CPU, FQDN, CERTIFICATE, EMAIL) "
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    data = (user, password, injection, ip, ram, cpu, domain, ssl, email)

    cursor.execute(command, data)
    self.connection.commit()
  
  @staticmethod
  def progress_bar(statement):
    for iterator in '|/-\\'*3 + "✓": 
      sys.stdout.write(f"{statement}" + "... " + iterator + "\r")
      sys.stdout.flush()
      time.sleep(0.25)
    print("")

# Example:

# def main():
#   connection = Connection("root", "Kn0wledge!", "192.168.1.75", "V_PAYLOAD")
#   result = connection.queryAll()
#   subnet = connection.incrementIP()
#   VPS_IP = connection.network + str(subnet)
#   connection.addVPS("root", "Password", "Minimal", VPS_IP, 512, 1, "N/A", 0, "jsanders4129@gmail.com")
#   connection.disconnect()

# if __name__ == "__main__":
#   main()