import os, requests, json

message = 'Test message again'

#telegramToken = os.getenv("TELEGRAMBOTKEY")
#chat_id = "-1001783307848" #CovetorNews

telegramToken = os.getenv("TELEGRAMBOTKEYTEST")
chat_id = "-1001371860541" #TestTelegramChannel

requesturl = "https://api.telegram.org/bot" + telegramToken + "/sendMessage" + "?chat_id=" + chat_id + "&parse_mode=HTML" + "&text=" + message 
response = requests.get(requesturl)
if response.status_code == 200:
    print("Sent to Telegram channel")
else:
    print(response)



exit(0)

theToken = os.getenv("TELEGRAMBOTKEY")
chat_id = "-1001783307848" #CovetorNews
poll_id = 0

#first get poll_id
api_url = "https://api.telegram.org/bot" + theToken + "/"
response = requests.post(api_url + "getUpdates", data={"chat_id": chat_id, "limit": 5})
result = response.json()
updates = sorted(result["result"], key=lambda x: x["channel_post"]["date"], reverse=True) #sort by date descending
for pst in updates:
    if pst['channel_post']['poll']:
        poll_id = pst['channel_post']['poll']['id']
        pollOptions = pst['channel_post']['poll']['options']
        break

print(poll_id)
print(pollOptions)

exit(0)

if poll_id!=0:
    response = requests.post(api_url + "getPoll", data={"chat_id": chat_id,"msg_id": poll_id})
    result = response.json()
    print(result)


#data = json.loads(response.text)
#print(data)





exit(0)

#post a message
text = "Testing news reporter bot"
token = theToken
chat_id = "-1001371860541" #"OnewheelNZ"
chat_id = "-1001783307848" #CovetorNews
url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
results = requests.get(url_req)
print(results.json())
