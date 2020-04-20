from app import app 

from app import main_views 

from app import controller

from envbin import zlogger 

if __name__ == "__main__":
    src = 'run.main'
    zlogger.log(src, 'STARTING')
    
    controller.initBot()     
    zlogger.log(src, f'Bot App Initialized {controller.bot_app}') 

    # TODO: Delay until up is running
    # controller.initStreamz()     
    # zlogger.log(src, 'Additional Streams Initialized')
    # zlogger.log(src, f"KE_DATA: {controller.KE_DATA }")
    # zlogger.log(src, f"GLOBAL_DATA: {controller.GLOBAL_DATA }")
    # zlogger.log(src, f"NEWS_TICKER: {controller.NEWS_TICKER }")

    if app.env == 'production':
        app.run()
    else:
        app.run(debug=True)
    zlogger.log(src, 'Flask App is started')

    zlogger.log(src, 'FINISHED')

