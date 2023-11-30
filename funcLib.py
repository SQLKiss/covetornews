#--------------------------------#
def getNewsArticles(topic, articleslimit = 2, sortBy = "publishedAt"):
    from datetime import datetime, timedelta
    import os,requests
    nfrom = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d') #UTC -1 day to cover all 24hour news
    newsApiKey = os.getenv("NEWSAPIKEY")
    if newsApiKey is None:
        raise ValueError('NEWSAPIKEY is missing')
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
    #category = "food,health" #business,entertainment,environment,food,health,politics,science,sports,technology,top,tourism,world
    from datetime import datetime, timedelta
    import os,requests
    newsApiKey = os.getenv("NEWSDATAKEY")
    if newsApiKey is None:
        raise ValueError('NEWSDATAKEY is missing')
    requesturl = 'https://newsdata.io/api/1/news?'+'apikey='+newsApiKey+'&language=en' #+"&country=au,nz"
    #requesturl +='&timeframe=24'#hours #disabled as it is only available on paid plans
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
                #ignore 'openpr' for now (to-do: better way of filtering sources)
                if c_src == 'openpr':
                    continue
                c_auth = arr['creator'][0] if arr['creator'] is not None else ''
                c_title = arr['title']
                c_url = arr['link']
                c_dsc = arr['description']
                c_cntnt = arr['content'] if arr['content'] is not None else arr['description']
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
        code = response.json()
        if code is None:
            print("")
        else:
            print(f"Message: {code['results']['message']}")
    return articles
#--------------------------------#

#--------------------------------#
def getArticleSummary(content, temperature=0.25):
    import os,openai
    openApiKey = os.getenv("OPENAPIKEY")
    openApiOrg = os.getenv("OPENAPIORG")
    if openApiKey is None:
        raise ValueError('OPENAPIKEY is missing')
    if openApiOrg is None:
        raise ValueError('OPENAPIORG is missing')
    
    openai.api_key = openApiKey
    openai.organization = openApiOrg
    result = """Summarize (key point only) the text below (answer should be as short as possible, a one-liner starts with a two-three emojis about the text, short answer is better):
    """ + content
    completion = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": result}], temperature=temperature
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
        chat_id = os.getenv("PRODCHATID")
        telegramToken = os.getenv("TELEGRAMBOTKEY")
    else:
        chat_id = os.getenv("TESTCHATID")
        telegramToken = os.getenv("TELEGRAMBOTTESTKEY")
    if telegramToken is None:
        raise ValueError('Telegram token key is Missing')
    if chat_id is None:
        raise ValueError('chat_id key is missing')

    return requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(telegramToken, "sendMessage"),
        data={'chat_id': chat_id, 'disable_web_page_preview': True, 'parse_mode': 'HTML', 'text': message}
    )
#--------------------------------#

#--------------------------------#
def generateAndPostNewsToTelegram(topics,debug=1):
    categories = 'business,science,technology,tourism,world'
    result = ""
    articleHash = []
    for topic,numberOfArticles in topics.items():
        print(f"Topic: {topic} ({numberOfArticles})")
        news = getNewsIOArticles(topic,numberOfArticles,categories)
        if len(news)>0:
            #result += "<b>" + topic + ":</b>\n"
            for article in news:
                try:
                    title = article['title']
                    description = article['description'] if article['description'] is not None else ''
                    content = article['content'] if article['content'] is not None else description
                    url = article['url'] if article['url'] is not None else ''
                    source = article['source'] if article['source'] is not None else ''
                    message = "Description: " + description + "\nContent: " + content
                    sourceURL = ' (<a href="'+url+'">'+prepareTelegramHTMLmessage(source)+'</a>)\n\n'
                    if len(description)>0:
                        articleSummary = getArticleSummary(message)
                        articleSummary = prepareTelegramHTMLmessage(articleSummary)
                        if (duplicateFactor(articleHash, articleSummary) > 0.7):
                            continue
                        if (len(result) + len(articleSummary) + len(sourceURL)) <= 4096: #Telegram message limit
                            result += articleSummary + sourceURL
                        else:
                            print("Message is too long, no more articles added")
                            break
                except:
                    print(title)
                    print(description)
                    print(url)
                    print(source)
        print("Articles generated")

    if len(result)>0:
        response = sendTelegramMessage(result,debug) #0=prod, 1=debug
        if response.status_code == 200:
            print("Sent to Telegram")
        else:
            print(result)
            print(response.json())
#--------------------------------#

#--------------------------------#
def duplicateFactor(articleHash, article):
    import string
    duplicateFactor = 0
 
    #remove punctuation from article
    article = article.translate(str.maketrans('', '', string.punctuation))    
    #split article using space as separator
    articleWords = article.split()
    #remove all words with less than 3 characters
    articleWords = [word for word in articleWords if len(word)>2]
    #remove all words with more than 15 characters
    articleWords = [word for word in articleWords if len(word)<16]

    #calculate the hash of every word in articleWords and put it into tempHash array
    tempHash = []
    for word in articleWords:
        tempHash.append(hash(word))

    tempHash.sort()

    if len(articleHash) > 0:
    #for every element in articleHash take the alement to array existingArticleHash
        articleDuplicateFactor = 0
        for existingArticleHash in articleHash:
            for hashValue in tempHash:
                if hashValue in existingArticleHash:
                    articleDuplicateFactor += 1

        percent = articleDuplicateFactor / len(tempHash)
        if percent > duplicateFactor:
            duplicateFactor = percent
        
    articleHash.append(tempHash)
    
    return duplicateFactor
#--------------------------------#