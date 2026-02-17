# Streamlit + Matplotlib で日本語対応グラフアプリを作る完全ガイド

## 🎯 このガイドについて

CSVファイルをアップロードして、日本語ラベル付きのグラフを自動生成するWebアプリケーションを、**無料で公開する方法**を解説します。

**デモ**: https://ksdmatplotlib-vfzqtchyftgeuy7vywkqq5.streamlit.app/

---

## 📋 必要なもの

- Python 3.8以上（推奨: 3.10以上）
- GitHubアカウント（無料）
- テキストエディタ（VS Code、PyCharmなど）

---

## 🚀 クイックスタート（5分で動かす）

### 1. プロジェクトフォルダを作成

```bash
mkdir csv-graph-app
cd csv-graph-app
```

### 2. 必要なファイルを作成

#### `requirements.txt`
```text
streamlit
pandas
matplotlib
japanize-matplotlib
setuptools
```

#### `app.py`
```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

st.set_page_config(page_title="CSVグラフ作成", page_icon="📊")

st.title("📊 CSVグラフ作成アプリ")
st.markdown("### CSVファイルをアップロードして、日本語対応グラフを作成")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    try:
        # CSV読み込み
        df = pd.read_csv(uploaded_file)
        
        # データプレビュー
        with st.expander("データのプレビュー"):
            st.dataframe(df.head(10))

        # 数値列の抽出
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            st.error("数値データを含む列が見つかりません。")
        else:
            # 列選択
            y_axis = st.multiselect("表示する列 (Y軸)", numeric_cols, default=numeric_cols[:1])
            x_axis = st.selectbox("X軸にする列", df.columns.tolist())
            
            if y_axis:
                # グラフ作成
                fig, ax = plt.subplots(figsize=(10, 6))
                
                for col in y_axis:
                    ax.plot(df[x_axis], df[col], marker='o', label=col)

                ax.set_title("CSVデータの可視化", fontsize=18, fontweight='bold')
                ax.set_xlabel(x_axis)
                ax.set_ylabel("値")
                ax.legend()
                ax.grid(True, linestyle='--', alpha=0.6)
                
                plt.xticks(rotation=45)
                fig.tight_layout()
                
                # グラフ表示
                st.pyplot(fig)
            else:
                st.warning("表示する列を少なくとも1つ選択してください。")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.info("👆 CSVファイルをアップロードしてください。")
```

#### `sample.csv`（テスト用）
```csv
月,売上,利益
1月,100,20
2月,150,35
3月,120,25
4月,200,50
5月,180,40
6月,250,70
```

### 3. ローカルで動作確認

```bash
# ライブラリをインストール
pip install -r requirements.txt

# アプリを起動
streamlit run app.py
```

ブラウザで `http://localhost:8501` が自動的に開きます。

---

## 🌐 Streamlit Cloudで無料公開

### 1. GitHubにプッシュ

```bash
# Gitリポジトリを初期化
git init

# .gitignoreを作成
echo "venv/
__pycache__/
*.pyc
.DS_Store" > .gitignore

# コミット
git add .
git commit -m "Initial commit: CSV graph app"

# GitHubにプッシュ（事前にGitHubでリポジトリを作成）
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
git branch -M main
git push -u origin main
```

### 2. Streamlit Cloudでデプロイ

1. **https://streamlit.io/cloud** にアクセス
2. **GitHubアカウントでサインイン**
3. **"New app"** をクリック
4. 以下を入力：
   - **Repository**: `あなたのユーザー名/リポジトリ名`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. **"Deploy"** をクリック

**数分で公開URL（例: `https://your-app.streamlit.app`）が発行されます！**

---

## ❓ よくあるエラーと解決方法

### エラー1: `ModuleNotFoundError: No module named 'distutils'`

**原因**: Python 3.12以降で `distutils` が削除された

**解決方法**: `requirements.txt` に `setuptools` を追加
```text
streamlit
pandas
matplotlib
japanize-matplotlib
setuptools  ← これを追加
```

---

### エラー2: 日本語が豆腐（□□□）になる

**原因**: 日本語フォントが読み込まれていない

