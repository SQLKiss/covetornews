from funcLib import getNewsArticles,getArticleSummary,sendTelegramMessage

posts = {"Queensland": 2, "New Zealand": 2, "Aviation":1, "Boobs":1, "IT News": 4, "Science": 3}

#"Brisbane","Auckland","Economy","Crypto","Industry","Business","Shopping","Lifestyle","Boobs","Aviation","Aircraft","Travel","Technology"

result = ""
for topic,numberOfArticles in posts.items():
    print(f"Topic: {topic} ({numberOfArticles})")
    news = getNewsArticles(topic,numberOfArticles)

    #Integrated ADs
    #if topic == "New Zealand":
    #    sponsortext = {'source': "Kiwieducation",'author':"Denis", 'title':"", 'url':"https://Kiwieducation.co.nz"
    #                ,'description':"A New Zealand company Kiwieducation.co.nz which brings a lot of students into the country announced a new discount program for studens from Ukraine"}
    #    news.append(sponsortext)

    if len(news)>0:
        result += "\n<b>" + topic + ":</b>\n"
        for article in news:
            if len(article['description'])>0:
                result += getArticleSummary(article['description'])
                result +=' <i>(<a href="'+article['url']+'">'+article['source']+'</a>)</i>\n'
    print("Articles generated")

if len(result)>0:
    response = sendTelegramMessage(result,0) #0=prod, 1=debug
    if response.status_code == 200:
        print("Sent to Telegram")
    else:
        print(response.json())
