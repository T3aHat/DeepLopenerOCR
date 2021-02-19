import zipfile
with zipfile.ZipFile('DeepLopenerPROEXE.zip', 'w')as zf:
    zf.write('manifest.json')
    zf.write('background.js')
    zf.write('contents.js')
    zf.write('icon128.png')
