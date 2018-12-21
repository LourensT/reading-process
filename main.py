from typing import Dict
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import numpy as np
import matplotlib.pyplot as plt


def LogBook(filepath):
    response = {}

    book = pd.read_excel(filepath, sheet_name='Blad1')
    dates = book[book.columns[0]].tolist()
    progress = book[book.columns[1]].tolist()

    first_date = dates[0] - pd.Timedelta('1 days')
    first_progress = 0
    dates = [first_date] + dates
    progress = [first_progress] + progress

    dates_interpolated = []
    progress_interpolated = []
    for i in range(len(dates)):
        dates_interpolated.append(dates[i])
        progress_interpolated.append(progress[i])
        if (i != (len(dates)-1)):
            iterator_date = dates[i] + pd.Timedelta('1 days')
            while (dates[i+1] != iterator_date):
                dates_interpolated.append(iterator_date)
                progress_interpolated.append(progress[i])
                iterator_date = iterator_date + pd.Timedelta('1 days')

    if (len(dates_interpolated) != len(progress_interpolated)):
        print('Error: Progress and Dates out of Sync: ')
        print(filepath[int(filepath.rfind('\\')+1) : -5])
        print('\n')
        InSync = False
    else:
        print('Processed ' + (filepath[int(filepath.rfind('\\')+1) : -5]))
        InSync = True

    if InSync:
        response['dates'] = dates_interpolated
        response['progress'] = progress_interpolated
        response['InSync'] = True
    else:
        response['dates'] = dates_interpolated
        response['progress'] = progress_interpolated
        response['InSync'] = False

    title = filepath[int(filepath.rfind('\\')+1) : -5]
    response['title'] = title
    response['finished'] = dates[-1]

    return response

def GetListOfFiles(startdir):
    filenames_relative = os.listdir(startdir)
    filenames = []
    for item in filenames_relative:
        filenames.append(str(startdir + item))

    return filenames

def AllBooks(startdir = 'logs\\'):
    filepaths = GetListOfFiles(startdir)
    Logs = []
    for item in filepaths:
        Logs.append(LogBook(item))

    return Logs

def AddToPLot(book):
    if book['InSync']:
        plt.plot(book['dates'],book['progress'])
        print('plotted: ' + book['title'])
    else:
        print('skipped: ' + book['title'] + 'it\'s out of sync')

def AddAnEvent(date, label):
    plt.axvline(x=(date+pd.Timedelta('4 days')), color='k', linestyle='--', label=label,alpha=0.3)
    plt.text(date,900,label,rotation=90, alpha=0.5, fontsize='x-small')

def AddEvents():
    events = [(pd.Timestamp(year=2018, month=5, day=24), 'End CE Examperiod'),
            (pd.Timestamp(year=2018, month=8, day=20), 'Moved out for uni'),
            (pd.Timestamp(year=2018, month=3, day=20), 'End Examweek'),
            (pd.Timestamp(year=2017, month=12, day=31), 'Spending new years eve sick in bed'),
            (pd.Timestamp(year=2018, month=8, day=8), 'Return travel with parents'),
            (pd.Timestamp(year=2018, month=6, day=9), 'Return trip with friends'),
            (pd.Timestamp(year=2018, month=11, day=5), 'End Examperiod')
            ]
    for event in events:
        AddAnEvent(event[0], event[1])

def ShowPlot():
    plt.grid(True)
    plt.title(label='Progress per book over time')
    plt.xlabel(xlabel='Time')
    plt.ylabel(ylabel='Pages')
    plt.xlim(pd.Timestamp(year=2017, month=12, day=14), pd.Timestamp(year=2018, month=12, day=20))
    plt.show()
    #plt.

all_data = AllBooks()
print('Books Loaded and Processed')
print('\n')
#print(all_data)
AddEvents()
for item in all_data:
    AddToPLot(item)
ShowPlot()
