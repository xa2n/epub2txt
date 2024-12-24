# EPUB to Text Converter

このスクリプトは、EPUB ファイルを HTML に変換し、さらに HTML からテキストを抽出してテキストファイルを作成する Python スクリプトです。Pandoc と BeautifulSoup4 ライブラリを使用しています。

## 動作環境

- Python 3
- Pandoc
- BeautifulSoup4

## 事前準備

### 1. Pandoc のインストール

Pandoc がインストールされている必要があります。以下の手順でインストールしてください。

- **Windows:** [Pandoc の公式サイト](https://pandoc.org/installing.html)からインストーラーをダウンロードして実行してください。
- **macOS:** Homebrew を使用している場合は、ターミナルで `brew install pandoc` を実行してください。
- **Linux:** 各ディストリビューションのパッケージマネージャーを使用してインストールしてください (例: Ubuntu の場合は `sudo apt-get install pandoc`)。

### 2. 必要な Python ライブラリのインストール

以下のコマンドを実行して、BeautifulSoup4 をインストールしてください。

```bash
pip install beautifulsoup4
```

## 使用方法

1. このリポジトリをクローンするか、`epub_converter.py` をダウンロードします。
2. `epub_converter.py` ファイル内の `epub_file` 変数に変換したい EPUB ファイルのパスを設定します。
3. `output_dir` 変数に変換後の HTML ファイルとテキストファイルを保存するディレクトリのパスを設定します。
4. ターミナルまたはコマンドプロンプトで、`epub_converter.py` が保存されているディレクトリに移動します。
5. 以下のコマンドを実行してスクリプトを実行します。

```bash
python epub_converter.py
```

実行が完了すると、`output_dir` で指定したディレクトリに HTML ファイルとテキストファイルが作成されます。

## スクリプトの解説

```python
import subprocess
import os
from bs4 import BeautifulSoup

def epub_to_text(epub_file, output_dir):
    """
    EPUBファイルをHTMLに変換し、HTMLからテキストファイルを作成する関数。

    Args:
        epub_file: EPUBファイルのパス。
        output_dir: 出力ディレクトリのパス。
    """

    # 出力ディレクトリが存在しない場合は作成する
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # EPUBファイル名から拡張子を除いたものをベース名とする
    base_name = os.path.splitext(os.path.basename(epub_file))[0]

    # 1. EPUBをHTMLに変換
    html_file = os.path.join(output_dir, f"{base_name}.html")
    try:
        subprocess.run(['pandoc', '-f', 'epub', '-t', 'html', epub_file, '-o', html_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during EPUB to HTML conversion: {e}")
        return

    # 2. HTMLからテキストを抽出
    text_file = os.path.join(output_dir, f"{base_name}.txt")
    try:
        with open(html_file, 'r', encoding='utf-8') as f_html, open(text_file, 'w', encoding='utf-8') as f_text:
            soup = BeautifulSoup(f_html, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)  # 改行で区切り、前後の空白を削除
            f_text.write(text)
    except Exception as e:
        print(f"Error during HTML parsing or text extraction: {e}")
        return

    print(f"Successfully converted '{epub_file}' to '{text_file}'")

# 使用例
epub_file = 'your_epub_file.epub'  # 変換したいEPUBファイルのパス
output_dir = 'output'  # 出力ディレクトリ

epub_to_text(epub_file, output_dir)
```

このスクリプトは以下の手順で EPUB からテキストへの変換を行います。

1. **Pandoc を使用して EPUB を HTML に変換:** `subprocess` モジュールを使用して Pandoc コマンドを実行し、EPUB ファイルを HTML ファイルに変換します。
2. **BeautifulSoup4 を使用して HTML からテキストを抽出:** `BeautifulSoup` オブジェクトを作成して HTML ファイルを解析し、`get_text()` メソッドを使用してテキストを抽出します。抽出したテキストは、改行で区切られ、前後の空白が削除されます。
3. **テキストファイルへの書き込み:** 抽出したテキストをテキストファイルに書き込みます。

## 注意点

- EPUB ファイルの構造によっては、テキストの抽出がうまくいかない場合があります。その場合は、BeautifulSoup のセレクタなどを調整して、適切なテキストを抽出できるようにコードを修正する必要があります。
- 大きな EPUB ファイルを処理する場合は、時間がかかることがあります。
- このコードは基本的な例です。必要に応じて、エラー処理やログ出力などの機能を追加してください。
- Pandoc は非常に多くのフォーマットに対応しています。詳細は [Pandoc User's Guide](https://pandoc.org/MANUAL.html) を参照してください。

## ライセンス

このスクリプトは MIT ライセンスの下で公開されています。詳細は LICENSE ファイルをご覧ください.
