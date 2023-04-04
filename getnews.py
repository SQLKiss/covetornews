import requests

api_key='eda4bf5358654cafbee74d38c6c001f8'
country = None #'au' #'au'
q = "Crypto" #'Tesla'

baseurl = 'https://newsapi.org/v2/top-headlines?'
#baseurl = 'https://newsapi.org/v2/everything?'
requesturl = baseurl+'apiKey='+api_key + ('&country='+country if country is not None else "")+ ('&q='+q if q is not None else "")
response = requests.get(requesturl)

if response.status_code == 200:
    result = response.json()
    #print(result)
    authors=[]
    url = []
    for article in result['articles']:
        #if article['author'] == 'New Zealand Herald':
        #if article['author'] != 'New Zealand Herald':
        url.append(article['url'])
        #authors.append(article['author'])
    #authors = sorted(set(authors))
    #for author in authors:
    #    print(author)
    url = sorted(set(url))
    print('Could you please provide a summary (bullet points) on the news (URLs below):')
    for u in url:
        print(u)
else:
    print(f"Error: {response.status_code}")
