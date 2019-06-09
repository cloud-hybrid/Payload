pyinstaller --name Payload ^
  --console ^
  --onefile ^
  --add-data ".\Vault\Installation\Source\Bionic-Server.iso;." ^
  --add-data ".\Vault\Installation\Source\Vault.ico;." ^
  --distpath ".\Distribution" ^
  --workpath ".\Build" ^
  --icon=Vault.ico ^
  --log-level INFO ^
  --debug all ^
  --clean ^
  __main__.py
