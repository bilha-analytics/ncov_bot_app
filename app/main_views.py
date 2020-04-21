from flask import render_template, request

from app import app 

from app import controller
from app.controller import * 

from envbin import zlogger


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot( title="Botify"): 
    zlogger.log('main_views.home', f"NEWS_TICKER = {controller.NEWS_TICKER}")     
    if len( controller.NEWS_TICKER) == 0:
        controller.initStreamz()
        zlogger.log('main_views.home.restartStreamz', f"NEWS_TICKER = {controller.NEWS_TICKER}")     

    if request.method == 'POST':
        msg_in = request.form.get('askBot') 
        controller.addChatMsg( controller.USER_ID, msg_in ) 
        controller.addChatMsg(controller.BOT_ID, controller.getBotResponse(msg_in ) ) 

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
    ARGZ = {
        'title' : title,     
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
def mapcases(title='Covid19 Map'):
    ARGZ = {
        'title' : title,
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

@app.route('/news/<newsid>')
def news(newsid=None):
    pass 