News processor  
Filter out unnecessary content and get short but informative news on the Telegram channel  
  
# therdl  
SQLKiss Covetor News App project  
More info and documentation: https://www.sqlkiss.com/covetor-news-app/introduction  
  
Quick start:  
-Set environment variables for: NEWSDATAKEY, OPENAPIKEY, OPENAPIORG, TELEGRAMBOTKEY, PRODCHATID  
-Create a python script  
-Add this code:    
```  
from funcLib import generateAndPostNewsToTelegram  
topics = {"Brisbane":5, "Auckland":5}  
generateAndPostNewsToTelegram(topics=topics,debug=0)  
```  
-Run   