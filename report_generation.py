from database_connection import ArgusDB
from datetime import datetime, timedelta
import csv
import constants
import os 
import traceback
import dbx_code
import dbx_file_address as dfa
import dbx_token

# Contants Values
report_id =False
report_request_time=False
days_in_numeric={
        0 : "Today",
        1 : "Yesterday",
        7 : "Last Week",
        30 :"Month",
        365 :"Year"
    }

def uploadReport_dbx_add_notification(customer_id,report_path:str,csv_file_name:str):
    csv_file_path = report_path + csv_file_name
    dbx_report_path= dfa.dbx_report(customer_id)
    token=dbx_token.dbx_token()
    # print(token)
    # dbx_code.upload(access_token=token,file_path=report_path+csv_file_name,target_path=dbx_report_path)
    upload_status=dbx_code.upload_file(dbx=token,dbx_path=dbx_report_path+csv_file_name,computer_path=csv_file_path)
    print('Upload Status :',upload_status)
    if not upload_status:
        return False
    # generate File URL :
    url=dbx_code.dropbox_get_link(dbx=token,dropbox_file_path=dbx_report_path+csv_file_name)
    print("URL of the File :",url)

    """ 
    Updating Report_URL, Report Status In DB- Report_Table
    """
    table_name=f'"argus"."{customer_id}_reports"'
    today_date=int(datetime.now().strftime("%Y%m%d%H%M%S"))
    columns={"report_status":1,"report_url":url}
    where_condition=f'report_id = {report_id}'
    update_status_db=ArgusDB().update_query_where(table_name=table_name,columns=columns,where_condition=where_condition)
    print("Uploading file into DB : {update_status}")
    return True

def incident_report_csv(customer_id:int,incident_data:list,dateRange:int):
    columns = ['user_id','user_name']
    table_name = f'"argus"."{customer_id}_users"'
    user_data = ArgusDB().get_columns(table_name=table_name, columns=columns)
    print(user_data)
    name_id=[]

    if user_data == []:
        print('Users Id and Team Data Not Found')
        return 404

    name_id = {user[0]: user[1] for user in user_data}
    name_id[1]='System'
    print(name_id)
    """Table 

    Columns 1: Date and Time
    Columns 2:'incident_id', 
    Columns 3: 'priority',
    Columns 4: 'category', 
    Columns 5: 'location', 
    Columns 6: 'status',
    Columns 7: 'assignee' ,
    Columns 8: 'assigned_by'
    """
    new_incident_data=[]
    new_incident_data.append(['Date Time', 'Incident','Priority','Category','Location','Status','Assignee','Assigned By'])
    for each_incident in incident_data:
        print(each_incident)
        dateTime = str(each_incident[0])
        str_date_time = dateTime[:4] + ' / ' + dateTime[4:6] + ' / ' + dateTime[6:8] + '  ' + dateTime[8:10] + ":" + dateTime[10:12]

        inc_id= 'INC -' + str(each_incident[1])
        priority = constants.incident_data['priority'].get(each_incident[2], 0)
        category = constants.incident_data['category'].get(each_incident[3], 0)
        location = constants.incident_data['location'].get(each_incident[4], 0)
        status = constants.incident_data['status'].get(each_incident[5], 0)
        assignee = name_id.get(each_incident[6],0)
        assigned_by = name_id.get(each_incident[7],0)

        new_incident_data.append([str_date_time,inc_id,priority,category,location,status,assignee,assigned_by])
    # print(new_incident_data)

    
        
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    
    report_path = basedir + "/static/" + customer_id + "/reports/"
    today_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file_name="Argus_Report_"+ days_in_numeric[dateRange] +"_days_gen_"+today_date+".csv"


    with open(report_path+csv_file_name, "w", newline="") as f:
        # Create a CSV writer object.
        writer = csv.writer(f)

        # Write the list of data to the CSV file.
        writer.writerows(new_incident_data)


    return uploadReport_dbx_add_notification(customer_id,report_path,csv_file_name)

