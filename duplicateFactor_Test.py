from funcLib import duplicateFactor

print("Start")
articleHash = []

article = "✈️🔊 The opening of Western Sydney International Airport in 2026 will require airspace adjustments that could disrupt operations at other Sydney airports and alter noise patterns for residents, despite previous assurances to the contrary. (brisbanetimes (https://www.brisbanetimes.com.au/business/companies/new-airport-will-bring-changes-to-sydney-s-skies-but-no-one-s-sure-what-they-are-20230725-p5dr7p.html?ref=rss&utm_medium=rss&utm_source=rss_business))"
result = duplicateFactor(articleHash, article)
print (result, " - ", article)

article = "#✈️🏙️🔊 The opening of Western Sydney International Airport in 2026 will require changes to the airspace of existing Sydney airports, potentially affecting pilot training, emergency services, and noise patterns for residents. (smh (https://www.smh.com.au/business/companies/new-airport-will-bring-changes-to-sydney-s-skies-but-no-one-s-sure-what-they-are-20230725-p5dr7p.html?ref=rss&utm_medium=rss&utm_source=rss_business))"
result = duplicateFactor(articleHash, article)
print (result, " - ", article)

article = "#🦘✈️ Qantas' reputation is suffering due to customer complaints about poor service, mismanagement, and staff treatment, leading to calls for government intervention. (crikey (https://www.crikey.com.au/2023/08/07/qantas-reputation-passengers-staff/))"
result = duplicateFactor(articleHash, article)
print (result, " - ", article)

article = "#🔥🇦🇺👨‍👦‍👦 A father and his five sons died in a house fire in Queensland, Australia, while the mother escaped unharmed. (thefrontierpost (https://thefrontierpost.com/six-dead-in-tragic-house-fire-in-australias-queensland/))"
result = duplicateFactor(articleHash, article)
print (result, " - ", article)

article = "#🔥🇦🇺👨‍👦‍👦 Six people, including a father and his five sons, died in a house fire in Queensland, Australia. (in_cyprus (https://in-cyprus.philenews.com/news/international/six-dead-in-tragic-house-fire-in-australias-queensland/))"
result = duplicateFactor(articleHash, article)
print (result, " - ", article)

article = "#✈️🏙️🔊 The opening of Western Sydney International Airport in 2026 may disrupt operations at other Sydney airports, affect pilot training and emergency services, and change noise patterns for residents. (brisbanetimes (https://www.brisbanetimes.com.au/business/companies/new-airport-will-bring-changes-to-sydney-s-skies-but-no-one-s-sure-what-they-are-20230725-p5dr7p.html?ref=rss&utm_medium=rss&utm_source=rss_business))"
result = duplicateFactor(articleHash, article)
print (result, " - ", article)
