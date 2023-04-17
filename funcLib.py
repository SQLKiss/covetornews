#--------------------------------#
def convertNewsResponseToContent(response):
    articles = []
    if response.status_code == 200:
        result = response.json()
        for arr in result['articles']:
            content = {'source': arr['source']['name'],'author':arr['author'], 'title':arr['title'], 'url':arr['url'], 'description':arr['description'], 'content':arr['content']}
            articles.append(content)
    else:
        print(f"Error: {response.status_code}")
    return articles

def getNewsArticles(topic, articleslimit = 2, sortBy = "publishedAt"):
    from datetime import datetime, timedelta
    import os,requests
    nfrom = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d') #UTC -1 day to cover all 24hour news
    newsApiKey = os.getenv("NEWSAPIKEY")
    requesturl = 'https://newsapi.org/v2/everything?'+'apiKey='+newsApiKey+'&language=en'+"&sortBy="+sortBy+'&from='+nfrom+f'&pageSize={articleslimit}'
    requesturl +='&q='+topic

    response = requests.get(requesturl)
    return convertNewsResponseToContent(response)
#--------------------------------#

#--------------------------------#
def getArticleSummary(content, temperature=0.25):
    import os,openai
    openai.api_key = os.getenv("OPENAPIKEY")
    openai.organization = os.getenv("OPENAPIORG")
    result = """Summarise text below into a short story-line with a two-three emoji (assisting describing content, but not replacing the content):
    """ + content[:2048]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": result}], temperature=temperature
    )
    return completion.choices[0].message['content']
#--------------------------------#

#--------------------------------#
def sendTelegramMessage(message, debug = 1):
    import os,requests
    if debug == 0:
        chat_id = "-1001783307848" #CovetorNews
        telegramToken = os.getenv("TELEGRAMBOTKEY")
    else:
        chat_id = "-1001371860541" #TestTelegramChannel
        telegramToken = os.getenv("TELEGRAMBOTKEYTEST")
    
    requesturl = "https://api.telegram.org/bot" + telegramToken + "/sendMessage" + "?chat_id=" + chat_id + "&parse_mode=HTML" + "&text=" + message 
    requesturl +="&disable_web_page_preview=true"
    return requests.get(requesturl)
#--------------------------------#