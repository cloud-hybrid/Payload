# -*- mode: python -*-

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['C:\\Users\\Development\\Documents\\Payload'],
             binaries=[],
             datas=[('.\\Vault\\Installation\\Source\\Bionic-Server.iso', '.'), ('.\\Vault\\Installation\\Source\\Vault.ico', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Payload',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='Vault.ico')
