# -*- coding: utf-8 -*-
"""
This code is used to automatically download the DAY wise data (Bhavcopy from NSE Website ) from 2016 onwards as a csv file.

Parameters:

d_path='Path_to_download_the_extracted_file'
Start_date = The date from which you need the Bhavcopy file in DDMMMYYYY format.
End_date = The date from to you need the Bhavcopy file in DDMMMYYYY format.

For example, if you need to download each bhavcopy file from 01OCT2019 to 12OCT2019, the input should be as below.
Start_date="09OCT2019"
End_date="12OCT2019"
"""

import requests, zipfile, io,logging
import pandas as pd
from datetime import datetime,timedelta


Start_date="enter_start_date_in_YYYYMMMDD"
End_date="enter_end_date_in_YYYYMMMDD"

#Start_date="2023MAR01"
#End_date="2023MAR12"
#If no date is given, then it will download the files from the 7 previous days

d_path="Path_to_download_the_csv_file"
#Example: d_path='D:\Trade\Day_Bhavcopy.'
#If you fail to specify a path, the csv files will get downloaded in the path where this code is saved(Under /Path_to_download_the_extracted_file).

#To print Number of working days/files downloaded
global No_of_download,Working_day,Non_Work_day
No_of_download=0
Working_day=0
Non_Work_day=0

#Def for downloading and Unzipping the File    
def req(zip_file_url):
    global No_of_download
    r = requests.post(zip_file_url)
    status_code=r.status_code
    #print(status_code)
    #If status code is <> 200, it indicates that no data is present for that date. For example, week-end, or trading holiday.
    if status_code==200:
        No_of_download=No_of_download+1
        logger.info("File Available.Downloading")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path=d_path)
    else:
        logger.info("******File Not Available.Moving to next date.")



#Main Program
today_date=datetime.now().strftime("%Y%b%d")
logging.basicConfig(filename="Log_"+today_date+".log", format='%(asctime)s %(message)s', filemode='w') 
logger=logging.getLogger() 
logger.setLevel(logging.INFO) 

#Populating today's date as default, if the stat_date and/or End_date is not provided.
if Start_date=="" or Start_date=="enter_start_date_in_YYYYMMMDD":
    Start_date=(datetime.now()-timedelta(days=7)).strftime("%Y%b%d")
    End_date=today_date
if End_date=="" or End_date=="enter_end_date_in_YYYYMMMDD":
        End_date=today_date

daterange = pd.date_range(datetime.strptime(Start_date, "%Y%b%d"),datetime.strptime(End_date, "%Y%b%d"))

#Looping through each date, and downloading the file.
for single_date in daterange:
    loop_date=single_date.strftime("%Y-%b-%d")
    year,month,date=loop_date.split('-')
    month=month.upper()
    weekday=single_date.weekday()
    #If day is not Saturday or Sunday,then proceed to download the file.
    if weekday not in [5,6]:
        Working_day=Working_day+1
        logger.info("Trying to download File of :"+loop_date)
        temp_zip_file_url = 'https://www1.nseindia.com/content/historical/EQUITIES/'+year+'/'+month+'/cm'+date+month+year+'bhav.csv.zip'
        req(zip_file_url=temp_zip_file_url)
        #print(temp_zip_file_url)
    else:
        Non_Work_day=Non_Work_day+1
        
#print("Number of files downloaded:"+str(No_of_download))
logger.info("****************************************************************************************") 
logger.info("No. of files downloaded="+str(No_of_download)) 
logger.info("Span= " + Start_date+ " to " + End_date )
logger.info("No. of weekdays in the given time span="+str(Working_day)) 
logger.info("****************************************************************************************") 
logging.shutdown()
