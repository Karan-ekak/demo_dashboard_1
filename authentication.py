""" Authentication 
    Step 1 : Check Email if Not Exist Back to Login Page
    
    if Email Exist The Go Step 2:
    Step 2 : Get password according to Email from DB

    Step 3 : User Input Password's Create Hash 

    Step 4 : Compare with DB's Store Password
             Return TRUE / False 

"""

from database_connection import ArgusDB
from loguru import logger
import hashlib

from Kanplas_database_connection import check_user_email_get_ps_customer_id_user_id
logger.add("logs/system.log", level="INFO", rotation="100 MB")


def check_email_exist(input_email):
    # db_ps -> Database password
    try:
        logger.info(f"_Checking Input Email Exist or Not email is {input_email}")
        db_ps = ArgusDB().check_user_email_get_ps_customer_id_user_id(input_email)
        print(db_ps,"printing the db password")
        if db_ps == None or db_ps == False:
            logger.info(f"_Invalid Email :  {input_email}")
            return False,False,False
        logger.info(f"_Email is Valid : {input_email}")
        return db_ps[0], db_ps[1],db_ps[2]
    except Exception as E:
        logger.exception(f"Error Occurs In check_email_exist {E}")
        return False,False,False


def create_password_hash(user_entered_password: str) -> str:
    """Create Hash Password

    Args:
        user_entered_password (str): Using Input Password

    Returns:
        hashing Str : Str
    """

    # Create Salth
    try:
        logger.info(f"_Creating Password Hash")
        salt = "45597E68B599"

        # Adding Salt Inside the Password
        logger.info(f"_Mixing Salt in Password")
        db_password = user_entered_password + salt

        h = hashlib.md5(db_password.encode())
        # print(type(h.hexdigest()))
        logger.info("_Return Hash Password")
        return h.hexdigest()
    except Exception as E:
        logger.exception('Error Occurs create_hash_password ')

        return False


def main_function(input_email: str, input_ps: str):
    """ Authentication 
    Step 1 : Check Email if Not Exist Back to Login Page
    
    if Email Exist The Go Step 2:
    Step 2 : Get password according to Email from DB

    Step 3 : User Input Password's Create Hash 

    Step 4 : Compare with DB's Store Password
             Return TRUE , customer_id / False , False
    """
    try:
        # Step 1 Check Email
        db_ps, customer_id,user_id = check_email_exist(input_email)
        print("printing and extracting data",db_ps, customer_id,user_id)
        # print(customer_id)
        # Step 2 Get Database_password db_ps
        if db_ps == False:
            return False, False,False
        else:
            # Step 3
            hash_input_ps = create_password_hash(input_ps)

            # Step 4
            if hash_input_ps == db_ps:
                return True, customer_id,user_id
            else:
                return False, False,False
    except Exception as E:
        print(f"Error Occurs In Main Function {E}")
        print("testing purpose")
        return False, False,False


if __name__ == "__main__":
    pass
    authenticate,user_customer_id,flag = main_function('sudhanshusharma@kanplas.com', 'Kanplas@123')
    print(f'Authencate : {authenticate}')
    get_password = create_password_hash('Kanplas@123')
    print(get_password)
