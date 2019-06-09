pyinstaller --name Payload ^
  --console ^
  --onefile ^
  --add-data ".\Vault\Installation\Source\Bionic-Server.iso;." ^
  --distpath ".\Distribution" ^
  --workpath ".\Build" ^
  --log-level INFO ^
  --debug all ^
  --clean ^
  __main__.py
