from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import os
from time import sleep
import seaborn as sns
import matplotlib.pyplot as plt

def api_runner():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200) 
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'10',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'Your API Key Here', 
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = response.json()
        
        df = pd.json_normalize(data["data"])
        
        df["timestamp"] = pd.Timestamp.now()
        if not os.path.isfile('Crypto.csv'):
            df.to_csv('Crypto.csv', header='column_names', index=False)
        else:
            df.to_csv('Crypto.csv', mode='a', header=False, index=False)
            
        print("Data saved successfully.")

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"Connection Error: {e}")


print("Starting Scraper...")

for i in range(0):
    api_runner()
    print(f"API Runner Completed: Run {i+1}")
    sleep(60)
print("All runs finished!")


df = pd.read_csv('Crypto.csv')
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df3 = df.groupby('name', sort=False)[[
    'quote.USD.percent_change_1h',
    'quote.USD.percent_change_24h',
    'quote.USD.percent_change_7d',
    'quote.USD.percent_change_30d',
    'quote.USD.percent_change_60d',
    'quote.USD.percent_change_90d'
]].mean()

df4 = df3.stack()
df5 = df4.to_frame(name='values')

df7 = df5.reset_index()

df7 = df7.rename(columns={'level_1': 'percent_change'})

df7['percent_change'] = df7['percent_change'].replace({
    'quote.USD.percent_change_1h': '1h',
    'quote.USD.percent_change_24h': '24h',
    'quote.USD.percent_change_7d': '7d',
    'quote.USD.percent_change_30d': '30d',
    'quote.USD.percent_change_60d': '60d',
    'quote.USD.percent_change_90d': '90d'
})

print(df7.head(15))



print("Opening Plot 1 (Comparison)... Please close it to see Plot 2.")
sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')
plt.title('Crypto Price Change Trends')
plt.show()

df10 = df[['name','quote.USD.price','timestamp']]
df10 = df10.query("name == 'Bitcoin'")
df10['timestamp'] = pd.to_datetime(df10['timestamp'])

print("Opening Plot 2 (Bitcoin Trend)...")
sns.set_theme(style="darkgrid")
plt.figure(figsize=(12, 6))

sns.lineplot(x='timestamp', y='quote.USD.price', data = df10)

plt.title('Bitcoin Price Live Trend', fontsize=16)
plt.xlabel('Time')
plt.ylabel('Price (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()















































