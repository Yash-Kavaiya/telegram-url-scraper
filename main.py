import json
import pandas as pd

with open('result.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data['messages'])  # Assuming 'messages' is the key containing your messages

# Filter messages with length greater than 6
df = df[df['text'].str.len() > 6]

df.to_csv('result.csv', columns=['text'], index=False)
import pandas as pd
from textblob import TextBlob
df = pd.read_csv('result.csv')
df['sentiment'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
df.to_csv('result_with_sentiment.csv', index=False)