def incident_entries(customer_id :str, dateRange :int) -> list | bool:
    report_request_time=int(datetime.now().strftime("%Y%m%d%H%M%S"))
    print(type(dateRange))
    between_date=''
    where_condition = ''

    if dateRange == 0:
        between_date = datetime.now().strftime("%Y%m%d")
        where_condition = f"CAST(date AS VARCHAR) LIKE '{between_date}%' "
        # print(between_date)
    elif dateRange == 1:
        between_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        where_condition = f"CAST(date AS VARCHAR) LIKE '{between_date}%' "

    elif dateRange == 7:
        today_date = datetime.now().strftime("%Y%m%d")

        seven_day_ago = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
        where_condition = f"CAST(date AS VARCHAR) BETWEEN '{seven_day_ago}%' AND '{today_date}%' "

    elif dateRange == 30 :
        between_date = datetime.now().strftime('%Y%m')
        where_condition = f"CAST(date AS VARCHAR) LIKE '{between_date}%' "
    elif dateRange == 365 :
        between_date = datetime.now().strftime('%Y')
        where_condition = f"CAST(date AS VARCHAR) LIKE '{between_date}%' "
    else:
        report_date=report_request_time
        report_table_name=f'"argus"."{customer_id}_reports"'
        report_columns_value={
            "report_name":f"Incident Report {days_in_numeric[dateRange]}",
            "report_date": report_date,
            "report_status":2
        }
        global report_id
        
        report_id=ArgusDB().insert_columns_return_columns(report_table_name,report_columns_value,"report_id")
        report_id=report_id[0]
        print("Wrong Input for Days")
        return False

    columns = [ 'date', 'incident_id', 'priority','category', 'location', 'status','assignee' ,'assigned_by']
    table_name = f'"argus"."{customer_id}_incident"'
    
    incident_data = ArgusDB().get_columns(table_name=table_name, columns=columns, where=where_condition)

    # print(incident_data)
    if incident_data == []:
        """No Data Found in a Incident Table

        """
        report_date=report_request_time
        report_table_name=f'"argus"."{customer_id}_reports"'
        report_columns_value={
            "report_name":f"Incident Report {days_in_numeric[dateRange]}",
            "report_date": report_date,
            "report_status":2
        }
        
        report_id=ArgusDB().insert_columns_return_columns(report_table_name,report_columns_value,"report_id")
        report_id=report_id[0]
        print(report_id)
        print('No Incident Found')
        return 404

    # If This Section Excuting which Means data Found and Generating Report
    report_date=report_request_time
    report_table_name=f'"argus"."{customer_id}_reports"'
    report_columns_value={
        "report_name":f"Incident Report {days_in_numeric[dateRange]}",
        "report_date": report_date,
        "report_status":0
    }
    
    report_id=ArgusDB().insert_columns_return_columns(report_table_name,report_columns_value,"report_id")
    report_id=report_id[0]


    print(f"Len of Incident_Data : {len(incident_data)}" )

    return incident_report_csv(customer_id=customer_id,incident_data=incident_data,dateRange=dateRange)



def report_generate(customer_id: str, dateRange: str) -> str | bool:
    """Get Data From DB According to Date, Insert Into CSV , Upload into DBX and Share Link into DB

    Args:
        customer_id (str): _description_
        dateRange (str): _description_

    Returns:
        URL: _description_

    dateRange Notations : 
        0 Means Today
        1 Means Yesterday
        7 Means Last Week
        30 Last Month
        365 This Year

    """
    days_in_numeric={
        0 : "Today",
        1 : "Yesterday",
        7 : "Last Week",
        30 :"Month",
        365 :"Year"
    }
    
    try:
        dateRange = int(dateRange)
    except TypeError:
        return False
    if dateRange not in [0, 1, 7, 30, 365]:
        return False
    
    all_incident = incident_entries(customer_id, dateRange)

    return "Yes"


if __name__ == '__main__':
    a=incident_entries('1002',0)
    print(a)
    # today_date =

    # seven_day_ago = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    # yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    # print(seven_day_ago)
    # print(type(yesterday))
