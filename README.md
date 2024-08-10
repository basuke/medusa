- 指定のURLから到達できるHTMLを静的HTMLにlinux系のコマンドラインツール
- 引数に受け取るのは
  - url entry point: スクレープを始める最初のURL。アクセスできなければエラー
  - path: スクレープの対象となるpath。このpathの子要素へのアクセスはスクレープの対象とし、外側へのリンクはノータッチで。
  - output_dir: スクレープした結果を書き出すディレクトリ。
  - rewrite_file: スクレープしたHTMLのURLが変わるものを列挙する
- プログラムは、まず引数を受け取って指定のURLをスクレープ対象のキューに入れる。
- 対象キューからURLを取り出し、コンテンツをダウンロードする。
- ダウンロードしたファイルがHTMLだった場合
  - その中に列挙されているhyperlink, css/javascript, そのほかのURLをリスト
  - もしリンク先のURLがpathの中に納まっていたらそのURLもスクレープの対象キューに追加。コンテンツHTMLのURLを置き換える。
- output_dirに相対的な位置を保持しながら保存
- 対象キューが空になるまで繰り返す
- 書き換えたURLのリストをrewrite_file へ書き出す
