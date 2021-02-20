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

# 常駐化
裏で常に`keyboard.add_hotkey()`にてキー入力を確認している．

# 起動時実行
`add_to_startup()`は

```
bat_file.write("cd "+folder_path+'\nstart "" ' +
                   folder_path+"\dist\deeplopenerproexe.exe")
```
↑にてpyinstallerで固めた`.exe`を，

```
bat_file.write("cd "+folder_path+'\nstart "" ' +file_path)

```
↑にて`.py`をそれぞれWindows起動時に実行するためのファイルを自動的に作成して適当な場所に保存する．  
ただし，上の場合は`cmd.exe`が出てしまうので，これが出てこないショートカットを作成して該当箇所に保存するようにしたい．



# exe化
```
python -m eel .\deeplopenerproexe.py assets --onefile --noconsole --icon assets/favicon.ico
```

# Todo  
