import datetime
import pytz


def ist_time():
    ist_time = ''
    try:
        ist_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    except:
        print("Issue in timezone")

        # return False
    return ist_time

def get_IST_today_date_time():
    """ This Calculate the Current India Standard Time 
        Hour : Minutes and Return 

    Returns:
        str: HH:MM
    """
    ist = ist_time()
    # print(ist)
    ist_time_formatted = ist.strftime("%Y_%m_%d__%H_%M")
    # print(ist_time_formatted)

    return ist_time_formatted


def time_compare(time1:str,time2:str) -> str:
     
    """ Compare Two Time in HH:MM 

    Args:
        time1 (str): initial Time
        time2 (str): final Time

    Returns:
        str: time in minute
    """
    date_format_str = '%H:%M'
    start = datetime.datetime.strptime(time1, date_format_str)
    end =   datetime.datetime.strptime(time2, date_format_str)
    # Get interval between two timstamps as timedelta object
    diff = end - start
    # Get interval between two timstamps in hours
    diff_in_min = abs(diff.total_seconds() // 60)
    # print('Difference between two datetimes in hours:')
    return f'{int(diff_in_min)} min'



def get_IST_current_Hour_and_Min() -> str:
    """ This Calculate the Current India Standard Time 
        Hour : Minutes and Return 

    Returns:
        str: HH:MM
    """
    ist = ist_time()
    ist_time_formatted = ist.strftime("%H:%M")
    # print(ist_time_formatted)

    return ist_time_formatted


def get_IST_today_date():
    """ This Calculate the Current India Standard Time 
        Hour : Minutes and Return 

    Returns:
        str: HH:MM
    """
    ist = ist_time()
    # print(ist)
    ist_time_formatted = ist.strftime("%Y/%m/%d")
    # print(ist_time_formatted)

    return ist_time_formatted


def get_today_day():
    """This Calculate the India Standard Time
        Current day
    """
    ist = ist_time().strftime('%A').lower()
    print(ist)
    return ist


def get_that_day_name(date:str):
    """ Get Specific Day
    :return:
    """

    first_dt = datetime.datetime.strptime(date, '%d/%m/%Y')
    day_name = first_dt.strftime('%A').lower()
    # print(day_name)
    return day_name


def cal_thershold_time(time_in_HH_MM, thershold_time_HH_MM):
    try:

        import datetime
        time_delta = datetime.timedelta(minutes=int(thershold_time_HH_MM))
        datetime_object = datetime.datetime.strptime(time_in_HH_MM, '%H:%M')
        calc_entry_thershold = time_delta + datetime_object
        print(time_in_HH_MM)
        calc_entry_thershold = str(calc_entry_thershold.strftime("%H:%M"))
        print('calc_entry_thershold', calc_entry_thershold)

    except Exception as E:
        print(E)
        return 'False'
    return calc_entry_thershold


def days_name_month(month, year) -> list:
    import calendar

    month, year = int(month), int(year)
    # Get the calendar for February 2022
    cal = calendar.monthcalendar(month,year)

    # Loop through each week in the calendar and get the day names
    days = []
    # print(cal)
    for week in cal:
        # print(week)
        for day in week:
            try:
                if day != 0:
                    days.append(calendar.day_name[calendar.weekday(2022, 2, day)])
            except Exception as E:
                # print(E)
                # day is out of range for month
                pass
    return days


if __name__ == '__main__':
    # print(get_IST_today_date())
    # print(get_today_day())
    # print(get_IST_today_date())
    # get_specific_day('04', '2023')
    print(ist_time().strftime('%Y%m%d%H%M'))
    # print("Day Name in Month :" ,days_name_month('2023', '3'))
