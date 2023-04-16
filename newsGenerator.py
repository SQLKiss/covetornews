from funcLib import getNewsArticles,getArticleSummary,sendTelegramMessage

#"Brisbane","Auckland","Economy","Crypto","Industry","Business","Shopping","Lifestyle","Boobs","Aviation","Aircraft","Travel","Technology"

#posts = {"Queensland": 2, "New Zealand": 2, "Aviation":1, "Boobs":1, "IT News": 4, "Science": 3}
posts = {"Queensland": 2, "New Zealand": 2, "Aviation":2, "Technology": 3, "Science": 3}

#to-do:
#add headlines
#save results first, then post (easier to debug)

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
                articleSummary = getArticleSummary(article['description'])
                sourceURL = ' (<a href="'+article['url']+'"><i>'+article['source']+'</i></a>)\n'
                if (len(result) + len(articleSummary) + len(sourceURL)) <= 4096: #Telegram message limit
                    result += articleSummary + sourceURL
                else:
                    print("Message is too long")
                    break
    print("Articles generated")

if len(result)>0:
    response = sendTelegramMessage(result,0) #0=prod, 1=debug
    if response.status_code == 200:
        print("Sent to Telegram")
    else:
        print(result)
        print(response.json())
        
