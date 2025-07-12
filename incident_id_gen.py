import datetime
from database_connection import ArgusDB

"""
Step
Get The Latest inCident Id Cached Table
Insert IncidentID into DB IncidentTable
Update into cached Table
"""



# latest_IncidentID=ArgusDB().get_ca_latest_incident('1002')
# print(latest_IncidentID)


def generate_incidentID(customer_id):
    """ Generating Next Incident ID

    Args:
        customer_id (_type_): 4 Digit interger

    Returns:
        int : 15 Digit Incident ID YYMMDDHHmm_On_of_incident(5 digit)
    """
    today_data=datetime.datetime.now()
    today_date=today_data.strftime("%y%m%d%H%M")


    latest_IncidentID=ArgusDB().get_ca_latest_incident(customer_id)
    print(latest_IncidentID)


    if latest_IncidentID == None or len(latest_IncidentID) != 15:
        # If Incident ID is Not or Digit is not equal to 15
        return int(today_date+'00001')

    elif len(latest_IncidentID) == 15:
        # Check Incident is for today or not 
        print(latest_IncidentID[:6])
        if latest_IncidentID[:6] == str(today_date[:6]):
            # print(latest_IncidentID[10:])
        #     print()
            new_incidentID=int(today_date + latest_IncidentID[10:])+1

            # print("New Incident",new_incidentID)
            return new_incidentID
        else:
            # Not Today, May Be yesterday , So Its Give Today 1st Incide
            return int(today_date+'00001')

    # print("Latest incidetn ID",latest_IncidentID)
    # print(len(latest_IncidentID))

    

# a=generate_incidentID(1002)
# print(a)



# print(today_date)
# count_today_incident=