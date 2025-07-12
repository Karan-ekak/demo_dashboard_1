import ist_time_zone as ist
from datetime import timedelta
from database_connection import ArgusDB
# from flask import current_app
# session=current_app.session



def camera3_analysis_count(customer_id)-> dict:
    """Fetch From and All Input Incident Calculated

       { 
        today: int,
        yesterday: int,
        last6Day: int
        table : {}
        }
    Returns:
        analysis_count : dict{}
        {
            'Today': 0, 
            'Yesterday': 0, 
            'Last 6 Days': sum(6), 
            'Table': [(day1, count1), ...]
    }
    """""
    pass
    

    dict_analysis={
                'Today':0,
                'Yesterday':0,
                'Last 6 Days':0,
                'Table':{}
            }
    try:
        today_ist=ist.ist_time()
        yesterday=today_ist-timedelta(days=1)
        day_6_ago=today_ist-timedelta(days=6)
        print('Six day ago',day_6_ago)
        today_date=int(today_ist.strftime("%Y%m%d"))
        yesterday_date=int(yesterday.strftime("%Y%m%d"))
        day_6_ago_date=int(day_6_ago.strftime("%Y%m%d"))
        
        table_name=f'"argus"."{customer_id}_{table_name}"'
        columns=('date','time','frame_no','count(object)',)
        extra_query=f'''WHERE object='person' AND date between {day_6_ago_date} AND {today_date}
                GROUP BY date,time,frame_no
                ORDER BY date DESC'''
        list_json=ArgusDB().get_columns(table_name=table_name,columns=columns,extra=extra_query)
        
        print(len(list_json),'camera3_analysis_count')
        if len(list_json) == 0:
            return dict_analysis
        
        # Calculating Today IST Date and Time
        sum_count=0
        table_entries=[]
        for each in list_json:
            analytics_count=0
            try:
                try:
                    analytics_count=each[2]//1500
                except Exception as Err:
                    print(Err)
                    analytics_count=0
                if each[0] == today_date:
                    dict_analysis['Today']=analytics_count
                elif each[0] == yesterday_date:
                    dict_analysis['Yesterday']=analytics_count

                sum_count+=analytics_count

                table_entries.append((each[0],analytics_count))
            except Exception as Err:
                print(Err)

        dict_analysis['Last 6 Days']=sum_count
        dict_analysis['Table'] = table_entries
    except Exception as Err:
        print(Err)    

    # print(dict_analysis)
    return dict_analysis


if __name__ == '__main__':
    print(camera3_analysis_count('1002'))