# pip install psycopg
import psycopg2
from psycopg2 import OperationalError
from psycopg2.errors import UniqueViolation
from datetime import datetime
from loguru import logger
import os
from dotenv import load_dotenv
import json
load_dotenv()


def create_connection():
    """
    db_name,db_user,db_password,db_host,db_port ==> these Data which provide by Heroku PostGreSQL
    q_status ==> query Status . Return -> TRUE ,FALSE,OBJECT, DATA
    __Every Function of this class return q_status
    """
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    """
        Creating A Connection with PostGreSQL to Perform Operation form Database.

        Return :
        ==>If Connection is Created Return -> Object
        ==>If Connection is Not Created Return -> False
        """
    logger.info("Creating Connection")
    connection = False
    try:
        connection = psycopg2.connect(host=db_host, database=db_name, user=db_user,
                                      password=db_password)
        print("Connection to PostgreSQL DB successful")
        logger.info("Successfully Creating Connection")
    except Exception as e:
        print(f"The error '{e}' occurred")
        logger.debug("Issue in Creation Connection")
        logger.exception("Issue Is")
    return connection

def get_query(self, query):
    """
    Show all the data from table query

    Parameter : query
    Return :
    ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
    """
    connection = self.create_connection()
    connection.autocommit = True
    # print("Connection Status is :",connection)
    logger.info("Reading Data in a Table")
    q_status = False

    if connection != False:
        result = None
        cursor = connection.cursor()
        try:
            # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
            # Its Give a QUotes Using "ESCAPE SEQUENCE"
            # query = F'select * from \"argus\".\"{argus_id}_unknown\";'
            cursor.execute(query)
            result = cursor.fetchone()
            logger.info("Successfully Reading Data in a Table")
            return result

        except OperationalError as e:
            print(f"The error '{e}' occurred")
            logger.info("Issue in Reading Data in a Table")
            logger.exception("Issue is")
    return q_status


def insert_query( query: str) -> bool:
    """
    Creating a Row In Columns
    if Insertion is Successfull -> return True
    if insertion is UnSuccessfull -> return False

    Parameter : query
    Return :
    ==> q_status = True -> No Error / Or False -> if Error
    """
    connection = create_connection()
    connection.autocommit = True
    q_status = {
        'status': True,
        'error': 'No Error'
    }
    logger.info("Creating Table")
    logger.info(str(query))
    if connection != False:
        # Connection is Created
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            q_status['status'] = True
            print("Query executed successfully")
            logger.info("Successfully Insertion in Table")
            # Query Execute Successfully 
            return q_status
        except Exception as er:
            # Error InQuery
            print(f"The error '{er}' occurred")
            logger.debug("Issue is Inserting")
            logger.exception("Issue is ")
            q_status['status'] = False
            q_status['error'] = er
            # print(q_status)
        return q_status


def get_latest_incident(customer_id):
    try:
        table_name=str(customer_id)+'_cache_table'
        query=F'''Select feature_value from argus.\"{table_name}\" where feature_name='Latest_IncidentID';'''
        return get_query(query)[0]
    except Exception as E:
        print(E)
        return False

def update_latest_incidentID(customer_id,incident_id):
    try:
        table_name=str(customer_id)+'_cache_table'
        query=F'''UPDATE argus.\"{table_name}\" set feature_value=\'{str(incident_id)}\' where feature_name='Latest_IncidentID';'''
        return insert_query(query)
    except Exception as E:
        print(E)
        return False




def insert_table( table_name :str, Key_values:dict) -> dict:
    try:
        columns_names = tuple(Key_values.keys())
        columns_values = tuple(Key_values.values())
        new_columns_names = '('
        for each_name in columns_names:
            new_columns_names += each_name + ','
        new_columns_names = new_columns_names[:-1]+')'
        print(new_columns_names)
        # print(columns_names.replace("'",''))

        query = F'insert into "argus"."{table_name}" {new_columns_names} values {columns_values} ; '
        return insert_query(query)
    except Exception as err:
        print("Error In Insertion Table")
        print(err)






if __name__=="__main__":
    pass
    # get_latest_incident=get_latest_incident('1002')
    # # Get Latest Incident ID

    # if get_latest_incident:
    #     # If Latest Incident ID is not false
    #     # Then Insert into DB
    #     insertion_status=insert_table('1002_incident',{
    #         'incident_id':199,
    #         "priority":1,
    #         'date':'2023_06_20',
    #     })

    # print(insertion_status)