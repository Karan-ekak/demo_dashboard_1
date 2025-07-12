# pip install psycopg
import psycopg2 # pip install psycopg
from psycopg2 import OperationalError
from psycopg2.errors import UniqueViolation , UndefinedTable
import psycopg2.extras

from dotenv import load_dotenv # pip install python-dotenv==0.20.0
import os

load_dotenv()

class ArgusDB:
    """
    db_name,db_user,db_password,db_host,db_port ==> these Data which provide by Heroku PostGreSQL
    q_status ==> query Status . Return -> TRUE ,FALSE,OBJECT, DATA
    __Every Function of this class return q_status
    """
    KEY="kknud9kab37cmx0"
    TOKEN="8wo5nJ0Q_5oAAAAAAAAAAYJiI6o5xHY9au4o9qHh1jh5yIOcNF5JePMGMB0f3mIC"
    DB_NAME="d1ncdprnirsou1"
    DB_USER="cpxrnuylqgbmtt"
    DB_PASSWORD="80fe810946b73074aef07c88937d8b657a92019ba920c835687e3199a857e9b4"
    DB_HOST="ec2-44-199-9-102.compute-1.amazonaws.com"
    DB_PORT="5432"
    # db_name = os.getenv("DB_NAME")
    # db_user = os.getenv("DB_USER")
    # db_password = os.getenv("DB_PASSWORD")
    # db_host = os.getenv("DB_HOST")
    # db_port = os.getenv("DB_PORT")
    
    db_name = DB_NAME
    db_user = DB_USER
    db_password = DB_PASSWORD
    db_host = DB_HOST
    db_port = DB_PORT

    def check_env_data(self) -> bool :
        '''Check env Data Exist Or Not 
        
        if Data : Exist No Error
        If Data Not Exist : Error 
        '''
        env_values=(self.db_name,self.db_user,self.db_password,self.db_host,self.db_port)
        env_data_exist= all(var is not None for var in env_values) #Checking Variable Exist of Not
        if not env_data_exist:
            
            # logger.critical("No File Found ENV Data - Creditails Not Found")
            return False
        return True
        # return env_data_exist


    def create_connection(self):
        """
        Creating A Connection with PostGreSQL to Perform Operation form Database.

        Return :
        ==>If Connection is Created Return -> Object
        ==>If Connection is Not Created Return -> False
        """
        # logger.info("Creating Connection")
        connection = False
        try:
            if self.check_env_data() == False:
                return False
            connection = psycopg2.connect(host=self.db_host, database=self.db_name, user=self.db_user,
                                          password=self.db_password)
          
            # logger.info("Successfully Creating Connection")
        except Exception as e:
            print(F'Exception as {e}')
            print(F"Issue in Creation Connection {e}")
            # logger.exception("Issue Is")
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
        # logger.info("Reading Data in a Table")
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
                # logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
            except UndefinedTable as e:
                print(f"Table is Not Exist {e}")
            except Exception as Err:
                print(F"Issue {Err}")
        return q_status
    
    def get_all(self, query):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        
        # logger.info("Reading Data in a Table")
        q_status = False
        # logger.info(str(query))
        if connection != False:
            result = None
            cursor = connection.cursor()
            try:

                cursor.execute(query)
                result = cursor.fetchall()
                # logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")

                # logger.exception("Issue is")
            except UndefinedTable as e:
                print(f"Table is Not Exist '{e}' occurred")
            except Exception as Err:
                print(F"Issue {Err}")
        return q_status

    def get_columns(self, table_name: str, columns: list, where: str = "", getOne=False, extra=''):
        """  
        table_name : (STR)
        columns : (List) 
        Where : (STR)
        getOne : Bool [ True / False ]
                If True Return Only 1 Line , If False Return Multiple Lines
        Return : False or List of Tuple

        """

        query = f'SELECT {", ".join(columns)} FROM {table_name}'
        if where:
            query += f' WHERE {where}'
        if getOne:
            return self.get_query(query)

        return self.get_all(query + extra)
    


if __name__ == '__main__':

    # Want Fetch only 1 Row | Limit is not working
    query=F''' 
    SELECT "WorkOrderId","Title","CreatedAt" FROM argus."WorkOrder"
    ORDER BY "WorkOrderId" DESC LIMIT 10
    '''
    data=ArgusDB().get_query(query=query)
    print(data)



    # Want to fetch Multiple Rows Limit is work here
    query=F''' 
    SELECT "WorkOrderId","Title","CreatedAt" FROM argus."WorkOrder"
    ORDER BY "WorkOrderId" DESC LIMIT 10
    '''
    data=ArgusDB().get_all(query=query)
    print(data)