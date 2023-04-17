#--------------------------------#
def getNewsArticles(topic, articleslimit = 2, sortBy = "publishedAt"):
    from datetime import datetime, timedelta
    import os,requests
    nfrom = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d') #UTC -1 day to cover all 24hour news
    newsApiKey = os.getenv("NEWSAPIKEY")
    requesturl = 'https://newsapi.org/v2/everything?'+'apiKey='+newsApiKey+'&language=en'+"&sortBy="+sortBy+'&from='+nfrom+f'&pageSize={articleslimit}'
    requesturl +='&q='+topic

    response = requests.get(requesturl)
    articles = []
    if response.status_code == 200:
        result = response.json()
        for arr in result['articles']:
            content = {'source': arr['source']['name'],'author':arr['author'], 'title':arr['title'], 'url':arr['url'], 'description':arr['description'], 'content':arr['content']}
            articles.append(content)
    else:
        print(f"Error: {response.status_code}")
    return articles

def getNewsIOArticles(q, articleslimit = 2, category = 'top'):
    #category = "business,entertainment" #,environment,food,health,politics,science,sports,technology,top,tourism,world
    from datetime import datetime, timedelta
    import os,requests
    nfrom = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d') #UTC -1 day to cover all 24hour news
    newsApiKey = os.getenv("NEWSDATAKEY")
    requesturl = 'https://newsdata.io/api/1/news?'+'apikey='+newsApiKey+'&language=en'+"&country=au,nz"
    requesturl +='&from_date='+nfrom
    requesturl +=f'&category={category}'
    requesturl += ('&q='+q) if q is not None else ''

    articles = []
    response = requests.get(requesturl)
    if response.status_code == 200:
        result = response.json()
        counter = 0
        for arr in result['results']:
            try:
                c_src = arr['source_id']
                c_auth = arr['creator'][0] if arr['creator'] is not None else ''
                c_title = arr['title']
                c_url = arr['link']
                c_dsc = arr['description']
                c_cntnt = arr['content']
                content = {'source':c_src, 'author':c_auth, 'title':c_title, 'url':c_url, 'description':c_dsc, 'content':c_cntnt}
                articles.append(content)
                counter+=1
            except TypeError as te:
                print("Error: ",te)
                #print(arr)
            if counter>=articleslimit:
                break
    else:
        print(f"Error: {response.status_code}")
    return articles
#--------------------------------#

#--------------------------------#
def getArticleSummary(content, temperature=0.25):
    import os,openai
    openai.api_key = os.getenv("OPENAPIKEY")
    openai.organization = os.getenv("OPENAPIORG")
    result = """Summarise text below into a short sentense with a two-three emoji at the beginning (assisting describing content, but not replacing the content):
    """ + content[:2048]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": result}], temperature=temperature
    )
    return completion.choices[0].message['content']
#--------------------------------#

#--------------------------------#
def prepareTelegramHTMLmessage(message):
    #we need this instead of html.escape(message) as Telegram doesn't support all special tags, only some
    text = message
    text = text.replace("<","&lt;")
    text = text.replace(">","&gt;")
    text = text.replace("&","&amp;")
    text = text.replace('"',"&quot;")
    return text

def sendTelegramMessage(message, debug = 1):
    import os,requests
    if debug == 0:
        chat_id = "-1001783307848" #CovetorNews
        telegramToken = os.getenv("TELEGRAMBOTKEY")
    else:
        chat_id = "-1001371860541" #TestTelegramChannel
        telegramToken = os.getenv("TELEGRAMBOTTESTKEY")
    if telegramToken is None:
        print("Missing token Key")
        telegramToken = ""

    return requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(telegramToken, "sendMessage"),
        data={'chat_id': chat_id, 'disable_web_page_preview': True, 'parse_mode': 'HTML', 'text': message}
    )
#--------------------------------#