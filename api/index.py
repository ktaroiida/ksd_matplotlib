from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import io
import base64

import os

app = Flask(__name__, template_folder='../templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルが見つかりません'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400

    try:
        # Load CSV
        df = pd.read_csv(file)
        
        # Basic validation
        if df.empty:
            return jsonify({'error': 'CSVファイルが空です'}), 400

        # Create plot
        plt.figure(figsize=(10, 6))
        
        # Try to plot numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
             return jsonify({'error': '数値データを含む列が見つかりません'}), 400
        
        # Simple plot: if first col is not numeric, use as label
        first_col = df.columns[0]
        if first_col not in numeric_cols:
            x_label = first_col
            y_cols = numeric_cols
            for col in y_cols:
                plt.plot(df[x_label], df[col], marker='o', label=col)
            plt.xticks(rotation=45)
        else:
            for col in numeric_cols:
                plt.plot(df[col], marker='o', label=col)
        
        plt.title('CSVデータの可視化', fontsize=16)
        plt.xlabel(df.columns[0] if first_col not in numeric_cols else 'インデックス')
        plt.ylabel('値')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return jsonify({'image': f'data:image/png;base64,{img_str}'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
