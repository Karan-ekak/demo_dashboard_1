from database_connection  import ArgusDB
from loguru import logger
from ist_time_zone import get_IST_today_date_time

logger.add("logs/acitivtyLogger.log", level="INFO", rotation="100 MB")

def upload_actitivity(user_id,activity_page,activity_action,date=None):
    table_name='1005_activity'
    table_data={
        'user_id':int(user_id),
        'activity_page':activity_page,
        'activity_action':activity_action,
        'date':str(get_IST_today_date_time())
    }
    logger.info(f'User Id : {user_id}, Activity Page : {activity_page} , Activity Action : {activity_action}')
    ArgusDB().insert_db(table_name,table_data)
   
    

if __name__ == "__main__":
    pass
    new_user_name,new_user_email,new_user_role='22','22',00
    activity_data='Successfully Creating Users Data : '+ new_user_name,new_user_email,new_user_role
    upload_actitivity(00,"Admin Creating Users Page",activity_data)
                