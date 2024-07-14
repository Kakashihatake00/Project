import newsapi
import requests

api_key = "1d84223d12314cfdae758ae01a5f537e"

url = 'https://newsapi.org/v2/top-headlines'
params = {'country': 'in', 'apiKey': api_key}
response = requests.get(url, params=params)


response_json = response.json()

for article in response_json['articles']:
    print(article['title'] and article ['description'])
    print('_____________________________________________')
    