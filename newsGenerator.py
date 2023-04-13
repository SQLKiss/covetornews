from funcLib import getNewsArticles,getArticleSummary,sendTelegramMessage

topics = ["Queensland","Aviation","New Zealand"] #"Auto","Games","Economy","Crypto", "Australia"

result = ""
for topic in topics:
    news = getNewsArticles(topic)
    result += "\n<b>" + topic + ":</b>\n"
    for article in news:
        result += getArticleSummary(article['description'])
        result +=' <i>(<a href="'+article['url']+'">'+article['source']+'</a>)</i>\n'

response = sendTelegramMessage(result)
print(response)
