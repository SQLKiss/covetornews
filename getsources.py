import requests

api_key='eda4bf5358654cafbee74d38c6c001f8'
country = None #'au'
q = None #'Tesla'

baseurl = 'https://newsapi.org/v2/top-headlines/sources?'
#baseurl = 'https://newsapi.org/v2/everything?'
requesturl = baseurl+'apiKey='+api_key + ('&country='+country if country is not None else "")+ ('&q='+q if q is not None else "")
#print(requesturl)
response = requests.get(requesturl)

if response.status_code == 200:
    result = response.json()
    sourcelist = []
    #print(result)
    for src in result['sources']:
        sourcelist.append(src['country'])
        #print(src['id']) #country #id
    sourcelist = sorted(set(sourcelist))
    #print(sourcelist)
    for src in sourcelist:
        print(src)
else:
    print(f"Error: {response.status_code}")
