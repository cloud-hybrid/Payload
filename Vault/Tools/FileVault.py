class FileVault(object):
  def __init__(self):
    pass

  def backup(self, source, target):
    with tempfile.NamedTemporaryFile(delete = False) as conversion:
      for line in open(str(source), "rb") :
        line = line.rstrip()
        conversion.write(line + "\n".encode())

    conversion.close()

    os.rename(str(source), str(f"{source}"[:-3] + ".backup"))
    os.rename(conversion.name, f"{target}")