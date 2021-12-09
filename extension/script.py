import zipfile
with zipfile.ZipFile('DeepLopenerOCR.zip', 'w')as zf:
    zf.write('manifest.json')
    zf.write('background.js')
    zf.write('contents.js')
