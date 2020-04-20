
import requests , json 

# import sys
# sys.path.append("../../../shared") 
# import zlogger




def getLatestSummaryStats_PA(country='Kenya'):
    KE_DATA = None 
    GLOBAL_DATA = None

    api_url = "https://api.covid19api.com/summary"
    rqst = requests.get(api_url)
    rqst = json.loads( rqst.text )

    GLOBAL_DATA = rqst['Global']

    rqst = rqst['Countries']
    for item in rqst:
        if item['Country'] == country:
            KE_DATA = item

    return KE_DATA, GLOBAL_DATA
    
def getRelatedNews():
    NEWS = []

    api_key = "633d33d95eac415e8334b783cabe3485"
    
    q = "covid19"
    mkt='en-US'
    safeSearch = 'safeSearch'
    news_source = 'medical-news-today' #'google-news' #reuters associated-press bbc-news cnn google-news business-insider bloomberg buzzfeed  etc>>> 
    category = 'health' #&category={category}

    api_url = f"http://newsapi.org/v2/top-headlines?sources={news_source}&apiKey={api_key}"

    rqst = requests.get(api_url)
    rqst = json.loads( rqst.text )
    print(rqst) 
    
    for item in rqst['articles']:
        NEWS.append( item['title'] )

    return NEWS 