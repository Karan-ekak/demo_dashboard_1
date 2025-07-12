# pip install psycopg
import psycopg2
from psycopg2 import OperationalError
from psycopg2.errors import UniqueViolation,SyntaxError
import psycopg2.extras
from datetime import datetime
from loguru import logger
import os
from dotenv import load_dotenv
import json

load_dotenv()

"""
Defining A Loggine
"""
logger.add("logs/Database_Argus.log", level="INFO", rotation="100 MB")
basedir = os.path.abspath(os.path.dirname(__file__))


class ArgusDB:
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


    def check_env_data(self) -> bool :
        '''Check env Data Exist Or Not 
        
        if Data : Exist No Error
        If Data Not Exist : Error 
        '''
        env_values=(self.db_name,self.db_user,self.db_password,self.db_host,self.db_port)
        env_data_exist= all(var is not None for var in env_values) #Checking Variable Exist of Not
        if not env_data_exist:
            print("ENV Data is Not Found")
            logger.critical("ENV Data - Creditails Not Found")
        return False
        # return env_data_exist
    def create_connection(self):
        """
        Creating A Connection with PostGreSQL to Perform Operation form Database.

        Return :
        ==>If Connection is Created Return -> Object
        ==>If Connection is Not Created Return -> False
        """
        logger.info("Creating Connection")
        connection = False
        try:
            connection = psycopg2.connect(host=self.db_host, database=self.db_name, user=self.db_user,
                                          password=self.db_password)
            # print("Connection to PostgreSQL DB successful")
            logger.info("Successfully Creating Connection")
        except Exception as e:
            print(f"The error '{e}' occurred")
            logger.debug("Issue in Creation Connection")
            logger.exception("Issue Is")
        return connection

    def create_database(self, query):
        """
        Creating New Database


        If DB is created -> Print ("Query Executed successfully )
        If DB is not created -> Print (Error and Return False)

        Parameter : query
        Return :
        ==> q_status = True -> its means New DB is created / Or False -> New Database is not created
        """
        connection = self.create_connection()
        connection.autocommit = True
        cursor = connection.cursor()
        q_status = False  # Query_status
        logger.info("Creating A Database")
        logger.info(str(query))
        if connection != False:
            try:
                cursor.execute(query)
                print("Query executed successfully")
                q_status = True
                logger.info("Successfully Database is Created")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue in Creating Database")
                logger.exception("Issue is")
        return q_status

    def create_table(self, query):
        """
        Creating a Table
        if Table is created -> Print ("Query Executed successfully )
        if Table is not created -> Print (Error and Return False)

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        q_status = False  # Query_status
        logger.info("Creating Table")
        logger.info(str(query))
        if connection != False:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                q_status = True
                print("Query executed successfully")
                logger.info("Successfully Created Table")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue in Creating Table")
                logger.exception("Issue is ")
        return q_status

    def insert_query(self, query: str) -> bool:
        """
        Creating a Row In Columns
        if Insertion is Successfull -> return True
        if insertion is UnSuccessfull -> return False

        Parameter : query
        Return :
        ==> q_status = True -> No Error / Or False -> if Error
        """
        connection = self.create_connection()

        q_status = False  # Query_status
        logger.info("Creating Table")
        logger.info(str(query))
        connection.autocommit=True
        if connection != False:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                q_status = True
                print("Query executed successfully")
                logger.info("Successfully Insertion in Table")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue is Inserting")
                logger.exception("Issue is ")
        return q_status

    def multiple_query(self, all_query: list) -> bool:
        """
        Executing Multiple Query At a time 

        Parameter : all_query : List Of All Query
        if All Query Then Commit If AnyOne Query Its ROll Back and Return False
        Return :
        ==> q_status = True -> No Error / Or False -> if Error
        """
        connection = self.create_connection()

        # disable autocommit mode
        connection.autocommit = False
        q_status = False  # Query_status

        if connection != False:
            try:
                cursor = connection.cursor()

                for each_query in all_query:
                    cursor.execute(each_query)
                    logger.info(f"Query : {each_query}")
                connection.commit()

                q_status = True
                print("Query executed successfully")
                logger.info("Successfully Insertion in Table")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug(f"Issue is E {e}")
                logger.exception("Issue is ")

                return False
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error in transaction, reverting all changes using rollback ", error)
                logger.debug(f"Issue is E {e}")
                connection.rollback()
                logger.debug("Roll Back Executing")
                return False

        return q_status

    def insert_query_with_parameter(self, query: str, parameter) -> bool:
        """
        Creating a Row In Columns
        if Insertion is Successfull -> return 
        True
        if insertion is UnSuccessfull -> return False

        Parameter : query
        Return :
        ==> q_status = True -> No Error / Or False -> if Error
        """
        connection = self.create_connection()
        connection.autocommit = True
        q_status = False  # Query_status
        logger.info("Creating Table")
        logger.info(str(query))
        if connection != False:
            try:
                cursor = connection.cursor()
                cursor.execute(query, parameter)
                q_status = True
                print("Query executed successfully")
                logger.info("Successfully Insertion in Table")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue is Inserting")
                logger.exception("Issue is ")
        return q_status

    def excute_query(self, query: str) -> bool:
        """
        Creating a Row In Columns
        if Insertion is Successfull -> return True
        if insertion is UnSuccessfull -> return False

        Parameter : query
        Return :
        ==> q_status = True -> No Error / Or False -> if Error
        """
        connection = self.create_connection()
        connection.autocommit = True
        q_status = False  # Query_status
        logger.info("Creating Table")
        logger.info(str(query))
        if connection != False:
            try:
                email=''
                role=''
                customer_id=''
                cursor = connection.cursor()
                cursor.execute(cursor.execute("""
                UPDATE argus.customer_table
                SET roles = jsonb_set(roles, '{%s}', '{"role": "%s"}')
                WHERE customer_id = %s;
                """ % (email, role, customer_id)))
                q_status = True
                print("Query executed successfully")
                logger.info("Successfully Execute Query")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue is Inserting")
                logger.exception("Issue is ")
        return q_status

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

    def update_query_where(self, table_name: str, columns, where_condition: str):
        """Updates a PostgreSQL table based on the given columns and where condition.

            Paramter be Like  : update_query_where ("str ", dict or list of Dict, str -> "id = 1"  )
            Args:
                table_name: The name of the PostgreSQL table to update.
                columns: A dictionary of column names and new values.
                where_condition: A SQL WHERE clause to filter the rows to update.

            Returns:
                Bool (True / False)
        """

        sql = """
            UPDATE {}
            SET {}
            WHERE {};
        """.format(table_name,
                   ", ".join(["{} = %s".format(col) for col in columns]),
                   where_condition)
        # print(sql, tuple(columns.values()))
        return self.insert_query_with_parameter(sql, tuple(columns.values()))

    def get_query_dict(self, query):
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
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                # query = F'select * from \"argus\".\"{argus_id}_unknown\";'
                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_all(self, query):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False
        logger.info(str(query))
        if connection != False:
            result = None
            cursor = connection.cursor()
            try:

                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
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

    def count_teamMember(self, argus_id):
        """
        Count all the Team Member

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        table_name = '\"argus\".\"' + argus_id + '_team\"'
        query = f'SELECT COUNT(*) FROM {table_name}'

        return self.get_query(query)[0]

    def today_Known_Unknown(self, today_date, argus_id):
        """Show  Today Total Known and Unknown(known,Unknown)

        Args:
            today_date (STR): _description_

        Returns:
            _type_: tuples with 2 Values (Known , Unknown)
        """

        query = f'''
        SELECT
        COUNT(DISTINCT CASE WHEN name LIKE 'unknown%' THEN name END) AS Unknown_present_today,
        COUNT(DISTINCT CASE WHEN name NOT LIKE 'unknown%' THEN name END) AS Known_present_today
        FROM argus."{argus_id}_attendance_entries"
        WHERE date = '{today_date}';
        '''
        # print(query)

        data_known_Unknown = self.get_query(query)
        if type(data_known_Unknown) == bool:
            return (0, 0)
        return data_known_Unknown

    def get_face_encoding(self, argus_id, new_member):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True ->
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'Select \"numpy_encoding\" from \"argus\".\"onboarded_unkownface_search_queue_{argus_id}\" where emp_name=\'{new_member}\'  ;'

                # query = F'select \"unknown_id\" from \"argus\".\"{argus_id}_unknown\";'

                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")
                result = [i[0] for i in result]
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def insert_row(self, query):
        """
        Insert rows into database's table
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Insert Rows in Table")
        logger.info(str(query))
        q_status = False
        if connection != False:
            try:
                cursor = connection.cursor()
                connection.autocommit = True
                # insert data into db
                # query='''insert into "dave-alpha-build"."dave_device" (dave_id,driver_name,driver_score,travel_time) values ('dave_101','James','100','300');'''
                cursor.execute(query)
                # save into db
                logger.info("Successfully Insert a row in a Table")
                q_status = True
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_all_unknown(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
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
                query = F'select * from \"argus\".\"{argus_id}_attendance_entries\" where \"name\" like \'unknow%\' ;'

                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_unknown_name(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select \"unknown_id\" from \"argus\".\"{argus_id}_unknown\";'

                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")
                result = [i[0] for i in result]
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_all_team(self, argus_id):
        """
        Show all the Team Member data from table query

        Parameter : query
        Return :
        ==> q_status = [(),()]  List of Team Member Data
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_team\";'

                cursor.execute(query)
                result = cursor.fetchall()

                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_only_name_team(self, argus_id):
        """
        Show all the Team Member data from table query

        Parameter : query
        Return :
        ==> q_status = [(),()]  List of Team Member Data
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select emp_name from \"argus\".\"{argus_id}_team\" ;'

                cursor.execute(query)
                result = cursor.fetchall()

                logger.info("Successfully Reading Data in a Table")
                result = [i[0] for i in result]
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_all_un_processed(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"onboarded_unkownface_search_queue_{argus_id}\" where processed=\'false\' ;'
                # select * in onboarded_unkownface_search_queue_argus_id
                # where
                # processed = 0
                cursor.execute(query)
                result = cursor.fetchall()
                # result = [i for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_all_onboard_unprocessed(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"onboarded_unkownface_search_queue_{argus_id}\" where processed=\'false\' ;'
                # select * in onboarded_unkownface_search_queue_argus_id
                # where
                # processed = 0
                cursor.execute(query)
                result = cursor.fetchall()
                # result = [i for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_all_team_unprocessed(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_team\" where processed=\'false\' ;'
                # select * in onboarded_unkownface_search_queue_argus_id
                # where
                # processed = 0
                cursor.execute(query)
                result = cursor.fetchall()
                # result = [i for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_all_unknown_unprocessed(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_unknown\" where processed=\'false\' ;'
                # select * in onboarded_unkownface_search_queue_argus_id
                # where
                # processed = 0
                cursor.execute(query)
                result = cursor.fetchall()
                # result = [i for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def update_new_team_member_unknown_face(self, argus_id, new_member, count_face, found_face):
        """
        Update Unknown Faces into New Team Memeber

        Parameter : query
        Return : True

        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                connection.autocommit = True
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'Update \"argus\".\"onboarded_unkownface_search_queue_{argus_id}\" set processed=true,found=\'{found_face}\',count_processed=\'{count_face}\' where emp_name=\'{new_member}\'  ;'
                # select * in onboarded_unkownface_search_queue_argus_id
                # where
                # processed = 0

                cursor.execute(query)
                result = True
                # result = [i for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def update_only_face_encoding(self, argus_id, new_member, only_face_encoding):
        """
        Update Unknown Faces into New Team Memeber

        Parameter : query
        Return : True

        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                connection.autocommit = True
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'Update \"argus\".\"onboarded_unkownface_search_queue_{argus_id}\" set numpy_encoding=%s where emp_name=\'{new_member}\'  ;'
                # select * in onboarded_unkownface_search_queue_argus_id
                # where
                # processed = 0

                cursor.execute(query, (only_face_encoding,))
                result = True
                # result = [i for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def update_team_face_encoding(self, argus_id: str, emp_name: str, face_encoding: str):
        """
        Update Faces into Team Table

        Parameter : Argus_id,emp_name,face_encoding
        Return : True

        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                connection.autocommit = True
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'Update \"argus\".\"{argus_id}_team\" set numpy_encoding=%s where emp_name=\'{emp_name}\'  ;'
                # select * in onboarded_unkownface_search_queue_argus_id
                # where
                # processed = 0

                cursor.execute(query, (face_encoding,))
                result = True
                # result = [i for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def update_team_data(self, argus_id, emp_name, emp_doj, emp_entry_time, emp_exit_time, emp_working_hour):
        """
        Update Faces into Team Table

        Parameter : Argus_id,emp_name,face_encoding
        Return : True

        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                connection.autocommit = True
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'Update \"argus\".\"{argus_id}_team\" set emp_name=%s, join_date=%s,entry_time=%s,exit_time=%s,working_hour=%s where emp_name=\'{emp_name}\'  ;'
                # select * in onboarded_unkownface_search_queue_argus_id
                # where
                # processed = 0

                cursor.execute(
                    query, (emp_name, emp_doj, emp_entry_time, emp_exit_time, emp_working_hour,))
                result = True
                # result = [i for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    # def update_team_data2(self, argus_id, new_emp_name, edit_email_alert, threshold_value, mondayEntryEdit,mondayExitEdit, tuesdayEntryEdit, tuesdayExitEdit, wednesdayEntryEdit, wednesdayExitEdit,thursdayEntryEdit,thursdayExitEdit, fridayEntryEdit, fridayExitEdit, saturdayEntryEdit, saturdayExitEdit,sundayEntryEdit, sundayExitEdit):
    #     """
    #     Update Faces into Team Table
    #
    #     Parameter : Argus_id,emp_name,face_encoding
    #     Return : True
    #
    #     """
    #     connection = self.create_connection()
    #     # print("Connection Status is :",connection)
    #     logger.info("Reading Data in a Table")
    #     q_status = False
    #
    #     if connection != False:
    #         result = None
    #         cursor = connection.cursor()
    #         try:
    #             connection.autocommit = True
    #             # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
    #             # Its Give a QUotes Using "ESCAPE SEQUENCE"
    #
    #             # query = F'Update \"argus\".\"{argus_id}_team\" set emp_name=%s, join_date=%s,entry_time=%s,exit_time=%s,working_hour=%s where emp_name=\'{emp_name}\'  ;'
    #
    #             query = F'Update \"argus\".\"{argus_id}_team\" set alert_switch=%s , monday_entry_time=%s, monday_exit_time=%s, tuesday_entry_time=%s, tuesday_exit_time=%s, wednesday_entry_time=%s, wednesday_exit_time=%s, thursday_entry_time=%s, thursday_exit_time=%s, friday_entry_time=%s, friday_exit_time=%s,  saturday_entry_time=%s, saturday_exit_time=%s,  sunday_entry_time=%s, sunday_exit_time=%s where emp_name=\'{new_emp_name}\'  ;'
    #
    #             # select * in onboarded_unkownface_search_queue_argus_id
    #             # where
    #             # processed = 0
    #             if edit_email_alert == 'true':
    #                 edit_email_alert = True
    #             else:
    #                 edit_email_alert = False
    #
    #
    #             cursor.execute(query, (edit_email_alert, mondayEntryEdit, mondayExitEdit,tuesdayEntryEdit, tuesdayExitEdit, wednesdayEntryEdit, wednesdayExitEdit,thursdayEntryEdit,thursdayExitEdit, fridayEntryEdit, fridayExitEdit, saturdayEntryEdit,saturdayExitEdit,sundayEntryEdit, sundayExitEdit,))
    #             result = True
    #             # result = [i for i in result]
    #             logger.info("Successfully Reading Data in a Table")
    #             return result
    #
    #         except OperationalError as e:
    #             print(f"The error '{e}' occurred")
    #             logger.info("Issue in Reading Data in a Table")
    #             logger.exception("Issue is")
    #     return q_status

    def update_team_data2(self, argus_id, new_emp_name, edit_email_alert, threshold_value, mondayEntryEdit,
                          mondayExitEdit, tuesdayEntryEdit, tuesdayExitEdit, wednesdayEntryEdit, wednesdayExitEdit,
                          thursdayEntryEdit, thursdayExitEdit, fridayEntryEdit, fridayExitEdit, saturdayEntryEdit,
                          saturdayExitEdit, sundayEntryEdit, sundayExitEdit):
        """
        Update the team data for an employee in the specified Argus ID's team table.

        Parameters:
            - argus_id: The ID of the Argus instance.
            - new_emp_name: The new name of the employee.
            - edit_email_alert: A boolean indicating whether email alerts should be edited.
            - threshold_value: The threshold value.
            - mondayEntryEdit: The new Monday entry time.
            - mondayExitEdit: The new Monday exit time.
            - tuesdayEntryEdit: The new Tuesday entry time.
            - tuesdayExitEdit: The new Tuesday exit time.
            - wednesdayEntryEdit: The new Wednesday entry time.
            - wednesdayExitEdit: The new Wednesday exit time.
            - thursdayEntryEdit: The new Thursday entry time.
            - thursdayExitEdit: The new Thursday exit time.
            - fridayEntryEdit: The new Friday entry time.
            - fridayExitEdit: The new Friday exit time.
            - saturdayEntryEdit: The new Saturday entry time.
            - saturdayExitEdit: The new Saturday exit time.
            - sundayEntryEdit: The new Sunday entry time.
            - sundayExitEdit: The new Sunday exit time.

        Returns:
            - True if the team data was successfully updated, False otherwise.
        """

        # Create a database connection.
        connection = self.create_connection()

        # Log the connection status.
        logger.info("Reading data in a table")

        # Set the query status to False by default.
        q_status = False

        # If a connection was established, proceed with the update.
        if connection != False:
            result = None
            cursor = connection.cursor()

            try:
                # Set autocommit to True to avoid issues with transactions.
                connection.autocommit = True

                # Update the team table with the new data.
                query = f'UPDATE "argus"."{argus_id}_team" SET alert_switch=%s, entry_time_threshold=%s , monday_entry_time=%s, monday_exit_time=%s, tuesday_entry_time=%s, tuesday_exit_time=%s, wednesday_entry_time=%s, wednesday_exit_time=%s, thursday_entry_time=%s, thursday_exit_time=%s, friday_entry_time=%s, friday_exit_time=%s, saturday_entry_time=%s, saturday_exit_time=%s, sunday_entry_time=%s, sunday_exit_time=%s WHERE emp_name=\'{new_emp_name}\'  ;'

                # Convert the edit_email_alert value to a boolean.
                # print(edit_email_alert)
                # if edit_email_alert == 'true' or edit_email_alert is True or edit_email_alert == 'True':
                #     edit_email_alert = True
                # else:
                #     edit_email_alert = False

                edit_email_alert = edit_email_alert in ['true', 'True']

                # Execute the query with the specified values.
                cursor.execute(query, (
                edit_email_alert, threshold_value, mondayEntryEdit, mondayExitEdit, tuesdayEntryEdit, tuesdayExitEdit,
                wednesdayEntryEdit, wednesdayExitEdit,
                thursdayEntryEdit, thursdayExitEdit, fridayEntryEdit, fridayExitEdit, saturdayEntryEdit,
                saturdayExitEdit, sundayEntryEdit, sundayExitEdit,))
                result = True
                logger.info("Successfully updated the team data")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                return False

    def update_uknown_face_encoding(self, argus_id: str, unknown_id: str, face_encoding: str):
        """
        Update Faces into Team Table

        Parameter : Argus_id,emp_name,face_encoding
        Return : True

        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                connection.autocommit = True
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'Update \"argus\".\"{argus_id}_unknown\" set numpy_encoding=%s , processed=true where unknown_id=\'{unknown_id}\'   ;'
                # select * in onboarded_unkownface_search_queue_argus_id
                # where
                # processed = 0

                cursor.execute(query, (face_encoding,))
                result = True
                # result = [i for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def update_row(self, query):
        """
        Update Row
        """
        connection = self.create_connection()
        print("Connection is Created")
        logger.info("Updating a Row in Table")
        logger.info(str(query))
        q_status = False
        if connection != False:
            try:
                cursor = connection.cursor()
                connection.autocommit = True
                cursor.execute(query)
                q_status = True
                logger.info("Successfully Update a Row in a Table")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue in Updating a Row")
                logger.exception("Issue is")
        return q_status

    def read_driver_score(self, dave_id):
        """
        In 1st Table
        Reading Driver Score
        """
        connection = self.create_connection()
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            try:
                cursor = connection.cursor()
                query = '''Select driver_score,travel_time from "dave-alpha-build"."dave_device" where "dave_id"=%s;'''
                cursor.execute(query, (dave_id,))
                # dave_id , <-  its is a way of writing Query
                logger.info(str(query))
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")
                return result

            except Exception as e:
                print(e)
                return q_status
        return q_status

    def update_driver_score(self, dave_id, driver_score, travel_time):
        """
        Update Row in Driver Score
        """
        connection = self.create_connection()
        print("Connection is Created")
        logger.info("Updating a Row in Table")

        q_status = False
        if connection != False:
            try:
                cursor = connection.cursor()
                connection.autocommit = True
                # update_query='''UPDATE  "dave-alpha-build".dave_device SET dave_id = Dave_101 WHERE dave_id = dave_101 ;'''
                query = '''UPDATE "dave-alpha-build"."dave_device" SET "driver_score"=%s, "travel_time"=%s Where "dave_id"=%s;'''

                cursor.execute(query, (driver_score, travel_time, dave_id,))
                q_status = True
                logger.info("Successfully Update a Row in a Table")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue in Updating a Row")
                logger.exception("Issue is")
        return q_status

    # OPeration For Table 2 for Driver score
    """
    2nd Table Columns (dave_id (varchar),dbx_videos(varchar),is_analyzed(varchar))

    """

    def update_analyzed_video(self, dave_id, video):
        """
        Update Row in Driver Score
        """
        connection = self.create_connection()
        print("Connection is Created")
        logger.info("Updating a Video in Table")

        q_status = False
        if connection != False:
            try:
                cursor = connection.cursor()
                connection.autocommit = True
                # update_query='''UPDATE  "dave-alpha-build".dave_device SET dave_id = Dave_101 WHERE dave_id = dave_101 ;'''
                query = '''UPDATE "dave-alpha-build"."for_driver_score" SET "is_analyzed"=1  WHERE "dbx_videos"=%s and "dave_id"=%s;'''

                cursor.execute(query, (video, dave_id,))
                q_status = True
                logger.info("Successfully Update a Row in a Table")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue in Updating a Row")
                logger.exception("Issue is")
        return q_status

    def read_for_driver_score(self):
        """

        In 2nd Table
        Reading for_driver_score table
        Return : If No Issue -> Rows (tuple) OR Return : False

        """
        q_status = False
        try:

            return ArgusDB().get_all('''select * from "dave-alpha-build"."for_driver_score";''')
        except Exception as e:
            print(f"The error '{e}' occurred")
            return q_status

    def insert_new_video(self, dave_id, list_videos_name):
        """

        In 2nd Table
        insert_new_videos
        Return : If No Issue -> True or False

        """
        logger.info("Insert new_Video in for_driver_score in a Table")
        connection = self.create_connection()
        q_status = False
        if connection != False:

            try:
                cursor = connection.cursor()
                connection.autocommit = True
                # print(dave_id,list_videos_name)
                # print(list_videos_name)
                for i in list_videos_name:

                    try:
                        logger.info("_Inserting Video_name {}", i)
                        print(dave_id, i)
                        query = '''insert into "dave-alpha-build"."for_driver_score" (dave_id,dbx_videos,is_analyzed) values (%s,%s,%s);'''
                        cursor.execute(query, (dave_id, i, '0',))

                        q_status = True

                        print(i)
                    except Exception as issue_in_video:
                        logger.debug("_Issue & Skip this in Video {}", i)
                        logger.debug("_Issue is {}", issue_in_video)
                        # Skip this VIdeo Move Forward

                        print(issue_in_video)
                        continue

                # return ArgusDB().get_all('''select * from "dave-alpha-build"."for_driver_score";''')
                # pass
            except Exception as e:
                print(f"The error '{e}' occurred")
                return q_status
        return q_status

    def get_all_videos(self, dave_id):
        """
        Fetching Video from Table 1 for_driver_score

        parameter: <- dave_id

        return: -> all Video list of tuple
        """
        connection = self.create_connection()
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            try:
                print(dave_id)
                cursor = connection.cursor()
                query = '''Select dbx_videos from "dave-alpha-build"."for_driver_score" where "dave_id"=%s;'''
                cursor.execute(query, (dave_id,))
                logger.info(str(query))
                result = cursor.fetchall()
                result = [i[0] for i in result]
                logger.info("Successfully Reading Data in a Table")
                return result
            except Exception as e:
                logger.debug("Issue in Reading Data in a Table {}", e)
                print(e)
                return q_status
        return q_status

    def get_new_videos(self, dave_id):
        """
        Fetching Video from Table 1 for_driver_score

        parameter: <- dave_id

        return: -> all Video list of tuple
        """
        connection = self.create_connection()
        logger.info("Reading New Video in a Table")
        q_status = False

        if connection != False:
            result = None
            try:
                print(dave_id)
                cursor = connection.cursor()
                query = '''Select dbx_videos from "dave-alpha-build"."for_driver_score" where "dave_id"=%s and "is_analyzed"='0' ;'''
                cursor.execute(query, (dave_id,))
                logger.info(str(query))
                result = cursor.fetchall()
                result = [i[0] for i in result]
                logger.info("Successfully New Video Data in a Table")
                return result
            except Exception as e:
                logger.debug("Issue in New Video Data in a Table {}", e)
                print(e)
                return q_status
        return q_status

    def add_new_unknown_img(self, argus_id, unknown_ID, Url, date_time):
        """
        Add a New Team Member

        param: argus_id,emp_name,emp_date,emp_dep,img_link,
        Return : If No Issue -> True or False


        """
        logger.info("Insert new_Video in for_driver_score in a Table")
        connection = self.create_connection()
        q_status = False
        if connection != False:
            cursor = connection.cursor()
            connection.autocommit = True

            table_name = argus_id + '_unknown'
            # print(table_name)
            # print(dave_id,list_videos_name)
            # print(list_videos_name)
            # query=F'INSERT INTO "argus".\"{argus_id}_team\" VALUES (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'
            # query=F'Insert Into \"argus\".\"{argus_id}_team\"  (name,join_date,department,photos) values (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'

            try:
                query = '''insert into "argus"."{}" (argus_id,unknown_id,url,date_time) values (%s,%s,%s,%s);'''.format(
                    table_name)
                print(query)
                cursor.execute(query, (argus_id, unknown_ID, Url, date_time,))
                q_status = True
            except Exception as issue_in_video:
                logger.debug("_Issue & Skip this in Video")
                logger.debug("_Issue is {}", issue_in_video)
                # Skip this VIdeo Move Forward

            # return ArgusDB().get_all('''select * from "dave-alpha-build"."for_driver_score";''')
            # pass
        return q_status

    def add_team_memeber(self, argus_id, emp_name, emp_date, emp_dep, img_link):
        """
        Add a New Team Member

        param: argus_id,emp_name,emp_date,emp_dep,img_link,
        Return : If No Issue -> True or False


        """
        logger.info("Insert new_Video in for_driver_score in a Table")
        connection = self.create_connection()
        q_status = False
        if connection != False:
            cursor = connection.cursor()
            connection.autocommit = True
            table_name = argus_id + '_team'
            # print(dave_id,list_videos_name)
            # print(list_videos_name)
            # query=F'INSERT INTO "argus".\"{argus_id}_team\" VALUES (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'
            # query=F'Insert Into \"argus\".\"{argus_id}_team\"  (name,join_date,department,photos) values (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'

            try:
                query = '''insert into "argus"."{}" (emp_name,join_date,department,photos) values (%s,%s,%s,%s);'''.format(
                    table_name)
                cursor.execute(query, (emp_name, emp_dep, emp_date, img_link,))
                q_status = True
            except Exception as issue_in_video:
                logger.debug("_Issue & Skip this in Video")
                logger.debug("_Issue is {}", issue_in_video)
                # Skip this VIdeo Move Forward

            # return ArgusDB().get_all('''select * from "dave-alpha-build"."for_driver_score";''')
            # pass
        return q_status

    def add_notification(self, argus_id, activity_name, activity_detail, activity_status):
        """
        Add a New Team Member

        param: argus_id,emp_name,emp_date,emp_dep,img_link,
        Return : If No Issue -> True or False


        """
        logger.info("Insert new_Video in for_driver_score in a Table")
        connection = self.create_connection()

        activity_start_time = datetime.now().strftime("%Y_%m_%d__%H_%M")

        q_status = False
        if connection != False:
            cursor = connection.cursor()
            connection.autocommit = True
            table_name = argus_id + '_notification'
            # print(dave_id,list_videos_name)
            # print(list_videos_name)
            # query=F'INSERT INTO "argus".\"{argus_id}_team\" VALUES (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'
            # query=F'Insert Into \"argus\".\"{argus_id}_team\"  (name,join_date,department,photos) values (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'

            try:
                query = '''insert into "argus"."{}" (activity_name,activity_detail,activity_status,
                activity_start_time) values (%s,%s,%s,%s);'''.format(
                    table_name)
                cursor.execute(query, (activity_name, activity_detail,
                                       activity_status, activity_start_time,))
                q_status = True
            except Exception as issue_in_video:
                logger.debug("_Issue & Skip this in Video")
                logger.debug("_Issue is {}", issue_in_video)
                # Skip this VIdeo Move Forward

            # return ArgusDB().get_all('''select * from "dave-alpha-build"."for_driver_score";''')
            # pass
        return q_status

    def add_attendence(self, argus_id, photo_name, photo_url, name, date, time):
        """
        Add a New Attendance Entry In DB

        param: argus_id,emp_name,emp_date,emp_dep,img_link,
        Return : If No Issue -> True or False


        """
        logger.info("Insert new_Video in for_driver_score in a Table")
        connection = self.create_connection()
        q_status = False
        if connection != False:
            cursor = connection.cursor()
            connection.autocommit = True
            table_name = argus_id + '_attendance_entries'
            # print(dave_id,list_videos_name)
            # print(list_videos_name)
            # query=F'INSERT INTO "argus".\"{argus_id}_team\" VALUES (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'
            # query=F'Insert Into \"argus\".\"{argus_id}_team\"  (name,join_date,department,photos) values (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'

            try:
                query = '''insert into "argus"."{}" (photo_name,photo_url,name,date,time) values (%s,%s,%s,%s,%s);'''.format(
                    table_name)
                cursor.execute(
                    query, (photo_name, photo_url, name, date, time,))
                q_status = True
            except UniqueViolation as e:
                logger.info("Duplicate Exist")
                print("Dublicate Exist")
                q_status = True
            except Exception as issue_in_video:
                logger.debug("_Issue & Skip this in Video")
                logger.debug("_Issue is {}", issue_in_video)
                # Skip this VIdeo Move Forward

            # return ArgusDB().get_all('''select * from "dave-alpha-build"."for_driver_score";''')
            # pass
        return q_status

    def get_all_attendance_entries(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_attendance_entries\";'

                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")

                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_only_known_attendance_entries(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_attendance_entries\" where \"name\" not like \'unknow%\' ;'

                cursor.execute(query)
                result = cursor.fetchall()

                logger.info("Successfully Reading Data in a Table")
                list_result = []
                # for i in result:
                #     print(i)
                result = list(map(list, result))
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_year_attendance_entries(self, argus_id, yyyy):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_attendance_entries\" where \"name\" not like \'unknow%\' and \"date\" like \'{yyyy}%\';'

                cursor.execute(query)
                result = cursor.fetchall()

                logger.info("Successfully Reading Data in a Table")
                list_result = []
                # for i in result:
                #     print(i)
                result = list(map(list, result))
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_week_attendance_entries(self, argus_id, latest_sunday_date, today_date):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_attendance_entries\" where  \"name\" not like \'unknow%\' and \"date\" between \'{latest_sunday_date}\' and \'{today_date}%\' Order By \"date\" desc;'

                cursor.execute(query)
                result = cursor.fetchall()

                logger.info("Successfully Reading Data in a Table")
                list_result = []
                # for i in result:
                #     print(i)
                result = list(map(list, result))
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_range_report(self, argus_id, old_date, new_data):
        return self.get_week_attendance_entries(argus_id, old_date, new_data)

    def get_month_attendance_entries(self, argus_id, yyyy, mm):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"

                query = F'select * from \"argus\".\"{argus_id}_attendance_entries\" where \"name\" not like \'unknow%\' and  \"date\" like \'{yyyy}/{mm}%\' order by date asc , time asc;'

                cursor.execute(query)
                result = cursor.fetchall()

                logger.info("Successfully Reading Data in a Table")
                list_result = []
                # for i in result:
                #     print(i)
                result = list(map(list, result))
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_dbx_attendance_csv(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_dbx_attendance_csv\";'

                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")
                result = [i[0] for i in result]
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def add_dbx_attendance_csv(self, argus_id, csv_file_name):
        """
        Add a New Attendance Entry In DBX Attendance CSV

        param:
        Return : If No Issue -> True or False


        """
        logger.info("Insert new_Video in for_driver_score in a Table")
        connection = self.create_connection()
        q_status = False
        if connection != False:
            cursor = connection.cursor()
            connection.autocommit = True
            table_name = argus_id + '_dbx_attendance_csv'
            # print(dave_id,list_videos_name)
            # print(list_videos_name)
            # query=F'INSERT INTO "argus".\"{argus_id}_team\" VALUES (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'
            # query=F'Insert Into \"argus\".\"{argus_id}_team\"  (name,join_date,department,photos) values (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'

            try:
                query = '''insert into "argus"."{}" (csv_file_name) values (%s);'''.format(
                    table_name)
                cursor.execute(query, (csv_file_name,))
                q_status = True
            except Exception as issue_in_video:
                logger.debug("_Issue & Skip this in Video")
                logger.debug("_Issue is {}", issue_in_video)
                # Skip this VIdeo Move Forward

            # return ArgusDB().get_all('''select * from "dave-alpha-build"."for_driver_score";''')
            # pass
        return q_status

    def add_static_csv(self, argus_id, report_id, report_name, url, report_status):
        """
        Add a New Attendance Entry In DBX Attendance CSV

        param:
        Return : If No Issue -> True or False


        """
        logger.info("Insert new_Video in for_driver_score in a Table")
        connection = self.create_connection()
        q_status = False
        if connection != False:
            cursor = connection.cursor()
            connection.autocommit = True
            table_name = argus_id + '_static_reports'
            # print(dave_id,list_videos_name)
            # print(list_videos_name)
            # query=F'INSERT INTO "argus".\"{argus_id}_team\" VALUES (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'
            # query=F'Insert Into \"argus\".\"{argus_id}_team\"  (name,join_date,department,photos) values (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'

            try:
                query = '''insert into "argus"."{}" (report_id,report_name,url,report_status) values (%s,%s,%s,%s);'''.format(
                    table_name)
                cursor.execute(
                    query, (report_id, report_name, url, report_status,))
                q_status = True
            except Exception as issue_in_video:
                logger.debug("_Issue & Skip this in Video")
                logger.debug("_Issue is {}", issue_in_video)

        return q_status

    def get_report_id_static_csv(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select \"report_id\" from \"argus\".\"{argus_id}_static_reports\";'

                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")
                result = [i[0] for i in result]
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_static_report_csv(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_static_reports\";'

                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Reading Data in a Table")
                print(result)
                report_id, report_name, report_url, report_status = zip(
                    *result)
                return [list(report_id), list(report_name), list(report_url), list(report_status)]

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def get_all_notification(self, argus_id):
        """
        Show all the data from table query

        Parameter : query
        Return :
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                # This line look horror , Purpose for POSTGRE Wants Values must be Dual Quotes
                # Its Give a QUotes Using "ESCAPE SEQUENCE"
                query = F'select * from \"argus\".\"{argus_id}_notification\" ORDER BY activity_id DESC;'

                cursor.execute(query)
                result = cursor.fetchall()

                logger.info("Successfully Reading Data in a Table")
                return result

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")
        return q_status

    def add_notification(self, argus_id, activity_name, activity_detail, activity_status):
        """
        Add a New Team Member

        param: argus_id,emp_name,emp_date,emp_dep,img_link,
        Return : If No Issue -> True or False


        """
        logger.info("Insert new_Video in for_driver_score in a Table")
        connection = self.create_connection()

        activity_start_time = datetime.now().strftime("%Y_%m_%d__%H_%M")

        q_status = False
        if connection != False:
            cursor = connection.cursor()
            connection.autocommit = True
            table_name = argus_id + '_notification'
            # print(dave_id,list_videos_name)
            # print(list_videos_name)
            # query=F'INSERT INTO "argus".\"{argus_id}_team\" VALUES (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'
            # query=F'Insert Into \"argus\".\"{argus_id}_team\"  (name,join_date,department,photos) values (\"{emp_name}\",\"{emp_date}\",\"{emp_dep}\",\"{img_link}\");'

            try:
                query = '''insert into "argus"."{}" (activity_name,activity_detail,activity_status,
                   activity_start_time) values (%s,%s,%s,%s);'''.format(
                    table_name)
                cursor.execute(query, (activity_name, activity_detail,
                                       activity_status, activity_start_time,))
                q_status = True
            except Exception as issue_in_video:
                logger.debug("_Issue & Skip this in Video")
                logger.debug("_Issue is {}", issue_in_video)
                # Skip this VIdeo Move Forward

            # return ArgusDB().get_all('''select * from "dave-alpha-build"."for_driver_score";''')
            # pass
        return q_status

    # Customer Table Operations

    def get_site_AllArgus(self, customer_id):
        """
        Get Site_All_Argus

        Parameter : customer
        Return : dict
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        connection = self.create_connection()
        # print("Connection Status is :",connection)
        logger.info("Reading Data in a Table")
        q_status = False

        if connection != False:
            result = None
            cursor = connection.cursor()
            try:
                query = F'SELECT site_2 FROM argus.customer_table where customer_id={customer_id}; '

                cursor.execute(query)
                result = cursor.fetchone()
                # print(result)
                logger.info("Successfully Reading Data in a Table")
                if result is None:
                    return []
                return result[0]

            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.info("Issue in Reading Data in a Table")
                logger.exception("Issue is")

    def get_allSite_roles(self, customer_id):
        """get allSite and Roles From Customer Table

        Args:
            customer_id (str): Customer_id In Varchar

        Return : dict
        ==> q_status = True -> its means New Table is Created / Or False -> New Table is not created
        """
        query = F'SELECT site_2,roles FROM argus.customer_table where customer_id={customer_id}; '
        return self.get_query(query)

    def get_group_id_name_dis_permissionList(self, customer_id):
        """get Group ID , Group Name , Group Permission

        Args:
            customer_id (str): 4 Digit

        Return:
            if No_Error : List_of_Tuples
            if Error : False
        """
        try:
            logger.info(
                f'_Get group_id , group_name , group_permission for GROUP table ')
            table_name = str(customer_id) + '_group'
            query = F'SELECT group_id , group_name ,group_discription , permission_list FROM \"argus\". \"{table_name}\" '
            return self.get_all(query)
        except Exception as E:
            logger.exception(
                "Error Occurs In FUN : get_group_id_name_dis_permissionList")
            return False

    def get_customer_name_email_status_admin_group(self, customer_id):
        """Get Customer Id , Customer Email, Customer Status , Customer Group From Customer Table

        Args:
            customer_id (_type_): 4 Digit

        Return:
            if No_Error : List_of_Tuples
            if Error : False

        """
        try:
            # table_name = 'customer_table'
            # query = F'SELECT customer_name , customer_email, status , admin_group , roles FROM \"argus\". \"{table_name}\" where customer_id = { int(customer_id) } ; '
            table_name = str(customer_id) + '_users'
            query = F'SELECT user_name , email, status , groups , role , user_id FROM \"argus\". \"{table_name}\" where status = true; '
            logger.info(f'{query}')

            return self.get_all(query)
        except Exception as E:
            logger.exception(
                "Error Occurs In customer_name_email_status_admin_group")
            return False

    def create_new_group(self, customer_id, group_name: str, group_discription: str) -> bool:
        """Create new Group in Database


        Args:
            customer_id (_type_): 4 Digit
            group (str) : Taking from Admin Input
            permission_list (list) : list / Tupe / None

        Return:
            if No_Error : True
            if Error : False

        """

        try:
            table_name = str(customer_id) + '_group'
            # '''insert into "argus"."{}" (activity_name,activity_detail,activity_status,
            #        activity_start_time) values (%s,%s,%s,%s);'''.format(
            #     table_name)
            query = f'''Insert into \"argus\".\"{table_name}\" (group_name,group_discription) values ('{group_name}','{group_discription}')'''
            print(query)
            return self.insert_query(query)
        except Exception as E:
            print(f"Error - {E}")
            logger.exception("Error in Create New Group")
            return False

    def insert_new_user(self, new_user_email, new_user_password, customer_id):

        try:
            table_name = 'user'
            '''insert into "argus"."{}" (activity_name,activity_detail,activity_status,
                   activity_start_time) values (%s,%s,%s,%s);'''.format(
                table_name)
            query = f'''Insert into \"argus\".\"{table_name}\" (user_email,user_ps,customer_id) values ('{new_user_email}','{new_user_password}','{customer_id}') RETURNING user_id'''
            print(query)
            return self.get_query(query)[0]
        except Exception as E:
            print(f"Error - {E}")
            logger.exception("Error in Create New Group")
            return False

    def create_new_user(self, new_user_email, new_user_password, new_user_name, role, customer_id):
        status_insertion = self.insert_new_user(new_user_email, new_user_password, customer_id)
        # status_insertion=True
        print(status_insertion)
        print(type(status_insertion))
        if status_insertion:

            connection = self.create_connection()
            connection.autocommit = True
            q_status = False  # Query_status
            logger.info("Creating Table")
            # logger.info(str(query))
            if connection != False:
                try:
                    cursor = connection.cursor()
                    cursor.execute("""
                    UPDATE argus.customer_table
                    SET roles = jsonb_set(roles, '{%s}', '{"role": "%s","user_id":%d , "user_name" :"%s"}')
                    WHERE customer_id = %s;
                    """ % (new_user_email, role, status_insertion, new_user_name, customer_id))
                    q_status = True
                    print("Query executed successfully")
                    logger.info("Successfully Execute Query")
                except OperationalError as e:
                    print(f"The error '{e}' occurred")
                    logger.debug("Issue is Inserting")
                    logger.exception("Issue is ")
                except Exception as er:
                    return False
            return q_status

    def check_user_email_get_ps(self, email):
        """Get all Users Email , Users HashPassword, 

         Args:
            email(str):

         Return:
             if No_Error : return tuple
             if No Email : found Return None
             if Error : False

         """
        try:
            table_name = "user"
            logger.info(
                f'_Get user_ps from user Table . user_entered_email : {email} ')
            table_name = 'customer_table'
            query = F'SELECT user_ps  FROM \"argus\".\"user\" where user_email = \'{email}\' ; '

            return self.get_query(query)
        except Exception as E:
            logger.exception("Error in user Email")
            return False

    def check_user_email_get_ps_customer_id_user_id(self, email):
        """Get all Users Email , Users HashPassword, 

         Args:
            email(str):

         Return:
             if No_Error : return tuple
             if No Email : found Return None
             if Error : False

         """
        try:
            table_name = "user"
            logger.info(
                f'_Get user_ps from user Table . user_entered_email : {email} ')
            table_name = 'customer_table'
            query = F'SELECT user_ps,customer_id,user_id  FROM \"argus\".\"user\" where user_email = \'{email}\' ; '
            return self.get_query(query)
        except Exception as E:
            logger.exception("Error in user Email")
            return False

    def get_all_incident(self, customer_id,offset=None,where:dict= None):
        """Get all Users Email , Users HashPassword, 

         Args:
            email(str):

         Return:
             if No_Error : return tuple
             if No Email : found Return None
             if Error : False

         """
        try:
            table_name = str(customer_id) + "_incident"
            print(table_name)
            if where :
                where_condition =f'where '
                for column_name in where :
                    if column_name == 'incident_id' :
                        where_condition+=f"CAST({column_name} AS varchar) like \'%{where[column_name]}%\'"
                    else:
                        where_condition+=f"{column_name} like \'%{where[column_name]}%\'"
                    print(f'Where Condition {where_condition}')
                query =F'SELECT priority,incident_id,category,date,assignee,location,status,assigned_by,mid FROM argus.\"{table_name}\" {where_condition} order by date desc Limit 100 ; '
            elif offset:
                query = F'SELECT priority,incident_id,category,date,assignee,location,status,assigned_by,mid FROM argus.\"{table_name}\" order by date desc Offset {offset} Limit 100 ; '
            else:
                query = F'SELECT priority,incident_id,category,date,assignee,location,status,assigned_by,mid FROM argus.\"{table_name}\" order by date desc Limit 100 ; '
            
            logger.info(query)
            return self.get_all(query)
        except Exception as E:
            logger.exception("Error in user Email")
            return False

    def get_all_incident_mid(self, customer_id, mid):
        """Get all Users Email , Users HashPassword, 

         Args:
            email(str):

         Return:
             if No_Error : return tuple
             if No Email : found Return None
             if Error : False

         """
        try:
            tuple_mid = ()
            if len(mid) == 1:

                print(mid)
                table_name = str(customer_id) + "_incident"
                print(table_name)
                logger.info(
                    f'_Get SELECT priority,incident_id,category,date,assignee,location,status,assigned_by,mid FROM argus.\"{table_name}\" where mid in {tuple_mid};  ')
                query = F'SELECT priority,incident_id,category,date,assignee,location,status,assigned_by,mid FROM argus.\"{table_name}\" where mid = {mid[0]}; '
                return self.get_all(query)
            else:
                tuple_mid = tuple(mid)

            print(mid)
            table_name = str(customer_id) + "_incident"
            print(table_name)
            logger.info(
                f'_Get SELECT priority,incident_id,category,date,assignee,location,status,assigned_by,mid FROM argus.\"{table_name}\" where mid in {tuple_mid};  ')
            query = F'SELECT priority,incident_id,category,date,assignee,location,status,assigned_by,mid FROM argus.\"{table_name}\" where mid in {tuple_mid}; '
            return self.get_all(query)
        except Exception as E:
            logger.exception("Error in user Email")
            return False

    def get_10_incident(self, customer_id):
        """Get all Users Email , Users HashPassword, 

         Args:
            email(str):

         Return:
             if No_Error : return tuple
             if No Email : found Return None
             if Error : False

         """
        try:
            table_name = str(customer_id) + "_incident"
            print(table_name)
            logger.info(
                f'_Get priority,incident_id,category,date,assignee,location,status,assigned_by,location Where Table: {table_name} ')
            query = F'SELECT priority,incident_id,category,date,assignee,location,status,assigned_by FROM argus.\"{table_name}\" ORDER BY date DESC LIMIT 10 ; '
            return self.get_all(query)
        except Exception as E:
            logger.exception("Error in user Email")
            return False

    def get_one_incident(self, customer_id, incident_id):
        """Get all priority,incident_id,category,date,assignee,location,status,assigned_by

         Args:
            email(str):

         Return:
             if No_Error : return tuple 
             if No Email : found Return None
             if Error : False

         """
        try:
            table_name = str(customer_id) + "_incident"
            print(table_name)
            logger.info(
                f'_Get priority,incident_id,category,date,assignee,location,status,assigned_by,location,video_link  Where Table: {table_name} ')
            query = F'SELECT priority,incident_id,category,date,assignee,location,status,assigned_by,video_link FROM argus.\"{table_name}\" where incident_id={incident_id}; '
            return self.get_query(query)
        except Exception as E:
            logger.exception("Error in user Email")
            return False

    def get_today_incident(self, customer_id, date):
        """Get all  priority,incident_id,category,date,assignee,location,status,assigned_by,location

         Args:
            email(str):

         Return:
             if No_Error : return tuple
             if No Email : found Return None
             if Error : False

         """
        try:
            table_name = str(customer_id) + "_incident"
            print(table_name)
            logger.info(
                f'_Get priority,incident_id,category,date,assignee,location,status,assigned_by,location Where Table: {table_name} ')
            query = F'SELECT priority,incident_id,category,date,assignee,location,status,assigned_by FROM argus.\"{table_name}\" ; '
            return self.get_query(query)
        except Exception as E:
            logger.exception("Error in user Email")
            return False

    def insert_new_incident(self, customer_id, incident_id, priority, category, date, location, status, user_id,
                            assignee):
        """Insert New Incident Into DB

        Args:
            customer_id (_type_): _description_
            incident_id (_type_): _description_
            priority (_type_): _description_
            category (_type_): _description_
            location (_type_): _description_
            status (_type_): _description_

        Return :
            True / False
        """
        try:

            table_name = str(customer_id) + "_incident"
            # print(table_name)
            # logger.info(
            #         f'_Get priority,incident_id,category,date,assignee,location,status,assigned_by,location Where Table: {table_name} ')
            query = F'insert into "argus"."{table_name}" (incident_id,priority,category,date,location,status,assigned_by,assignee) values ({incident_id},{priority},{category},\'{date}\',{location},{status},{user_id},{assignee}) ; '
            q_status = self.insert_query(query)
            print(q_status)
            if q_status:
                date = str(date)
                table2 = str(customer_id) + "_incident_history"
                query2 = '''insert into "argus"."{}" (incident_id,incident_status) values (%s, %s)'''.format(table2)
                arg = (incident_id, '{ \"%s\": { "status": %d, "assigned_by": %d, "assignee": %d }}' % (
                date, int(status), int(user_id), int(assignee)))
                print(query2, arg)
                return self.insert_query_with_parameter(query2, arg)


        except Exception as E:
            logger.exception("Error in Create Incident")
            print(E)
            return False

    def update_incident_history(self, customer_id, date, status, assignee, assigned_by, comment, incident_id):
        # status_insertion=True

        connection = self.create_connection()
        connection.autocommit = True
        q_status = False  # Query_status
        logger.info("Creating Table")
        # logger.info(str(query))
        if connection != False:
            try:
                cursor = connection.cursor()

                table_name = str(customer_id) + "_incident_history"

                print("""
                UPDATE argus."%s"
                SET incident_status = jsonb_set(incident_status, '{%s}', '{"status": %d,"assignee":%d , "assigned_by" :%d , "comment":%s}')
                WHERE incident_id = %d ;
                """ % (table_name, date, status, assignee, assigned_by, comment, incident_id))
                cursor.execute("""
                UPDATE argus."%s"
                SET incident_status = jsonb_set(incident_status, '{%s}', '{"status": %d,"assignee":%d , "assigned_by" :%d , "comment":"%s"}')
                WHERE incident_id = %d ;
                """ % (table_name, date, status, assignee, assigned_by, comment, incident_id))

                q_status = True
                print("Query executed successfully")
                logger.info("Successfully Execute Query")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue is Inserting")
                logger.exception("Issue is ")
            except Exception as er:
                print(er)
                return False
        return q_status

    def update_assignedOfficer_incident(self, customer_id, incident_id, assignee):
        """Update Incident Assigned Officer

        Args:
            customer_id (4 Digit): 4 Digit Integer
            incident_id (_type_): 15 Digit Integer
            assignee (_type_): 4 Digit Integer ID

        Returns:
            _type_: _description_
        """

        try:
            table_name = str(customer_id) + '_incident'
            #   query = F'Update \"argus\".\"onboarded_unkownface_search_queue_{argus_id}\" set processed=true,found=\'{found_face}\',count_processed=\'{count_face}\' where emp_name=\'{new_member}\'  ;'

            query = F'UPDATE \"argus\".\"{table_name}\" set assignee={assignee} where incident_id={incident_id}'
            # print(query)

            return self.insert_query(query)
        except Exception as E:
            logger.exception("Error in Assigned Incident")
            print(E)
            return False

    def get_ca_latest_incident(self, customer_id):
        try:
            table_name = str(customer_id) + '_cache_table'
            query = F'''Select feature_value from argus.\"{table_name}\" where feature_name='Latest_IncidentID';'''
            return self.get_query(query)[0]
        except Exception as E:
            print(E)
            return False

    def update_ca_latest_incidentID(self, customer_id, incident_id):
        try:
            table_name = str(customer_id) + '_cache_table'
            query = F'''UPDATE argus.\"{table_name}\" set feature_value=\'{str(incident_id)}\' where feature_name='Latest_IncidentID';'''
            return self.insert_query(query)
        except Exception as E:
            print(E)
            return False

    def del_team_member(self, customer_id, user_id):
        try:
            query = f'UPDATE argus."1002_users" SET status = false Where user_id = {user_id} and down_node = ARRAY[]::integer[] OR down_node IS NULL RETURNING true;'
            updating_status = ArgusDB().get_query(query)
            print(updating_status)
            if updating_status is None:
                return False
            elif updating_status[0] is True:
                print(updating_status)
                return True
        except Exception as E:
            print(E)
        return False

    def update_user_account_detail(self, customer_id, user_email, user_id, user_name, user_role):
        # status_insertion=True

        # print(customer_id,user_email,user_id,user_name,user_role)
        connection = self.create_connection()
        connection.autocommit = True
        q_status = False  # Query_status
        logger.info("Creating Table")
        # logger.info(str(query))
        if connection != False:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                UPDATE argus.customer_table
                SET roles = jsonb_set(roles, '{%s}', '{"role": "%s","user_id":%d , "user_name" :"%s"}')
                WHERE customer_id = %s ;
                """ % (user_email, user_role, user_id, user_name, customer_id))
                q_status = True
                print("Query executed successfully")
                logger.info("Successfully Execute Query")
            except OperationalError as e:
                print(f"The error '{e}' occurred")
                logger.debug("Issue is Inserting")
                logger.exception("Issue is ")
            except Exception as er:
                print(er)
                return False
        return q_status

    # def test_insert():
    #     ins_qry = "INSERT INTO {tablename} ({columns}) VALUES {values};" .format(
    #             tablename=my_tablename,
    #             columns=', '.join(myDict.keys()),
    #             values=tuple(myDict.values())
    #         )
    # cursor.execute(ins_qry)

    # query = F'insert into "argus"."{table_name}" (incident_id,priority,category,date,location,status,assigned_by,assignee) values ({incident_id},{priority},{category},\'{date}\',{location},{status},{user_id},{assignee}) ; '

    def insert_db(self, table_name, Key_values):
        try:

            columns_names = tuple(Key_values.keys())
            columns_values = tuple(Key_values.values())
            new_columns_names = '('
            for each_name in columns_names:
                new_columns_names += each_name + ','
            new_columns_names = new_columns_names[:-1] + ')'
            print(new_columns_names)
            # print(columns_names.replace("'",''))
            query = F'insert into "argus"."{table_name}" {new_columns_names} values {columns_values} ; '
            return self.insert_query(query)
        except Exception as err:
            print(err)
            return False

    def insert_columns_return_columns(self, table_name, Key_values, return_column_name):
        try:

            columns_names = tuple(Key_values.keys())
            columns_values = tuple(Key_values.values())
            new_columns_names = '('
            for each_name in columns_names:
                new_columns_names += each_name + ','
            new_columns_names = new_columns_names[:-1] + ')'
            print(new_columns_names)
            # print(columns_names.replace("'",''))
            query = F'insert into {table_name} {new_columns_names} values {columns_values} RETURNING {return_column_name}; '
            return self.get_query(query)
        except Exception as err:
            print(err)
            return False

    def get_all_department_supervisor(self, customer_id):
        table_name = str(customer_id) + '_users'
        query = F'SELECT user_id , user_name  FROM \"argus\". \"{table_name}\"  where groups = 2'
        return ArgusDB().get_all(query)

    def insert_in_array(self):
        # Step 1
        return 'INSERT INTO array_table (array_column) VALUES (ARRAY[value] )'
        # Step 2
        return 'UPDATE numbers SET numbers = numbers + ARRAY[10] WHERE id =1 '

    def insertion_query(self, table_name: str, columns:dict)->bool:
        """Insert into DB 

            Paramter be Like  : update_query_where ("str ", dict or list of Dict, str -> "id = 1"  )
            Args:
                table_name: The name of the PostgreSQL table to update.
                columns: A dictionary of column names and new values.

            Returns:
                Bool (True / False)
        """
        try:
            print(table_name,columns)
            print(tuple(columns.keys()))
            print(columns.values())
            query=f'''INSERT INTO {table_name} {tuple(columns.keys())} VALUES {tuple(columns.values())}'''
            
            return self.insert_query(query=query)
        except SystemError:
            print('Syntax Error')
        except Exception as E:
            print("Error in Insertion")
        return False

