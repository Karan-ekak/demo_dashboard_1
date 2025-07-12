import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from loguru import logger
import os
host = os.getenv("KANPLAS_DB_HOST")
user = os.getenv("KANPLAS_DB_USER")
password = os.getenv("KANPLAS_DB_PASSWORD")
database = os.getenv("KANPLAS_DB_NAME")
def check_env_data() -> bool:
    '''Check env Data Exist Or Not
    if Data : Exist No Error
    If Data Not Exist : Error
    '''
    env_values = (host, user,
                    password, database)
    # Checking Variable Exist of Not
    env_data_exist = all(var is not None for var in env_values)
    if not env_data_exist:
        # #print("ENV Data is Not Found")
        ##print("No File Found ENV Data - Creditails Not Found")
        # logger.critical("No File Found ENV Data - Creditails Not Found")
        return False
    return
def create_connection():
    """Establishes a connection to the MySQL database."""
    #try:
    if check_env_data() == False:
        return False
    connection = mysql.connector.connect( host=host,
        user=user,
        password=password,
        database=database
        )
    if connection.is_connected():
        print("Connection successful!")
        return connection
    '''except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None'''



def insert_into_table(table_name, data):
    """
    Inserts data into a given table dynamically.
    Args:
        table_name (str): Name of the table.
        data (dict): Column-value pairs to insert.
    """
    print("inserting data")
    connection = create_connection()
    if connection is None:
        print("no connection")
        return
    #try:
    cursor = connection.cursor()
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    values = tuple(data.values())
    # columns = ['video_id', 'video_timestamp', 'total_material_count', 'material_json']
    # values = (data['video_id'],data['video_timestamp'],data['total_material_count'],data['material_count'])
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    # print(sql)
    cursor.execute(sql, values)
    connection.commit()
    # print(f"{cursor.rowcount} record(s) inserted into `{table_name}`.")
    return True



def check_user_email_get_ps_customer_id_user_id( email):
    """
    Get user password hash, customer ID, and user ID based on email.

    Args:
        email (str): User email

    Returns:
        tuple: if found
        None: if no email found
        False: if error
    """
    try:
        connection = create_connection()
        if connection is None:
            print("no connection")
            return
        
        logger.info(f'Fetching user_ps from user table. Email entered: {email}')
        
        # Use backticks (`) to escape `user` table name in MySQL
        query = f"SELECT user_ps, customer_id, user_id FROM `user` WHERE user_email = '{email}';"
        
        return get_query(query)
    except Exception as e:
        logger.exception("Error in user email lookup")
        return False



def get_query(query, params=None):
    """
    Execute a SELECT query and return a single row result.

    Parameters:
        query (str): SQL query to execute.
        params (tuple): Parameters to safely pass into query (optional).

    Returns:
        result (tuple or False): First row of query or False if failed.
    """
    connection = create_connection()
    if connection is None:
        print("No connection")
        return False

    logger.info("Reading data from the table")

    try:
        with connection.cursor() as cursor:
            logger.info(query)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            logger.info("Successfully read data from the table")
            return result

    except Exception as e:
        logger.debug(f"Issue: {e}")
        logger.exception("Query Execution Failed")

    return False



def get_today_defect_count():
    """
    Fetch today's total defect count from the MySQL database.
    Returns:
        int: Total number of defects today
    """
    try:
        connection = create_connection()
        if connection is None:
            print("No connection")
            return 0
        
        # Defect Count Query for today
        query = '''
            SELECT COALESCE(SUM(total_defect_count), 0) AS total_defects_today
            FROM `china7_defect_count`
            WHERE video_timestamp >= CURDATE()
              AND video_timestamp < CURDATE() + INTERVAL 1 DAY;
        '''

        logger.info(f"Executing query: {query}")
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            total_defects = result['total_defects_today'] if result and result['total_defects_today'] is not None else 0
            print("Today's total defects:", total_defects)
            return total_defects

    except Exception as e:
        logger.exception("Error fetching today's defect count")
        return 0



