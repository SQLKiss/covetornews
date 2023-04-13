import os
theToken = os.getenv("TELEGRAMBOTKEY")


print(theToken)


exit(0)

text = "Testing news reporter bot"

import requests

token = theToken
chat_id = "-1001371860541" #"OnewheelNZ"
chat_id = "-1001783307848" #CovetorNews
url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
results = requests.get(url_req)
print(results.json())
