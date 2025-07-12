import dropbox
from dotenv import load_dotenv #Required only for flask
import os
from loguru import logger #logging Module

load_dotenv()
logger.add("logs/dbx_token.log", level="INFO", rotation="100 MB")



def dbx_token():
    """This Function generate DBX token and Return token Object


    Returns:
        obj: dbx_token
    """
    #app_key fetch from .env file
    APP_KEY = os.getenv("KEY") 
    #refresh_token fetch from .env file
    refresh_token = os.getenv("TOKEN")
    # generating token
    with dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=APP_KEY) as dbx:
        dbx.users_get_current_account()
        # logger.info("End Dropbox ")
        return dbx

def dropbox_access_token():
    """This Function generate DBX token and Return token Object


    Returns:
        obj: dbx_token
    """
    APP_KEY = os.getenv("KEY")
    refresh_token = os.getenv("TOKEN")
    with dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=APP_KEY) as dbx:
        dbx.users_get_current_account()
        # logger.info("End Dropbox ")
        return dbx