def get_query_dict(query, params=None):
    """
    Execute a SELECT query and return the result as a list of dictionaries.

    Args:
        query (str): SQL query to execute.
        params (tuple): Parameters for query (optional).

    Returns:
        list: List of rows as dictionaries.
    """
    connection = create_connection()
    if connection is None:
        print("No connection")
        return []

    logger.info("Reading data from the table")

    try:
        with connection.cursor(dictionary=True) as cursor:
            logger.info(f"Executing query: {query}")
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            logger.info("Successfully read data from the table")
            return result

    except Exception as e:
        logger.debug(f"Issue: {e}")
        logger.exception("Query Execution Failed")
        return []




def today_breakdown():
    """
    Fetch today's idle time breakdown from the MySQL database.
    Returns:
        str: Breakdown in hours and minutes (e.g., "2 h 30 m")
    """
    try:
        # Create a connection to the database 
        connection = create_connection()
        if connection is None:
            print("No connection")
            return "Connection error"

        # Query for today's idle time 
        query = '''
            SELECT COUNT(*) AS zero_material_count
            FROM `china7_material_count`
            WHERE total_material_count = 0
            AND DATE(video_timestamp) = CURDATE()
            AND (
                (HOUR(video_timestamp) BETWEEN 6 AND 13 AND NOT (TIME(video_timestamp) BETWEEN '09:00:00' AND '09:30:00'))
                OR
                (HOUR(video_timestamp) BETWEEN 14 AND 21 AND NOT (TIME(video_timestamp) BETWEEN '17:00:00' AND '17:30:00'))
                OR
                (
                    ((HOUR(video_timestamp) BETWEEN 22 AND 23) OR (HOUR(video_timestamp) BETWEEN 0 AND 5))
                    AND NOT (TIME(video_timestamp) BETWEEN '02:00:00' AND '02:30:00')
                )
            )
        '''
        
        logger.info(f"Executing query: {query}")
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            zero_material_count = result['zero_material_count'] if result and result['zero_material_count'] is not None else 0
            
            # Convert minutes to hours and minutes
            hours, minutes = divmod(zero_material_count, 60)
            idle_time = f"{hours} h {minutes} m"
            return idle_time

    except Exception as e:
        logger.exception("Error fetching idle time breakdown")
        return "Error"



def insert_query(table_name, Key_values):
    """Generate the insert query."""
    columns = ', '.join(f"`{col}`" for col in Key_values.keys())
    values = ', '.join(f"'{val}'" if val is not None else "NULL" for val in Key_values.values())
    return f"INSERT INTO `{table_name}` ({columns}) VALUES ({values})"

def insert_db(table_name, Key_values):
    """Insert data into the specified table."""
    conn = create_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = insert_query(table_name, Key_values)
        cursor.execute(query)
        conn.commit()
        print(f"Data inserted successfully into {table_name}")
        return True
    except mysql.connector.Error as e:
        print(f"Error while inserting: {e}")
        return False
    finally:
        cursor.close()
        conn.close()




def get_incidents_with_filters(customer_id, selected_dates=None, selected_start_time=None, selected_end_time=None, limit=100, offset=0):
    try:
        table_name = "china7_material_count"
        base_query = f"SELECT id, video_id, total_material_count, video_timestamp FROM `{table_name}`"
        conditions = []

        if selected_dates:
            date_list = "', '".join(selected_dates)
            conditions.append(f"DATE(video_timestamp) IN ('{date_list}')")

        if selected_start_time:
            conditions.append(f"TIME(video_timestamp) >= '{selected_start_time}'")

        if selected_end_time:
            conditions.append(f"TIME(video_timestamp) <= '{selected_end_time}'")

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        base_query += " ORDER BY video_timestamp DESC"
        if not selected_dates and not selected_start_time and not selected_end_time:
            base_query += f" LIMIT {limit} OFFSET {offset * limit}"

        print("QUERY:", base_query)
        return get_all(base_query)

    except Exception as e:
        logger.exception("Error fetching incidents with filters")
        return False

def get_all(query):
    connection = create_connection()
    logger.info("Reading Data in a Table")
    
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully Read Data in a Table")
                return result
        except Exception as e:
            logger.exception("Error during query execution")
    return False


