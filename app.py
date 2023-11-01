from flask import Flask, render_template, request, send_file
import pandas as pd
import json
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    data = json.load(file)
    df = pd.DataFrame(data['messages'])
    df = df[df['text'].str.len() > 6]
    df.to_csv('result.csv', columns=['text'], index=False)
    urls = []
    for text in df['text']:
        urls.extend(re.findall(r'https?://\S+', text))
    url_df = pd.DataFrame(urls, columns=['urls'])
    url_df['urls'] = url_df['urls'].str.replace(r'[}{",]', '', regex=True)
    url_df.to_csv('urls.csv', index=False)
    return render_template('download.html')

@app.route('/download_result')
def download_result():
    return send_file('result.csv', as_attachment=True)

@app.route('/download_urls')
def download_urls():
    return send_file('urls.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
