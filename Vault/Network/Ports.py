@dataclass
class Ports:
  HTTP: int = 80
  HTTP_PROXY: int = 8080
  HTTPS: int = 443
  HTTPS_PROXY: int = 4443
  FTP_COMMAND: int = 20
  FTP_DATA: int = 21
  SSH: int = 22
  SSH_PROXY: int = 22
  DNS: int = 53
  SQL = 1433
  RDP: int = 3389
  VSFTPD: int = 49000