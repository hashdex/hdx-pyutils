import boto3
import requests
from datetime import date, datetime, timedelta
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = None
logger = None

def create_session():
    session = boto3.session.Session()
    return session

def get_session():
    '''Singleton pattern for getting AWS session.'''
    global session
    if(session is None):
        session = create_session()
    return session

def bdays(date = date.today().strftime("%Y-%m-%d"), daysToAdd = 1, 
          dayCountType = 2, cal_name = 'BRA - Banks'):
    """Add days to a date using a specific day count for a calendar name"
    
    @param date: Reference date.
    @param daysToAdd: Count of days to add.
    @param dayCountType: Count type ( 0 = NotSet | 1 = ContinuousDayCount | 2 = BusinessDayCount | 3 = ContinuousDay360Count) 
    @param cal_name: Calendars type ( 'USA - FINRA' | 'UK- Banks' | 'BRA - Banks' | 'B3' | 'HASH11 B3 ETF Primary Market') 
    """

    base_url = 'https://10.10.1.13/pas-referencedata-api/api/v1/'

    add_bdays = 'Calendar/{}/AddDays?date={}&daysToAdd={}&dayCountType={}'.format(cal_name,date,daysToAdd,dayCountType)
    r = requests.get(base_url + add_bdays, verify=False)
    str_datetime = datetime.strptime(r.json(), '%Y-%m-%dT%H:%M:%S')
    return str_datetime.date()