from app import app 

from app import main_views 

from app import controller

from envbin import zlogger 

import threading, atexit

def initService():    
    controller.initBot()     
    controller.addChatMsg( controller.BOT_ID, 'Hi there. Ask me about Corona virus')
    zlogger.log(src, f'Bot App Initialized {controller.bot_app}') 
   
    controller.initStreamz()     
    zlogger.log(src, 'Additional Streams Initialized')


if __name__ == "__main__":
    src = 'run.main'
    zlogger.log(src, 'STARTING')
        
    service_thread = threading.Thread( target=initService )
    service_thread.start() 

    if app.env == 'production':
        app.run()
    else:
        app.run(debug=True)
    zlogger.log(src, 'Flask App is started')

    zlogger.log(src, f"service_thread.isAlive = {service_thread.isAlive() }")

    zlogger.log(src, 'FINISHED')

