#list of subjects/questions
#current utc date -1 as a "from"
#call news api for each one news in the subject
#read content and convert to a bullet point with URL at the end

topics = ["Australia","New%20Zealand"] #,"Auto","Games","Economy","Crypto"]

###################################

articleslimit = 1 #number of article(s) per subject
sortBy = "publishedAt" #fresh news #"publishedAt" #"relevancy" #"popularity"


from datetime import datetime, timedelta
nfrom = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d') #UTC -1 day to cover all 24hour news


import requests,os
newsApiKey = os.getenv("NEWSAPIKEY")

#collect articles
articles = {}
for topic in topics:
    requesturl = f'https://newsapi.org/v2/everything?'
    requesturl +='apiKey='+newsApiKey 
    requesturl +='&language=en'
    requesturl +="&sortBy="+sortBy
    requesturl +='&from='+nfrom
    requesturl +=f'&pageSize={articleslimit}'
    requesturl +='&q='+topic

    #print(requesturl) ##########
    articles[topic] = []
    response = requests.get(requesturl)
    if response.status_code == 200:
        result = response.json()
        for article in result['articles']:
            articles[topic].append(article)
    else:
        print(f"Error: {response.status_code}")


print(articles)


exit(0)

#for topic, news in articles.items():
#    print(topic.replace('%20',' ')+":")
#    for artice in news:
#        print(artice['title'])

import openai
openai.api_key = os.getenv("OPENAPIKEY")
openai.organization = os.getenv("OPENAPIORG")

processedArticles = {}
for topic, news in articles.items():
    processedArticles[topic] = []
    for artice in news:
        content = """Summarise text below into a short story-line with a two-three emoji (assisting describing content):
        """ + article['description'][:1024]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}], temperature=0.25
        )
        processedArticles[topic].append(completion.choices[0].message['content'])

for topic, content in processedArticles.items():
    print(topic.replace('%20',' ')+":")
    for artice in content:
        print(artice)


#I need to show subjects and then the lines
#auto news:
#...
#games, etc..
