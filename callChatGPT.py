
country = "au" #'au'
q = None #"Money"


##--------------------------------------

import openai,requests,os
openAIapiKey = os.getenv("OPENAPIKEY")
openAIorganization = os.getenv("OPENAPIORG")
newsApiKey = os.getenv("NEWSAPIKEY")

baseurl = 'https://newsapi.org/v2/top-headlines?'
requesturl = baseurl+'apiKey='+newsApiKey + ('&country='+country if country is not None else "")+ ('&q='+q if q is not None else "")
response = requests.get(requesturl)

chatRequest = []
chatRequest.append("Could you please provide a summary (bullet points) on the news (URLs below).")
chatRequest.append("For each bullet point add full URL as source in (brackets) at the end")
#chatRequest.append("Write a A4 size mystical adventure story using the news from URLs below")
#chatRequest.append("Pretend to be a very suspision reporter with a tinfoil hat")
#chatRequest.append("Could you please provide a summary (bullet points) on the news (URLs below).")

if response.status_code == 200:
    result = response.json()
    for article in result['articles']:
        chatRequest.append(article['url'])
else:
    print(f"Error: {response.status_code}")
    exit(0)

chatRequest = sorted(set(chatRequest)) #just in case remove duplicates
chatRequest = chatRequest[:7] #get only 5 first URLs (as first two are request messages)
content = "\n".join(chatRequest) #split array into lines of text

openai.api_key = openAIapiKey
openai.organization = openAIorganization
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": content}
  ],
  temperature=0
)

print(completion.choices[0].message['content'])