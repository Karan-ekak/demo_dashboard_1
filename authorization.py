"""Authorization : After Authentication , According to Email ,
    Its Return 
    1.Customer_id ,
    2.Roles ,
    3.Sites
"""
from database_connection import ArgusDB
from Kanplas_database_connection import get_query

def main_function(authenticate, user_customer_id, input_email) :
    """Authorization : After Authentication , According to Email ,
    if No Error Then Tuple Return -> Email , Customer_id , Site , Role

    Args:
        authenticate (Bool): TRUE or False
        user_customer_id (int): 4 Digit for (New Series) , 3 Digit for (Old Series)
        input_email (str): When user input Email

    Returns:
        Case 1 . if No Error Authentcation Done , Role Found , Then Tuple Return -> Email , Customer_id , Site , Role
        Case 2 . If Authencation False or None , Return to Login Page
        Case 3 . If Authentcation True but No Authorizaton 
    """
    if authenticate == False or authenticate == None:
        return False
    else:

        # db_data = ArgusDB().get_allSite_roles(user_customer_id)
        # db_user_data=ArgusDB().get_one_dict_query(columns_name=('user_id','email','user_name','group','mid','mobile'),table_name='1002_users')
        try:
            table_name=str(user_customer_id) + "_users"
            query=F'SELECT user_id,user_name,role,groups,mid,mobile FROM argus.\"{table_name}\" where email=\'{input_email}\' and status=true; '
            db_data=ArgusDB().get_query(query)
            
            print("database date ",db_data)
            if db_data == False or db_data == None:
                return "No Group"

            user_data={
                'user_id' : db_data[0],
                'user_name' : db_data[1],
                'roles' : db_data[2],
                'group' : db_data[3],
                'mid' : db_data[4],
                'mobile' : db_data[5]
            }
            
            return user_data

        except Exception as E:
            print(f"Error In Authoziation {E}")
            return 'No Group'

if __name__ == "__main__":
    auth = main_function(True, '1002', 'abhishek1@ekak.com')
    print(auth)
