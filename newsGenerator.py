from funcLib import getNewsArticles,getArticleSummary,sendTelegramMessage
posts = []
#posts.append(["IT News"])
#posts.append(["Auckland"])
#posts.append(["Queensland","Brisbane","New Zealand","Auckland"])
#posts.append(["Economy","Crypto","Industry","Business"])
#posts.append(["Shopping","Lifestyle","Boobs"])
#posts.append(["Aviation","Aircraft","Travel"])
#posts.append(["Technology","IT News","Science"])

#choose only one combo for tomorrow
posts.append(["Queensland","New Zealand","Australia"])
posts.append(["IT News","Crypto","Science"])
posts.append(["Economy","Business","Aviation"])
posts.append(["Travel","Lifestyle","Shopping"])

for topics in posts:
    print(topics)
    result = ""
    numberOfArticles = int(8/len(topics))
    if numberOfArticles<1:
        numberOfArticles = 1
    print(f"numberOfArticles: {numberOfArticles}")
    for topic in topics:
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

    if len(result)>0:
        response = sendTelegramMessage(result,1) #0=prod, 1=debug
        if response.status_code == 200:
            print("Sent to Telegram")
        else:
            print(response.json())

