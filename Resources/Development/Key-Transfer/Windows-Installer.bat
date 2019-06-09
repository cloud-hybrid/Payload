pyinstaller --name Key-Transfer ^
  --console ^
  --onefile ^
  --add-data ".\Payload\Source\Bionic-Server.iso;." ^
  --add-data ".\Payload\Source\Vault.ico;." ^
  --distpath ".\Distribution" ^
  --workpath ".\Build" ^
  --icon=Vault.ico ^
  --log-level INFO ^
  --debug all ^
  --clean ^
  __main__.py
