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
            text = soup.get_text(separator='\\n', strip=True)  # 改行で区切り、前後の空白を削除
            f_text.write(text)
    except Exception as e:
        print(f"Error during HTML parsing or text extraction: {e}")
        return

    print(f"Successfully converted '{epub_file}' to '{text_file}'")

# 使用例
epub_file = 'your_epub_file.epub'  # 変換したいEPUBファイルのパス
output_dir = 'output'  # 出力ディレクトリ

epub_to_text(epub_file, output_dir)
