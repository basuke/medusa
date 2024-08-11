Pythonでスクリプトを作りたいので手伝ってください。仕様は以下の通りです。

- 指定のURLから到達できるHTMLを静的HTMLにlinux系のコマンドラインツール。名前はmedusa。

## 使い方
python medusa.py entry_url [path] [--output=dir] [--rewite=path]

- entry_url: スクレープを始める最初のURL。アクセスできなければエラー
- path: スクレープの対象となるpath。このpathの子要素へのアクセスはスクレープの対象とし、外側へのリンクはノータッチで。省略されたらentry_urlのpathを使う
- --output=dir: スクレープした結果を書き出すディレクトリ。省略されたらURLをstdoutに出力
- --rewrite=path: スクレープしたHTMLのURLが変わるものを列挙する。省略されたら書き出さない

## 動作
- プログラムは、まず引数を受け取って指定のURLをスクレープ対象のキューに入れる。
- 対象キューからURLを取り出し、コンテンツをダウンロードする。
- ダウンロードしたファイルがHTMLだった場合
  - その中に列挙されているhyperlink, image、css/javascript, そのほかのURLをリスト
  - もしリンク先のURLが同じホストで同じポート、そしてpathのサブコンテンツだったばあい、そのURLもスクレープの対象キューに追加。コンテンツHTMLのURLを置き換える。
  - URLがxxx.htmlという静的なpath出はなかった場合、保存するHTMLのパスは以下の通りに決める
    - もしディレクトリだった場合、`index`をつける
    - URLにquerystringが含まれていた場合、?を`_` に、&を`-` に置き換えてパスに追加
    - 最後に、.htmlをつける
    - 例
      - http://example.com/ は index.html
      - http://example.com/xxx は xxx.html
      - http://example.com/?yyy=zzz は index_yyy-zzz.html
      - http://example.com/xxx?yyy=zzz は xxx_yyy-zzz.html
- outputに相対的な位置を保持しながら保存。outputが指定されていない場合はURLと新しいURLをstdoutに出力
- 対象キューが空になるまで繰り返す
- 書き換えたURLのリストをrewrite_file へ書き出す

では少しずつ実装していきましょう。まずは、URLを取得する関数を作りましょう。
