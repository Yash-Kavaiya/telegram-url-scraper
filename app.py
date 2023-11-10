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
        if isinstance(text, list):
            # If 'text' is a list, iterate over its elements
            for item in text:
                if isinstance(item, dict):
                    # If 'item' is a dictionary, extract values and apply regex
                    for value in item.values():
                        urls.extend(re.findall(r'https?://\S+', str(value)))
                else:
                    # If 'item' is not a dictionary, apply the regular expression directly
                    urls.extend(re.findall(r'https?://\S+', str(item)))
        elif isinstance(text, dict):
            # If 'text' is a dictionary, extract values and apply regex
            for value in text.values():
                urls.extend(re.findall(r'https?://\S+', str(value)))
        else:
            # If 'text' is not a list or dictionary, apply the regular expression directly
            urls.extend(re.findall(r'https?://\S+', str(text)))

    url_df = pd.DataFrame(urls, columns=['urls'])
    url_df['urls'] = url_df['urls'].str.replace(r'[}{",]', '', regex=True)
    
    url_list = url_df['urls'].tolist()
    
    return render_template('download.html', urls=url_list)

@app.route('/download_result')
def download_result():
    return send_file('result.csv', as_attachment=True)

@app.route('/download_urls')
def download_urls():
    return send_file('urls.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
