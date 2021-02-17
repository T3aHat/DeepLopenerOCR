# DeepLopenerPROEXE  
DeepLのクライアント版にてDeepL API契約での恩恵を得られないので，似たような機能を持つアプリケーションを目指す．  
# Usage  
## メイン部
![exe.png](https://github.com/T3aHat/DeepLopenerPROEXE/raw/main/images/exe.png)
![dl.png](https://github.com/T3aHat/DeepLopenerPROEXE/raw/main/images/dl.png)__[本家](https://www.deepl.com/app)__  

* `deeplopenerexe.py`起動時に`ctrl+C`を1秒以内に2回入力すると，クリップボードのテキストが左の`textarea`に入力されて，
DeepL Pro APIを用いて翻訳された結果が右の`textarea`に表示される
* 左の`textarea`で`ctrl+Enter`をしても翻訳できる
* `Translate into`の横の一覧から翻訳先言語を選択でき，変更すると再度その言語にて翻訳される
  
## Settings
![settings.png](https://github.com/T3aHat/DeepLopenerPROEXE/raw/main/images/settings.png)
![dl2.png](https://github.com/T3aHat/DeepLopenerPROEXE/raw/main/images/dl2.png)__[本家](https://www.deepl.com/app)__  

* メイン部の右上の歯車アイコンから遷移
* `Default target language for translation`でコマンド実行時の翻訳先言語を指定する．なお，メイン部にある一覧で翻訳言語を変更すると，その言語に切り替わる
* `ctrl+C`+任意のショートカットを割り当てられる
* ここで`API_KEY`を保存する(現在は`config.ini`から取得できない場合はCUIでinputすることもできる)

# exe化
debugのため`--noconsole`用のコーディングはまだしていない
```
python -m eel .\deeplopenerproexe.py assets --onefile --noconsole --icon favicon.ico
```

# Todo  
* ウィンドウを閉じて終了する対策
`close_callback`で`eel.start("main.html")`かつwindowを最小化?
    * chrome extensionの`chrome.windows.update(window.id, { state: "minimized" });`で対処?
* Translate documents  
自分は必要性を全く感じないので優先度ε
* 起動時自動起動の簡略化