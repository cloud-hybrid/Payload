import textwrap

import mysql.connector

NETWORK = "192.168.0."

class SQL(object):
  def __init__(self, username:str, password:str, host:str , database:str):
    self.connection = mysql.connector.connect(
      user = username,
      passwd = password,
      host = host,
      database = database
    )

  def disconnect(self):
    self.connection.close()

  def queryAll(self):
    cursor = self.connection.cursor()
    cursor.execute("SELECT * FROM DEVELOPMENT")
    query = cursor.fetchall()
    return query

  def incrementIP(self):
    data = self.queryAll()
    for row in data:
      last_row = row

    IP = last_row[4]
    print("IP Address: " + IP)
    subnet = int(IP[10:])

    # print(subnet)
    return subnet + 1

  def addVPS(self, user:str, password:str, injection:str, ip:str, ram:int, cpu:int, domain:str, ssl:int, email:str):
    cursor = self.connection.cursor()
    command = ("INSERT INTO DEVELOPMENT "
              "(USERNAME, PASSWORD, INJECTION, IP, RAM, CPU, FQDN, CERTIFICATE, EMAIL) "
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    data = (user, password, injection, ip, ram, cpu, domain, ssl, email)

    cursor.execute(command, data)
    self.connection.commit()

def main():
  connection = SQL("root", "P@ssW0rd$", "169.0.0.0", "DATABASE_NAME")
  result = connection.queryAll()

  subnet = connection.incrementIP()

  VPS_IP = NETWORK + str(subnet)

  connection.addVPS("test2", "P@ssW0rd$", "Wordpress", NETWORK + str(subnet), 512, 1, "N/A", 0, "jsanders4129@gmail.com")
  
  connection.disconnect()

def example():
  database = mysql.connector.connect(user = "root", passwd = "P@ssW0rd$", host = "169.0.0.0", database = "DATABASE_NAME")
  cursor = database.cursor()
  cursor.execute("SELECT * FROM TABLE")
  result = cursor.fetchall()

  for row in result:
    print(row)

  database.close()

if __name__ == "__main__":
  main()