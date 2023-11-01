import json
import pandas as pd
import re

with open('result.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)
text=[]
for i in df.messages:
    text.append(i['text'])
print(len(text))
df = pd.DataFrame(data['messages']) 
df = df[df['text'].str.len() > 6]
df.to_csv('result.csv', columns=['text'], index=False)
import time
time.sleep(5)
df = pd.read_csv('result.csv')
url_pattern = r'https?://\S+'
def extract_urls(text):
    urls = re.findall(url_pattern, text)
    return [url.replace('}', '').replace("'", "") for url in urls]
df['urls'] = df['text'].apply(extract_urls)
all_urls = [url for url_list in df['urls'] for url in url_list]
url_l=[]
for url in all_urls:
    print(url)
    url_l.append(url)
url_df = pd.DataFrame(url_l, columns=['urls'])
url_df['urls'] = url_df['urls'].str.replace(r'[}{",]', '', regex=True)
url_df.to_csv('urls.csv', index=False)

