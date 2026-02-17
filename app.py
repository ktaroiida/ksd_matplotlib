import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# ページ設定（タイトルとアイコン）
st.set_page_config(page_title="VisualCSV - Streamlit", page_icon="📊", layout="wide")

# カスタムCSSでデザインをリッチにする
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #6366f1;
        color: white;
        font-weight: bold;
    }
    .stTitle {
        background: linear-gradient(to right, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("VisualCSV 📊")
st.markdown("### CSVファイルをアップロードして、すぐに日本語対応グラフを作成")

# サイドバーでの設定
st.sidebar.header("設定")
plot_type = st.sidebar.selectbox("グラフの種類", ["折れ線グラフ", "棒グラフ", "散布図"])
show_grid = st.sidebar.checkbox("グリッドを表示", value=True)

# ファイルアップローダー
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    try:
        # CSV読み込み
        df = pd.read_csv(uploaded_file)
        
        # データのプレビュー
        with st.expander("データのプレビュー"):
            st.dataframe(df.head(10))

        # 数値列の抽出
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            st.error("数値データを含む列が見つかりません。")
        else:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.write("#### 描画設定")
                y_axis = st.multiselect("表示する列 (Y軸)", numeric_cols, default=numeric_cols[:1])
                
                x_axis_options = df.columns.tolist()
                x_axis = st.selectbox("X軸にする列", x_axis_options)
                
                title = st.text_input("グラフのタイトル", "CSVデータの可視化")

            with col2:
                if y_axis:
                    # Matplotlibでの描画
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    for col in y_axis:
                        if plot_type == "折れ線グラフ":
                            ax.plot(df[x_axis], df[col], marker='o', label=col)
                        elif plot_type == "棒グラフ":
                            ax.bar(df[x_axis], df[col], label=col, alpha=0.7)
                        elif plot_type == "散布図":
                            ax.scatter(df[x_axis], df[col], label=col)

                    ax.set_title(title, fontsize=18, fontweight='bold')
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel("値")
                    ax.legend()
                    
                    if show_grid:
                        ax.grid(True, linestyle='--', alpha=0.6)
                    
                    # 日本語ラベル対応のために tight_layout を適用
                    plt.xticks(rotation=45)
                    fig.tight_layout()
                    
                    # Streamlitにグラフを表示
                    st.pyplot(fig)
                    
                    # ダウンロードボタン
                    import io
                    buf = io.BytesIO()
                    fig.savefig(buf, format="png", dpi=150)
                    st.download_button(
                        label="グラフを画像として保存",
                        data=buf.getvalue(),
                        file_name="graph.png",
                        mime="image/png"
                    )
                else:
                    st.warning("表示する列を少なくとも1つ選択してください。")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

else:
    st.info("👆 左のボタンまたはドラッグ＆ドロップでCSVファイルをアップロードしてください。")

# フッター
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & Matplotlib (Japanize support)")
