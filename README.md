### Ope recording system
眼科手術動画を解析し、録画の開始・停止をリアルタイムに行えるアプリケーションの構築を目指しています。
sample.mp4およびmodel.hdf5はGoogle Drive<br>
https://drive.google.com/drive/u/2/folders/1a55Sq5USy4fqW613d9_fjgqTRQE4mZiy<br>
にあるため、閲覧権限がない人は升本に連絡してください。


#### ロジック
常に眼の領域（上瞼から下瞼にかけてのsegmentation）を行う<br>
何回か連続して一定の面積を上回る or 下回るなら録画の開始 or 停止となる<br>
また、録画の開始・停止時に(手術室番号)_(S or C)_(timestamp、例えば20200401231612).datを保存する（中身は空）<br>
これは録画システムと連携するためのトリガーとして使うため


#### ファイルの内容について
main.py・・録画システムの共有フォルダに指定すると、datファイルが出力される<br>
unused.py・・・current directoryにoutput動画とdatファイルが出力される。output動画は録画中に青枠線が引かれる動画

#### 今後の改善点
そもそも目の領域で判定するシステムだと器具を置いた際に対応できない。<br>
また、目が写っていない動画に慣れていないことから、、結構停止漏れが生じることもある。<br>
白内障 or 注射手術ならだいたいできそう。<br>
眼瞼手術(目の面積が極端に少ない) or 緑内障（茶目を見る手術なので見え方が違う）or 硝子体手術（眼底を見る手術なので見え方が違う）ができたら売り物になるか。

### Juliusによる音声認識機能の追加

`main.py` にJuliusManagerクラスが追加。

このクラスはJuliusという音声認識システムの制御に用いられる。

検証は現在のところWindows環境でのみ行われている。

#### 音声認識環境構築

#### Juliusをインストール

https://julius.osdn.jp/index.php?q=newjulius.html

上記URLの[Windows用実行バイナリ](https://github.com/julius-speech/julius/releases/download/v4.5/julius-4.5-win32bin.zip)をクリックしてダウンロード。

ダウンロードした一群のディレクトリを適当な場所（Program Files等）に移動。

#### パスを通す

julius.exeの保存場所を含めてexeファイルを実行すれば動作するが、`julius`ワードをコマンドプロンプトで入力するだけで動作するようにパスを通す。

Windowsの「システム環境変数の編集」を開いて、環境変数ボタンをクリック。ユーザー環境変数・システム環境変数どちらでも良いので、PATH変数の値に、先述の一群のディレクトリの場所を設定。

#### インストール確認

以下をコマンドプロンプトで実行して、Help一覧が表示されるかどうかを確認。

```bash
julius --help
```

#### 音声認識用パッケージの設置

Julius音声認識パッケージのディクテーションキット (dictation-kit)をダウンロードして展開。

展開先は `(本リポジトリのパス)\julius-4.5\julius-kit\dictation-kit-4.5\` 以下に`bin`、`model`、`src`フォルダ他各種ファイルが展開されている状態にする。

> https://julius.osdn.jp/index.php?q=dictation-kit.html

#### Pythonの設定

PIPで`termcolor`をインストールする。

```bash
pip install termcolor
```

#### 音声認識の機能のみをテスト

上記設定が出来たら、`python test_julius.py`を実行すると、Pythonのコンソールと、Juliusのコンソールが起動する。

その状態で、マイクに向かって特定のワードで声掛けをすると、`test_julius.py`で設定した動作を行う。
