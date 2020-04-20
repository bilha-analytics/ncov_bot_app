
from app import app

from datetime import datetime 

from envbin import zlogger

from envbin import apiz

from envbin import zdata_source
from envbin import zbot_logic
from envbin.zbot_logic import ZBotLogicFlow

bot_app = None

######### -------- GLOBAL OBJECTS ----------

NAV_MENU = [
    {'label' : 'home', 'link' : 'home'}, 
    {'label' : 'Map of Cases', 'link' : 'map_cases'}, 
    {'label' : 'About', 'link' : 'about'}, 
]

BOT_ID = 'bot' 
USER_ID = 'me'

MESSAGEZ =[ 
]

NEWS_TICKER = [] #["the quick brown fox jumped over the lazy dogs", "This is a tester  <b>|</b> The dogs ate the homework", "The cats didn't care", "Pop goes the whistle", "435943 75,043"]


#### ----- TODO: UTILZ ------ 
@app.template_filter('formatNumber')
def formatNumber(znumber):
    return "{:,.0f}".format( znumber )    

@app.template_filter('formatDate')
def formatDate(zdate, src_format='%Y/%m/%d', target_format="%d %b, %Y"):
    zdate = datetime.strptime( zdate.split(' ')[0], src_format)
    return datetime.strftime(zdate, target_format ) 


######### -------- APP  ----------



######## ------     HELPERS ----- 

def getTempPage( cbody=None ):
    return f"<H1> { cbody.capitalize() if cbody else 'Nothing provided' } </H1>"

def getBotResponse(user_input):
    response, rcode = bot_app.getResponse( user_input ) 
    return "I don't understand. Try that again" if response is None else response

def genChatMsg(src, msg):
    return { 'src': src, 'msg': msg}

def upackDataForNewsTicker( datz ):
    res = []
    for k, v in datz.items():
        res.append( f"{k} {v}" )

    return ", ".join(res) 



def initBot():
    global bot_app
    model_fpath = 'ncov19_tfidf_faq'

    faq_path = [ ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'FAQ responses!A1:G1000'), ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'Classify_Phrases!A1:G1000')]
    faq_typ = zdata_source.zGSHEET_FAQ

    bot_app = ZBotLogicFlow()
    bot_app.loadFaqDbz( faq_path, faq_typ ) 
    bot_app.loadModel( zbot_logic.MODEL_COSINE_TFIDF, model_fpath ) 


def initStreamz():    
    global KE_DATA, GLOBAL_DATA, NEWS_TICKER 
    
    KE_DATA, GLOBAL_DATA =    apiz.getLatestSummaryStats_PA()
    
    NEWS_TICKER = [ upackDataForNewsTicker(KE_DATA), 
                    upackDataForNewsTicker(GLOBAL_DATA), 
                    *apiz.getRelatedNews() ]
    zlogger.log('controller.initStreamz', f"NEWS={NEWS_TICKER}")



if __name__ == "__main__":
    src = 'ncov.main'

    zlogger.log(src, "STARTING")
    
    initBot()

    initStreamz() 

    zlogger.log(src, "FINISHED")