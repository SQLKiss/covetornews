
source = "top-headlines"
articleslimit = 5
country = None #'au'
q = None #"chatGPT" #"Money"
nfrom = None #"2023-04-03"
nto = None #"2023-04-03"

##--------------------------------------

import openai,requests,os
openAIapiKey = os.getenv("OPENAPIKEY")
openAIorganization = os.getenv("OPENAPIORG")
newsApiKey = os.getenv("NEWSAPIKEY")

baseurl = f'https://newsapi.org/v2/{source}?'
requesturl = baseurl
requesturl +='apiKey='+newsApiKey 
requesturl +='&language=en'
requesturl +="&sortBy=popularity" #publishedAt #relevancy
requesturl +=('&country='+country if country is not None and source == "top-headlines" else "") 
requesturl +=('&from='+nfrom if nfrom is not None else "")
requesturl +=('&to='+nto if nto is not None else "")
requesturl +=('&q='+q if q is not None else "")
requesturl +=f'&pageSize={articleslimit}'

chatRequest = []
#chatRequest.append("Could you please provide a summary (bullet points) on the news (URLs below).")
#chatRequest.append("For each bullet point add source in (brackets) at the end") #full URL as 
#chatRequest.append("Write a A4 size mystical adventure story using the news from URLs below")
#chatRequest.append("Pretend to be a very suspision reporter with a tinfoil hat")

chatRequest.append("Tell me a story based on the news (titles below):")

response = requests.get(requesturl)
if response.status_code == 200:
    result = response.json()
    for article in result['articles']:
        #chatRequest.append(article['url'])
        chatRequest.append(article['title'])
else:
    print(f"Error: {response.status_code}")
    exit(0)

#chatRequest = sorted(set(chatRequest)) #just in case remove duplicates

if len(chatRequest)<3:
    requesturl = requesturl
    print("No data returned from this (debug mode key is not hidden !!!):")
    print(requesturl)
    exit(0)

content = "\n".join(chatRequest) #split array into lines of text

#print(content)
#exit(0)

openai.api_key = openAIapiKey
openai.organization = openAIorganization
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a time traveller and a great story teller"},
    {"role": "user", "content": content}
  ],
  temperature=0
)

print(completion.choices[0].message['content'])