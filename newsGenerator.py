#to-do:
#add headlines
#collect news first, then save, then process saved, then post (easier to debug and less API calls)
#use Google Trends to generate list of topics

from funcLib import generateAndPostNewsToTelegram

#"Brisbane","Auckland","Economy","Crypto","Industry","Business","Shopping","Lifestyle","Boobs","Aviation","Aircraft","Travel","Technology"

topics = {"Brisbane":5, "New Zealand":3, "Cloud":1, "Aviation":1}
generateAndPostNewsToTelegram(topics=topics,debug=0) #0 means post to prod

