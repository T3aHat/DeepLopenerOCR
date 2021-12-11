# DeepLopenerOCR  
DeepLのクライアント版にてDeepL API契約での恩恵を得られないので，似たような機能を持つアプリケーションを目指す．  
→tesseractを用いたOCRを利用できるアプリケーション．

## メイン部
__DeepLopenerOCR__  
![exe.png](https://github.com/T3aHat/DeepLopenerOCR/raw/main/images/exe.png)  
__[本家](https://www.deepl.com/app)__    
![dl.png](https://github.com/T3aHat/DeepLopenerOCR/raw/main/images/dl.png)

* 起動時に`ctrl+C`を0.5秒以内に2回入力すると，クリップボードのテキストが左の`textarea`に入力されて，
DeepL APIを用いて翻訳された結果が右の`textarea`に表示される
* 左の`textarea`で`ctrl+Enter`をしても翻訳できる
* `Translate into`の横の一覧から翻訳先言語を選択でき，変更すると再度その言語にて翻訳される

## OCR機能
* 有効時，クリップボードの変化を常に監視し，画像データになった場合はTesseractを使用したOCRを行って (English) DeepLに投げる．
![ocr.gif](https://github.com/T3aHat/DeepLopenerOCR/raw/main/images/ocr.gif)

## 拡張機能
* DeepLopenerOCRで翻訳時にウィンドウがフォーカスされるようにする [Chrome拡張機能](https://github.com/T3aHat/DeepLopenerOCR/tree/main/extension)
* ウィンドウを最小化している状態で新たに翻訳してもウィンドウが前に出てこなく使いにくいため実装した
* インストールしなくてもDeepLopenerOCR自体は利用可能

## Settings
__DeepLopenerOCR__  
![settings.png](https://github.com/T3aHat/DeepLopenerOCR/raw/main/images/settings.png)  
__[本家](https://www.deepl.com/app)__   
![dl2.png](https://github.com/T3aHat/DeepLopenerOCR/raw/main/images/dl2.png)  

* メイン部の右上の歯車アイコンから遷移
* `Default target language for translation`でコマンド実行時の翻訳先言語を指定する
* `ctrl+C`+任意のショートカットを割り当てられる
* ここで`API_KEY`を保存する


# 起動時実行
`add_to_startup()`により自動起動用.batが作成される．  


# exe化
```
python -m eel .\DeepLopenerOCR.pyw assets --icon assets/favicon.ico --exclude win32com --exclude numpy --exclude cryptography --exclude pandas
```
`--onefile`と`--noconsole`の両方をつけるとOCRが正常に実行できなくなったため，`--onefile`は指定していない．


# Todo
- OCR機能使用のための環境構築法をまとめて記載
- `pyocr.tesseract.TESSERACT_CMD = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'`などのコードの最適化(気が向いたら)
- 自動起動するかオプション