def get_10_incident3(customer_id, selected_dates=None, selected_start_time=None, selected_end_time=None, limit=100, offset=0):
    try:
        table_name = "china7_defect_count"
        base_query = f"SELECT id, video_id, total_defect_count, video_timestamp FROM `{table_name}`"
        conditions = []

        if selected_dates:
            date_list = "', '".join(selected_dates)
            conditions.append(f"DATE(video_timestamp) IN ('{date_list}')")

        if selected_start_time:
            conditions.append(f"TIME(video_timestamp) >= '{selected_start_time}'")

        if selected_end_time:
            conditions.append(f"TIME(video_timestamp) <= '{selected_end_time}'")

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        base_query += " ORDER BY video_timestamp DESC"
        if not selected_dates and not selected_start_time and not selected_end_time:
            base_query += f" LIMIT {limit} OFFSET {offset * limit}"

        print("QUERY :", base_query)
        return get_all(base_query)
    except Exception as e:
        logger.exception("Error fetching incident3 records")
        return False




def get_10_incident_breakdown(customer_id, selected_dates=None, selected_start_time=None, selected_end_time=None, limit=100, offset=0):
    try:
        table_name = "china7_material_count"
        base_query = f"SELECT id, video_id, total_material_count, video_timestamp FROM `{table_name}`"
        conditions = ["total_material_count = 0"]

        if selected_dates:
            date_list = "', '".join(selected_dates)
            conditions.append(f"DATE(video_timestamp) IN ('{date_list}')")

        if selected_start_time:
            conditions.append(f"TIME(video_timestamp) >= '{selected_start_time}'")

        if selected_end_time:
            conditions.append(f"TIME(video_timestamp) <= '{selected_end_time}'")

        base_query += " WHERE " + " AND ".join(conditions)
        base_query += " ORDER BY video_timestamp DESC"

        if not selected_dates and not selected_start_time and not selected_end_time:
            base_query += f" LIMIT {limit} OFFSET {offset * limit}"

        print("QUERY :", base_query)
        return get_all(base_query)

    except Exception as e:
        logger.exception("Error fetching breakdown data")
        return False

#FOR GRAPHS EACH QUERIES REPRESENT THE DIFFRENT GRAPH


def get_shift_materials_breakdown(incidentID=None):
    try:
        query = """
            SELECT 
                s.shift,
                CONCAT(FLOOR(COUNT(*) / 60), 'h ', MOD(COUNT(*), 60), 'm') AS zero_material_duration
            FROM 
                (
                    SELECT 'Shift A' AS shift, '06:00:00' AS start_time, '09:00:00' AS lunch_start, '09:30:00' AS lunch_end, '14:00:00' AS end_time
                    UNION ALL
                    SELECT 'Shift B', '14:00:00', '18:00:00', '18:30:00', '22:00:00'
                    UNION ALL
                    SELECT 'Shift C', '22:00:00', '02:00:00', '02:30:00', '06:00:00'
                ) AS s
            JOIN 
                china7_material_count m
                ON (
                    TIME(m.video_timestamp) >= s.start_time 
                    AND TIME(m.video_timestamp) <= s.end_time
                    AND NOT (TIME(m.video_timestamp) BETWEEN s.lunch_start AND s.lunch_end)
                )
            WHERE 
                DATE(m.video_timestamp) = CURDATE()
                AND m.total_material_count = 0
            GROUP BY 
                s.shift, s.start_time, s.end_time, s.lunch_start, s.lunch_end
            ORDER BY 
                s.start_time;
        """

        results = get_query_dict(query)  # Assuming a helper function already exists

        breakdown = {}
        for row in results:
            shift = row['shift']
            shift_efficiency = row['zero_material_duration']
            breakdown[shift] = {
                'shift_efficiency': shift_efficiency
            }

        print("Breakdown efficiency", breakdown)
        return breakdown

    except Exception as e:
        logger.exception("Error fetching shift materials breakdown data")
        return False



def get_hourly_data(query, value_key):
    try:
        result = get_query_dict(query)
        return [{"hour": row["hour"], "count": row[value_key]} for row in result]
    except Exception as e:
        logger.exception("Error in fetching hourly data")
        return []
