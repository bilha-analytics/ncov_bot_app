from flask import render_template, request

from app import app 

from app import controller

from envbin import zlogger


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home( title="Botify"): 
    zlogger.log('main_views.home', f"NEWS_TICKER = {controller.NEWS_TICKER}")     
    if len( controller.NEWS_TICKER) == 0:
        controller.initStreamz()
        zlogger.log('main_views.home.restartStreamz', f"NEWS_TICKER = {controller.NEWS_TICKER}")     

    if request.method == 'POST':
        msg_in = request.form.get('askBot') 
        controller.MESSAGEZ.append( controller.genChatMsg( controller.USER_ID, msg_in ) ) 
        controller.MESSAGEZ.append( controller.genChatMsg(controller.BOT_ID, controller.getBotResponse(msg_in ) ) ) 

    ARGZ = {
        'title' : title,
        "nav_menu" : controller.NAV_MENU,
        'BOT_ID' : controller.BOT_ID,
        'USER_ID' : controller.USER_ID,
        
        'scrollToAnchor' : 'bottomz',

        'msgs' : controller.MESSAGEZ, 
        'NEWS_TICKER' : controller.NEWS_TICKER, 
    }
    return render_template('main_page.html', **ARGZ)  


@app.route('/about')
def about():
    return render_template('widget_about.html')


@app.route('/casesmap')
def map_cases():
    return controller.getTempPage('Map Cases')
