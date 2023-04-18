#to-do:
#add headlines
#collect news first, then process, then post (easier to debug)
#use Google Trends to generate list of topics

from funcLib import generateAndPostNewsToTelegram

#"Brisbane","Auckland","Economy","Crypto","Industry","Business","Shopping","Lifestyle","Boobs","Aviation","Aircraft","Travel","Technology"

topics = {"Brisbane":5, "Auckland":5}
generateAndPostNewsToTelegram(topics=topics,debug=1) #0 means post to prod