**解決方法**: `import japanize_matplotlib` を必ず書く
```python
import matplotlib.pyplot as plt
import japanize_matplotlib  # ← これを追加（pltのインポート後でOK）
```

---

### エラー3: Streamlit Cloudでデプロイできない

**原因**: ファイル構成やファイル名が間違っている

**チェックリスト**:
- ✅ `requirements.txt` がリポジトリのルートにある
- ✅ ファイル名は `requirements.txt`（小文字）
- ✅ メインファイルは `app.py`
- ✅ GitHubにプッシュ済み

**ログの確認方法**:
1. Streamlit Cloudの管理画面で "Manage app" をクリック
2. ログを確認してエラーメッセージを読む

---

### エラー4: `ERR_CONNECTION_REFUSED` (ローカル)

**原因**: Streamlitサーバーが起動していない

**解決方法**:
```bash
streamlit run app.py
```
を実行して、サーバーを起動する

---

## 🎓 なぜこの構成で成功するのか？

### Vercelではなく、Streamlit Cloudを使う理由

| 項目 | Vercel | Streamlit Cloud |
|------|--------|-----------------|
| **Python対応** | ❌ サーバーレス関数のみ（制限あり） | ✅ 完全対応 |
| **Matplotlib** | ❌ フォント・描画ライブラリで問題発生 | ✅ 完全サポート |
| **日本語フォント** | ❌ japanize-matplotlibが動かない | ✅ 問題なく動作 |
| **デプロイの簡単さ** | 🟡 設定が必要 | ✅ GitHubと連携するだけ |
| **無料枠** | ✅ あり | ✅ 無制限（個人利用） |

### 技術的なポイント

#### 1. `japanize-matplotlib` の仕組み
```python
import japanize_matplotlib
```
このインポートだけで、Matplotlibのデフォルトフォントが日本語対応フォント（IPAexゴシック）に自動的に切り替わります。

#### 2. `setuptools` が必要な理由
- Python 3.12から `distutils` が標準ライブラリから削除された
- `japanize-matplotlib` は内部で `distutils.version` を使用
- `setuptools` をインストールすると、`distutils` の互換レイヤーが提供される

#### 3. Streamlitの利点
```python
st.pyplot(fig)  # Matplotlibのfigureを自動的に画像に変換して表示
```
Streamlitは科学計算・データ分析アプリに特化しており、Matplotlib、Pandas、NumPyなどを完全サポートしています。

---

## 📚 応用例

### グラフの種類を選べるようにする

```python
plot_type = st.sidebar.selectbox("グラフの種類", ["折れ線グラフ", "棒グラフ", "散布図"])

if plot_type == "折れ線グラフ":
    ax.plot(df[x_axis], df[col], marker='o', label=col)
elif plot_type == "棒グラフ":
    ax.bar(df[x_axis], df[col], label=col, alpha=0.7)
elif plot_type == "散布図":
    ax.scatter(df[x_axis], df[col], label=col)
```

### グラフを画像として保存できるようにする

```python
import io

buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=150)
st.download_button(
    label="グラフを画像として保存",
    data=buf.getvalue(),
    file_name="graph.png",
    mime="image/png"
)
```

---

## 🔗 参考リンク

- **Streamlit公式ドキュメント**: https://docs.streamlit.io/
- **Matplotlib公式ドキュメント**: https://matplotlib.org/
- **japanize-matplotlib**: https://github.com/uehara1414/japanize-matplotlib
- **Streamlit Community Cloud**: https://streamlit.io/cloud

---

## 📝 まとめ

✅ **Streamlit + Matplotlib + japanize-matplotlib** で日本語対応グラフアプリを作成  
✅ **ローカルで動作確認** → **GitHubにプッシュ** → **Streamlit Cloudでデプロイ**  
✅ **無料で公開可能**（個人利用なら無制限）  
✅ **Python 3.12以降は `setuptools` を忘れずに！**

---

**作成日**: 2026年2月17日  
**デモアプリ**: https://ksdmatplotlib-vfzqtchyftgeuy7vywkqq5.streamlit.app/
