
from app import app

from datetime import datetime 

from envbin import zlogger

from envbin import apiz

from envbin import zdata_source
from envbin import zbot_logic
from envbin.zbot_logic import ZBotLogicFlow

bot_app = None
IS_TABBED_PANE = False 

######### -------- GLOBAL OBJECTS ----------

GSHEET_RECORD_PATH = ['1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks' , 'user_input!A1:G10000' ] 

## TODO: kill repetition 
TABBED_NAV_MENU = [
    {'label' : 'Map of Cases', 'link' : 'mapcases', 'is_tabbed_pane':IS_TABBED_PANE }, 
    {'label' : 'Chat Bot', 'link' : 'chatbot', 'is_tabbed_pane':IS_TABBED_PANE }, 
    {'label' : 'About', 'link' : 'about', 'is_tabbed_pane':IS_TABBED_PANE }, 
]

APP_ICON_URL = "https://previews.123rf.com/images/goodzone95/goodzone951803/goodzone95180300026/96725720-chatbot-icon-.jpg" #"https://i.pinimg.com/originals/9a/11/33/9a1133d4af3b637e1c6c8ff251785f27.jpg"

BOT_ID = 'bot' 
USER_ID = 'me'

MESSAGEZ =[ ]

NEWS_TICKER = [] #["the quick brown fox jumped over the lazy dogs", "This is a tester  <b>|</b> The dogs ate the homework", "The cats didn't care", "Pop goes the whistle", "435943 75,043"]

KE_DATA, GLOBAL_DATA = [], []
NEWS_DATA , NEWS_TICKER = [], []


#### ----- TODO: UTILZ ------ 
@app.template_filter('formatNumber')
def formatNumber(znumber):
    # print( f"formatNumber.>>> '{znumber}' ")
    # znumber = znumber.strip() if isinstance(znumber, str) else znumber 
    return "{:,.0f}".format( znumber )  if znumber else znumber #if len(znumber) > 0 else znumber 

@app.template_filter('formatDate')
def formatDate(zdate, src_format='%Y-%m-%d', target_format="%d %b %Y"):
    # print( f'zdate.BEFORE >>>>>>>> {zdate}' )
    if zdate:
        zdate1 = datetime.strptime( zdate.split('T')[0], src_format)
        zdate2 = zdate.split('T')[1][:-4]
        # print( f'zdate.AFTER >>>>>>>> {zdate2}' )
        return f"{datetime.strftime(zdate1, target_format ) } at {zdate2}"
    else:
        return zdate 

@app.template_filter('formatDateOnly')
def formatDateOnly(zdate, src_format='%Y-%m-%d', target_format="%d %b %Y"):
    # print( f'zdate.BEFORE >>>>>>>> {zdate}' )
    if zdate:
        zdate1 = datetime.strptime( zdate.split('T')[0], src_format)
        # print( f'zdate.AFTER >>>>>>>> {zdate2}' )
        return f"{datetime.strftime(zdate1, target_format ) } "
    else:
        return zdate 



######### -------- APP  ----------



######## ------     HELPERS ----- 
def getTimeStamp():
    return f"{datetime.now()}"

def getTempPage( cbody=None ):
    return f"<H1> { cbody.capitalize() if cbody else 'Nothing provided' } </H1>"

def getBotResponse(user_input):        
    response, rcode, pred_cat = bot_app.getResponse( user_input ) 
    return "I don't understand. Try that again" if response is None else response, pred_cat

def addChatMsg(src, msg, user_agent=None, from_addr=None, bot_ans=None):
    MESSAGEZ.append( { 'src': src, 'msg': msg} ) 
    ## save user input
    if src == USER_ID:
        zdata_source.writeTo( 
                [ getTimeStamp(), msg, bot_ans, 
                    from_addr, user_agent.platform, 
                    user_agent.browser, user_agent.language], 
                GSHEET_RECORD_PATH, zdata_source.zGSHEET, zdata_source.MODE_APPEND
            ) 

def upackDataForNewsTicker( datz ):
    res = []
    if datz:
        for k, v in datz.items():
            try: ##by brute!!
                res.append( "{} : {:,.0f}".format( k, int(v) ) ) 
            except:            
                res.append( f"{k} {v}" ) 

    return ", ".join(res) 



def initBot():
    global bot_app
    model_fpath = 'ncov19_tfidf_faq'

    faq_path = [('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'FAQ responses!A1:G1000'), 
                ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'Classify_Phrases!A1:G1000')]
    faq_typ = zdata_source.zGSHEET_FAQ

    bot_app = ZBotLogicFlow()
    bot_app.loadFaqDbz( faq_path, faq_typ ) 
    bot_app.loadModel( zbot_logic.MODEL_COSINE_TFIDF, model_fpath ) 


def initStreamz():    
    global KE_DATA, GLOBAL_DATA, NEWS_DATA, NEWS_TICKER 
    
    KE_DATA, GLOBAL_DATA =    apiz.getLatestSummaryStats_PA()
    NEWS_DATA , NEWS_TICKER = apiz.getRelatedNews() 

    force_numz = [ upackDataForNewsTicker(KE_DATA), 
            upackDataForNewsTicker(GLOBAL_DATA), ]

    NEWS_TICKER = [ *NEWS_TICKER ]
    
    zlogger.log('controller.initStreamz', f"NEWS={NEWS_TICKER}")



if __name__ == "__main__":
    src = 'ncov.main'

    zlogger.log(src, "STARTING")
    
    initBot()

    initStreamz() 

    zlogger.log(src, "FINISHED")