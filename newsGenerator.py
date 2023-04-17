from funcLib import getNewsIOArticles,getArticleSummary,sendTelegramMessage,prepareTelegramHTMLmessage

#"Brisbane","Auckland","Economy","Crypto","Industry","Business","Shopping","Lifestyle","Boobs","Aviation","Aircraft","Travel","Technology"

#posts = {"Queensland": 2, "New Zealand": 2, "Aviation":1, "Boobs":1, "IT News": 4, "Science": 3}
#posts = {"Queensland": 2, "New Zealand": 2, "Aviation":2, "Technology": 3, "Science": 3}

posts = {"Economy":2, "Business":2, "Aviation":1, "Technology": 2, "Science": 2}

#to-do:
#add headlines
#collect news first, then process, then post (easier to debug)
#use Google Trends to generate list of topics

result = ""
for topic,numberOfArticles in posts.items():
    print(f"Topic: {topic} ({numberOfArticles})")
    news = getNewsIOArticles(topic,numberOfArticles)

    #Integrated ADs
    #if topic == "New Zealand":
    #    sponsortext = {'source': "Kiwieducation",'author':"Denis", 'title':"", 'url':"https://Kiwieducation.co.nz"
    #                ,'description':"A New Zealand company Kiwieducation.co.nz which brings a lot of students into the country announced a new discount program for studens from Ukraine"}
    #    news.append(sponsortext)

    if len(news)>0:
        result += "\n<b>" + topic + ":</b>\n"
        for article in news:
            try:
                title = article['title']
                description = article['description'] if article['description'] is not None else ''
                content = article['content'] if article['content'] is not None else description
                url = article['url'] if article['url'] is not None else ''
                source = article['source'] if article['source'] is not None else ''
                message = "Description: " + description + "\nContent: " + content
                sourceURL = ' (<a href="'+url+'">'+prepareTelegramHTMLmessage(source)+'</a>)\n'
                if len(description)>0:
                    articleSummary = getArticleSummary(message)
                    articleSummary = prepareTelegramHTMLmessage(articleSummary)
                    if (len(result) + len(articleSummary) + len(sourceURL)) <= 4096: #Telegram message limit
                        result += articleSummary + sourceURL
                    else:
                        print("Message is too long")
                        break
            except:
                print(title)
                print(description)
                print(url)
                print(source)
    print("Articles generated")

if len(result)>0:
    response = sendTelegramMessage(result,0) #0=prod, 1=debug
    if response.status_code == 200:
        print("Sent to Telegram")
    else:
        print(result)
        print(response.json())
