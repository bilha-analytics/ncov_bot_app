from flask import render_template, request

from app import app 

from app import controller
from app.controller import * 

from envbin import zlogger

def forceServiceStart():
    if len( controller.NEWS_TICKER) == 0:
        controller.initStreamz()
        zlogger.log('main_views.home.restartStreamz', f"NEWS_TICKER = {controller.NEWS_TICKER}")     
    
    if controller.bot_app is None:
        controller.initBot()        
        controller.addChatMsg( controller.BOT_ID, 'Hi there. Ask me about Corona virus')

    

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot( title="Botify"): 
    zlogger.log('main_views.home', f"NEWS_TICKER = {controller.NEWS_TICKER}")     
    
    forceServiceStart()

    if request.method == 'POST':
        msg_in = request.form.get('askBot') 
        bot_msg, pred_cat = controller.getBotResponse(msg_in ) 
        
        controller.addChatMsg( controller.USER_ID, msg_in,
                                request.user_agent, request.remote_addr , 
                                pred_cat
                                ) 
        controller.addChatMsg(controller.BOT_ID, bot_msg ) 

    ARGZ = {
        'title' : title,
        'IS_TABBED_PANE' : controller.IS_TABBED_PANE, 
        "nav_menu" : controller.TABBED_NAV_MENU , 
        "APP_ICON_URL" : controller.APP_ICON_URL,

        'BOT_ID' : controller.BOT_ID,
        'USER_ID' : controller.USER_ID,        
        'scrollToAnchor' : 'bottomz',
        'msgs' : controller.MESSAGEZ,

        'NEWS_TICKER' : controller.NEWS_TICKER, 
        'ke_data' : controller.KE_DATA,
        'glb_data' : controller.GLOBAL_DATA,
    }

    layout = 'layouts/layout_app.html'
    page =  'one_pager.html'      
    return render_template( 'page_creator.html', layout=layout, page=page , **ARGZ)  


@app.route('/about')
def about(title='About'):   
    forceServiceStart()

    ARGZ = {
        'title' : title,    
        'IS_TABBED_PANE' : controller.IS_TABBED_PANE,  
        "nav_menu" : controller.TABBED_NAV_MENU , 
        "APP_ICON_URL" : controller.APP_ICON_URL, 
        'NEWS_TICKER' : controller.NEWS_TICKER, 
        'ke_data' : controller.KE_DATA,
        'glb_data' : controller.GLOBAL_DATA,
    }
    layout = 'layouts/layout_app.html'
    page =  'widget_about.html'     
    return render_template( 'page_creator.html', layout=layout, page=page , **ARGZ)  



@app.route('/')
@app.route('/home')
@app.route('/mapcases')
def mapcases(title='Covid Bot'):
    forceServiceStart()
    
    ARGZ = {
        'title' : title,
        'IS_TABBED_PANE' : controller.IS_TABBED_PANE, 
        "nav_menu" : controller.TABBED_NAV_MENU ,
        "APP_ICON_URL" : controller.APP_ICON_URL,  
        'NEWS_TICKER' : controller.NEWS_TICKER, 
        'ke_data' : controller.KE_DATA,
        'glb_data' : controller.GLOBAL_DATA,
    }

    zlogger.log('route.mapcases', f"KE_DATA = {repr(controller.KE_DATA)}")
    zlogger.log('route.mapcases', f"GLOBAL_DATA = {repr(controller.GLOBAL_DATA)}")
    
    layout = 'layouts/layout_app.html'
    page =  'widget_jhu_map.html'
    return render_template( 'page_creator.html', layout=layout, page=page , **ARGZ)  

@app.route('/news')
@app.route('/news/<newsid>')
def news(title='Medical News', newsid=None):
    ARGZ = {
        'title' : title,
        'IS_TABBED_PANE' : controller.IS_TABBED_PANE, 
        "nav_menu" : controller.TABBED_NAV_MENU ,
        "APP_ICON_URL" : controller.APP_ICON_URL,  
        'NEWS_TICKER' : controller.NEWS_TICKER, 
        'NEWS_ITEMS' : controller.NEWS_DATA, 
    } 
    
    layout = 'layouts/layout_app.html'
    page =  'widget_news.html'
    return render_template( 'page_creator.html', layout=layout, page=page , **ARGZ)  