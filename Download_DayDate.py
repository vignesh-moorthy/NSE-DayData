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

import requests, zipfile, io
import pandas as pd
from datetime import datetime,timedelta

Start_date="enter_start_date_in_DDMMMYYYY"
End_date="enter_end_date_in_DDMMMYYYY"
#Start_date="09OCT2019"
#End_date="12OCT2019"
#If no date is given, then it will download the files from the 7 previous days

d_path='Path_to_download_the_csv_file'
#Example: d_path='D:\Trade\Day_Bhavcopy.'
#If you fail to specify a path, the csv files will get downloaded in the path where this code is saved(Under /Path_to_download_the_extracted_file).

#Def for downloading and Unzipping the File    
def req(zip_file_url):
    r = requests.post(zip_file_url)
    status_code=r.status_code
    #print(status_code)
    #If status code is <> 200, it indicates that no data is present for that date. For example, week-end, or trading holiday.
    if status_code==200:
        print("File Available.Downloading")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path=d_path)
    else:
        print("File Not Available.Moving to next date.")


#Main Program
today_date=datetime.now()

#Populating today's date as default, if the stat_date and/or End_date is not provided.
if Start_date=="" or Start_date=="enter_start_date_in_DDMMMYYYY":
    Start_date=(datetime.now()-timedelta(days=7))
    End_date=today_date
if End_date=="" or End_date=="enter_start_date_in_DDMMMYYYY":
        End_date=today_date

daterange = pd.date_range(Start_date,End_date)

#Looping through each date, and downloading the file.
for single_date in daterange:
    loop_date=single_date.strftime("%Y-%b-%d")
    year,month,date=loop_date.split('-')
    month=month.upper()
    weekday=single_date.weekday()
    #If day is not Saturday or Sunday,then proceed to download the file.
    if weekday not in [5,6]:
        print(loop_date)
        temp_zip_file_url = 'https://www.nseindia.com/content/historical/EQUITIES/'+year+'/'+month+'/cm'+date+month+year+'bhav.csv.zip'
        req(zip_file_url=temp_zip_file_url)
        #print(temp_zip_file_url)

"""
count=0
for single_date in daterange:
    loop_date=single_date.strftime("%Y-%b-%d")
    year,month,date=loop_date.split('-')
    month=month.upper()
    weekday=single_date.weekday()
    if weekday not in [5,6]:
        count=count+1
print(count)
"""
