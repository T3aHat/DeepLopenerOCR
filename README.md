# DeepLopenerPROEXE  
DeepLのクライアント版にてDeepL API契約での恩恵を得られないので，似たような機能を持つアプリケーションを目指す．  


## メイン部
![exe.png](https://github.com/T3aHat/DeepLopenerPROEXE/raw/main/images/exe.png)__DeepLopenerPROEXE__
![dl.png](https://github.com/T3aHat/DeepLopenerPROEXE/raw/main/images/dl.png)__[本家](https://www.deepl.com/app)__  

* `deeplopenerexe.py`起動時に`ctrl+C`を1秒以内に2回入力すると，クリップボードのテキストが左の`textarea`に入力されて，
DeepL Pro APIを用いて翻訳された結果が右の`textarea`に表示される
* 左の`textarea`で`ctrl+Enter`をしても翻訳できる
* `Translate into`の横の一覧から翻訳先言語を選択でき，変更すると再度その言語にて翻訳される
  
## Settings
![settings.png](https://github.com/T3aHat/DeepLopenerPROEXE/raw/main/images/settings.png)__DeepLopenerPROEXE__
![dl2.png](https://github.com/T3aHat/DeepLopenerPROEXE/raw/main/images/dl2.png)__[本家](https://www.deepl.com/app)__  

* メイン部の右上の歯車アイコンから遷移
* `Default target language for translation`でコマンド実行時の翻訳先言語を指定する
* `ctrl+C`+任意のショートカットを割り当てられる
* ここで`API_KEY`を保存する

# 疑似常駐化
起動したウィンドウは右上の
<img src="https://github.com/T3aHat/DeepLopenerPROEXE/raw/main/assets/cancel.png" width="16px" height="16px">
を押すか，
consoleで`deeplopenerpro.py`のタスクを終了しない限り，閉じても再度最小化して復活する．


# exe化
```
python -m eel .\deeplopenerproexe.py assets --onefile --noconsole --icon favicon.ico
```

# Todo  
* 起動時自動起動の簡略化