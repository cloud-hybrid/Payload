import subprocess

class Security(object):
  def __init__(self):
    pass

  def createKey():
    pass

  def authorizeKey(public_key, user, client):
    command = f"""scp {public_key} {user}@{client}:~/.ssh/authorized_keys