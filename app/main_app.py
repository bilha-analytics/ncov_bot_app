import sys
sys.path.append("../envbin") 
import zlogger

from flask import Flask, render_template, request

import apiz
from datetime import datetime 

import zdata_source
import zbot_logic
from zbot_logic import ZBotLogicFlow

app = Flask(__name__) 
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
    { 'src':'me'}
]

NEWS_TICKER = [] #["the quick brown fox jumped over the lazy dogs", "This is a tester  <b>|</b> The dogs ate the homework", "The cats didn't care", "Pop goes the whistle", "435943 75,043"]


## TODO: static/style.css
THEME_COLOR_BG="#422057"
THEME_COLOR_FONT="FCF951"
THEME_COLOR_HIGHLIGHT = "#CBCE91"


#### ----- TODO: UTILZ ------ 
@app.template_filter('formatNumber')
def formatNumber(znumber):
    return "{:,.0f}".format( znumber )    

@app.template_filter('formatDate')
def formatDate(zdate, src_format='%Y/%m/%d', target_format="%d %b, %Y"):
    zdate = datetime.strptime( zdate.split(' ')[0], src_format)
    return datetime.strftime(zdate, target_format ) 


######### -------- APP  ----------

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home( title="Botify"):
    if request.method == 'POST':
        msg_in = request.form.get('askBot') 
        MESSAGEZ.append( genChatMsg( USER_ID, msg_in ) ) 
        MESSAGEZ.append( genChatMsg(BOT_ID, getBotResponse(msg_in ) ) ) 

    ARGZ = {
        'title' : title,
        "nav_menu" : NAV_MENU,
        'BOT_ID' : BOT_ID,
        'USER_ID' : USER_ID,
        
        'THEME_COLOR_BG' : THEME_COLOR_BG,
        'THEME_COLOR_FONT' : THEME_COLOR_FONT,
        'THEME_COLOR_HIGHLIGHT' : THEME_COLOR_HIGHLIGHT, 
        
        'scrollToAnchor' : 'bottomz',

        'msgs' : MESSAGEZ, 
        'NEWS_TICKER' : NEWS_TICKER, 
    }
    return render_template('test.html', **ARGZ)  


@app.route('/about')
def about():
    return getTempPage('About')


@app.route('/casesmap')
def map_cases():
    return getTempPage('Map Cases')



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






if __name__ == "__main__":
    src = 'ncov.main'
    zlogger.log(src, "STARTING")
    
    KE_DATA, GLOBAL_DATA =    apiz.getLatestSummaryStats_PA()
    
    NEWS_TICKER = [ upackDataForNewsTicker(KE_DATA), 
                    upackDataForNewsTicker(GLOBAL_DATA), 
                    *apiz.getRelatedNews() ]

    app.run(debug=True)

    zlogger.log(src, "FINISHED")