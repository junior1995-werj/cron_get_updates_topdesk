from prettyconf import config

class Settings:

    URL_BOT_API = config("URL_BOT_API")
    USER_BOT_API = config("USER_BOT_API")
    PASSWORD_BOT_API= config("PASSWORD_BOT_API")
    URL_TOP_DESK = config("URL_TOP_DESK")
    USER_TOP_DESK = config("USER_TOP_DESK")
    PASSWORD_TOP_DESK = config("PASSWORD_TOP_DESK")
    
settings = Settings()