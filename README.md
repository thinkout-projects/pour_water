# Pour water

## 環境構築

### Juliusをインストール

https://julius.osdn.jp/index.php?q=newjulius.html

上記URLの[Windows用実行バイナリ](https://github.com/julius-speech/julius/releases/download/v4.5/julius-4.5-win32bin.zip)をクリックしてダウンロード。

ダウンロードした一群のディレクトリを適当な場所（Program Files等）に移動。

### パスを通す

julius.exeの保存場所を含めてexeファイルを実行すれば動作するが、`julius`ワードをコマンドプロンプトで入力するだけで動作するようにパスを通す。

Windowsの「システム環境変数の編集」を開いて、環境変数ボタンをクリック。ユーザー環境変数・システム環境変数どちらでも良いので、PATH変数の値に、先述の一群のディレクトリの場所を設定。

### インストール確認

以下をコマンドプロンプトで実行して、Help一覧が表示されるかどうかを確認。

```bash
julius --help
```

### 音声認識用パッケージの設置

Julius音声認識パッケージのディクテーションキット (dictation-kit)をダウンロードして展開。

展開先は `(本リポジトリのパス)\julius-4.5\julius-kit\dictation-kit-4.5\` 以下に`bin`、`model`、`src`フォルダ他各種ファイルが展開されている状態にする。

> https://julius.osdn.jp/index.php?q=dictation-kit.html

### 音声認識の機能のみをテスト

上記設定が出来たら、`python test_julius.py`を実行すると、Pythonのコンソールと、Juliusのコンソールが起動する。

その状態で、マイクに向かって特定のワードで声掛けをすると、`test_julius.py`で設定した動作を行う。