if __name__ == '__main__':
    pass
    print(ArgusDB().check_env_data())
    # customer_id,incident_id,priority,category,date,location,status,user_id,assignee
    # a= ArgusDB().insert_new_incident('1002',0,2,0,121,0,0,5001,5002)
    # print(a)
    # print(ArgusDB().get_query_dict('SELECT * FROM "argus"."1002_incident"'))
    # query='SELECT * FROM argus."1002_users" ORDER BY email ASC '
    # a=ArgusDB().get_all(query)
    # print(a)

    # table_name, columns, where_condition
    # query1= ArgusDB().update_query_where(table_name='1002_users',columns={ 'mobile' : '9876543210'},where_condition="user_id=5044")
    # print(query1)
    # print(ArgusDB().get_columns('1322',)
    # allSite_roles = columns = ArgusDB().get_columns(f'"argus"."1002_activity"',
    #                                                 ["user_id", "activity_page", "activity_action", "date"],
    #                                                 where='user_id = 5001', getOne=False)

    # print(allSite_roles)

    # insertion_query=ArgusDB().insertion_query('argus_101',columns={'Key':"value","K1":"v1"})
    # print(insertion_query)
    # group_data = ArgusDB().get_customer_name_email_status_admin_group('1002')
    # a=ArgusDB().create_new_user('numan@ekak.com',None,None,'readOnly','1001')
    # a=ArgusDB().get_customer_name_email_status_admin_group(1001)
    # a=ArgusDB().create_new_user("testing1","new_user_password","new_user_name","role",1002)
    # b=ArgusDB().get_ca_latest_incident(1002)
    # print(b)
    # customer_id,date, status,assignee, assigned_by, comment,incident_id
    # p=ArgusDB().update_incident_history('1002','200',0,5002, 5001, 'hi',230627171800002)
    # print(p)
