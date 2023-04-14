# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['manage.py'],
             pathex=[],
             binaries=[],
             datas=[(r'C:\Users\千千\PycharmProjects\audio_record\audio\static\static_root',r'.\static\static_root'),
                    (r'C:\Users\千千\PycharmProjects\audio_record\audio\templates',r'templates'),
                    (r'C:\Users\千千\PycharmProjects\audio_record\audio\conf',r'conf'),],
             hiddenimports=['admin','admin.urls','system','system.urls','django.contrib.admin.apps','django.contrib.auth.apps','django.contrib.contenttypes.apps',
             'django.contrib.sessions.apps','django.contrib.messages.apps','django.contrib.staticfiles.apps',],
             hookspath=[],
             hooksconfig={},
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
          [],
          exclude_binaries=True,
          name='manage',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='manage')