def today_breakdown_hour(incidentID=None):
    try:
        query = """
            SELECT 
                DATE_FORMAT(video_timestamp, '%Y-%m-%d %H:00:00') AS hour,
                COUNT(*) AS material_sum
            FROM china7_material_count
            WHERE total_material_count = 0 AND DATE(video_timestamp) = CURDATE()
            GROUP BY hour
            ORDER BY hour DESC;
        """
        result_hour = get_query_dict(query)
        return [{"hour": row["hour"], "count": row["material_sum"]} for row in result_hour]
    except Exception as e:
        logger.exception("Error in fetching hourly breakdown data")
        return []

def today_defects_hour():
    query = """
        SELECT 
            DATE_FORMAT(video_timestamp, '%Y-%m-%d %H:00:00') AS hour,
            SUM(total_defect_count) AS total_defects
        FROM china7_defect_count
        WHERE total_defect_count != 0 AND DATE(video_timestamp) = CURDATE()
        GROUP BY hour
        ORDER BY hour DESC;
    """
    return get_hourly_data(query, value_key="total_defects")


def today_material_hour():
    query = """
        SELECT 
            DATE_FORMAT(video_timestamp, '%Y-%m-%d %H:00:00') AS hour,
            SUM(COALESCE(total_material_count, 0)) AS total_material_count
        FROM china7_material_count
        WHERE DATE(video_timestamp) = CURDATE()
        GROUP BY hour
        ORDER BY hour DESC;
    """
    return get_hourly_data(query, value_key="total_material_count")



def get_quarterly_data(table_name, column_name):
    try:
        query = f"""
            SELECT 
                DATE_FORMAT(
                    DATE_ADD(
                        DATE_ADD(
                            DATE(video_timestamp),
                            INTERVAL HOUR(video_timestamp) HOUR
                        ),
                        INTERVAL FLOOR(MINUTE(video_timestamp)/15)*15 MINUTE
                    ),
                    '%Y-%m-%d %H:%i:00'
                ) AS quarter,
                SUM(COALESCE({column_name}, 0)) AS total_count
            FROM {table_name}
            WHERE 
                DATE(video_timestamp) = CURDATE()
                AND NOT (
                    (TIME(video_timestamp) >= '09:00:00' AND TIME(video_timestamp) < '09:30:00')
                    OR (TIME(video_timestamp) >= '18:00:00' AND TIME(video_timestamp) < '18:30:00')
                    OR ((TIME(video_timestamp) >= '22:00:00' OR TIME(video_timestamp) < '06:00:00')
                        AND TIME(video_timestamp) >= '02:00:00' AND TIME(video_timestamp) < '02:30:00')
                )
            GROUP BY quarter
            ORDER BY quarter DESC;
        """
        results = get_query_dict(query)
        return [{"quarter": row["quarter"], "count": row["total_count"]} for row in results]
    except Exception as e:
        logger.exception(f"Error in fetching quarterly data from {table_name}")
        return []


def today_defects_quarter(incidentID=None):
    return get_quarterly_data("china7_defect_count", "total_defect_count")

def today_material_quarter(incidentID=None):
    return get_quarterly_data("china7_material_count", "total_material_count")


def fetch_json_column(table_name, column_name, incidentID):
    try:
        logger.info(f'_Get {column_name} from Table: {table_name}')
        
       
        query = f"SELECT `{column_name}` FROM `{table_name}` WHERE `video_id` = %s;"
        print("query : ",query)
        
        result = get_query(query, (incidentID,))
        print("result : ",result)
        return result if result else None
    except Exception as e:
        logger.exception(f"Error in fetching {column_name}")
        return None


def fetch_one(incidentID):
    return fetch_json_column("china7_material_count", "material_json", incidentID)

def fetch_one2(incidentID):
    return fetch_json_column("china7_defect_count", "defect_material_json", incidentID)



def fetch_video_timestamp(table_name, incidentID):
    try:
        logger.info(f'_Get video_timestamp from table: {table_name}')
        query = f"SELECT video_timestamp FROM `{table_name}` WHERE video_id={incidentID};"
        result = get_all(query)
        
        if result and len(result) > 0:
            timestamp = result[0][0]
            return timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else None
        return None
    except Exception as E:
        logger.exception("Error in fetching video_timestamp")
        return None


def fetch_time(incidentID):
    return fetch_video_timestamp("china7_material_count", incidentID)


def fetch_time2(incidentID):
    return fetch_video_timestamp("china7_defect_count", incidentID)



