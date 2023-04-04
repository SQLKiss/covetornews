from newsapi import NewsApiClient

#exit(0)


# Init
newsapi = NewsApiClient(api_key='eda4bf5358654cafbee74d38c6c001f8')

sources = newsapi.get_sources(country='nz')
print(sources)
exit(0)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(country='nz', sources='stuff') #q='tesla', 

print(top_headlines)

#news-com-au, abc-news-au

exit(0)

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

print(all_articles)

# /v2/top-headlines/sources
sources = newsapi.get_sources()

print(sources)

