# VisualCSV - 日本語対応グラフ作成アプリ

CSVファイルをアップロードして、Matplotlibで美しいグラフを生成するStreamlitアプリケーションです。

## 🚀 機能

- CSVファイルのアップロード（ドラッグ&ドロップ対応）
- 日本語ラベルの完全サポート（japanize-matplotlib使用）
- 複数のグラフタイプ（折れ線、棒、散布図）
- インタラクティブな設定UI
- グラフの画像保存機能

## 📦 ローカルでの実行方法

```bash
# 依存ライブラリのインストール
pip install -r requirements.txt

# アプリの起動
streamlit run app.py
```

ブラウザで自動的に開きます（通常は `http://localhost:8501`）

## 🌐 Streamlit Cloudでのデプロイ方法

1. GitHubリポジトリにコードをプッシュ
2. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス
3. GitHubアカウントでサインイン
4. "New app" をクリック
5. リポジトリ、ブランチ、メインファイル（`app.py`）を選択
6. "Deploy" をクリック

数分でアプリが公開されます！

## 📊 使い方

1. CSVファイルをアップロード
2. サイドバーでグラフの種類を選択
3. 表示する列とX軸を設定
4. グラフが自動生成されます
5. 必要に応じて画像として保存

## 🛠 技術スタック

- **Streamlit**: Webアプリケーションフレームワーク
- **Matplotlib**: グラフ描画ライブラリ
- **japanize-matplotlib**: 日本語フォント対応
- **Pandas**: データ処理

## 📝 サンプルデータ

`sample.csv` を使ってすぐに試すことができます。
