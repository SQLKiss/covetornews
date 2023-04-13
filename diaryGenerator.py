from datetime import datetime, timedelta
import requests,os,openai

#list of subjects/questions
#current utc date -1 as a "from"
#call news api for each one news in the subject
#read content and convert to a bullet point with URL at the end

topics = ["Australia","New%20Zealand","Cars"] #,"Auto","Games","Economy","Crypto"]

###################################

articleslimit = 3 #number of article(s) per subject
sortBy = "publishedAt" #fresh news #"publishedAt" #"relevancy" #"popularity"

nfrom = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d') #UTC -1 day to cover all 24hour news

newsApiKey = os.getenv("NEWSAPIKEY")

#collect articles
articles = {}
for topic in topics:
    requesturl = 'https://newsapi.org/v2/everything?'
    requesturl +='apiKey='+newsApiKey 
    requesturl +='&language=en'
    requesturl +="&sortBy="+sortBy
    requesturl +='&from='+nfrom
    requesturl +='&pageSize=10'
    requesturl +='&q='+topic

    #get 5 topics and skip existing

    #print(requesturl) ##########
    articles[topic] = []
    response = requests.get(requesturl)
    if response.status_code == 200:
        result = response.json()
        limit = 0
        for arr in result['articles']:
            if limit>=articleslimit:
                break
            
            content = {'source': arr['source']['name'],'author':arr['author'], 'title':arr['title'], 'url':arr['url'], 'description':arr['description']}
            ##urlToImage #publishedAt
            
            #just to pick up all with dups
            #limit+=1
            #articles[topic].append(content)

            alreadyexists = 0
            for topic, news in articles.items():
                for title in news:
                    if content['title'] in title['title']:
                        alreadyexists = 1
                        break
            if alreadyexists==0:
                limit+=1
                articles[topic].append(content) #(arr)
    else:
        print(f"Error: {response.status_code}")


#for topic, news in articles.items():
#    print(topic.replace('%20',' ')+":")
#    for artice in news:
#        print(artice['title'])


openai.api_key = os.getenv("OPENAPIKEY")
openai.organization = os.getenv("OPENAPIORG")

processedArticles = {}
for topic, news in articles.items():
    processedArticles[topic] = []
    for article in news:
        content = """Summarise text below into a short story-line with a two-three emoji (assisting describing content, but not replacing the content):
        """ + article['description'][:1024]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}], temperature=0.25
        )
        processedArticles[topic].append(completion.choices[0].message['content']+" <i>(" + article['source'] + ")</i>")

message = ""
for topic, content in processedArticles.items():
    message += "\n<b>"+topic.replace('%20',' ')+":</b>\n"
    #print(topic.replace('%20',' ')+":")
    for artice in content:
        message += artice + "\n"
        #print(artice)
    #print("")

#print(message)
telegramToken = os.getenv("TELEGRAMBOTKEY")
chat_id = "-1001783307848" #CovetorNews

requesturl = "https://api.telegram.org/bot" + telegramToken + "/sendMessage" + "?chat_id=" + chat_id + "&parse_mode=HTML" + "&text=" + message 
response = requests.get(requesturl)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")


