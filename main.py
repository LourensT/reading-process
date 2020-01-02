from typing import Dict
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229),
             (31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

def LogBook(filepath):
    print(filepath)
    response = {}

    book = pd.read_excel(filepath, sheet_name='Blad1', header=None)
    dates = book[book.columns[0]].tolist()
    progress = book[book.columns[1]].tolist()

    print(book)
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
                print(iterator_date)
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
        response['index'] = np.arange(len(progress_interpolated))
        response['InSync'] = True
    else:
        response['dates'] = dates_interpolated
        response['progress'] = progress_interpolated
        response['index'] = np.arange(len(progress_interpolated))
        response['InSync'] = False

    title = filepath[int(filepath.rfind('\\')+1) : -5]
    response['title'] = title
    response['finished'] = dates[-1]
    response['length'] = progress[-1]

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

def AddToPLot(book, rank):
    if book['InSync']:
        plt.plot(book['dates'],book['progress'], lw=2, color=tableau20[rank])
        y_pos = book['progress'][-1] -5
        x_pos = book['dates'][-1]
        if rank == 16:
            y_pos = 700
        plt.text(book['dates'][-1], y_pos, '('+ str(rank+1)+')', fontsize=12, color=tableau20[rank])
        print('plotted: ' + book['title'])
    else:
        print('skipped: ' + book['title'] + 'it\'s out of sync')


def AddAnEvent(date, label):
    plt.axvline(x=(date+pd.Timedelta('4 days')), color='k', linestyle='--', label=label,alpha=0.3)
    plt.text(date,860,label,rotation=90, alpha=0.5, fontsize='small')

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

def AveragePlot(all_data):
    daysperbook = 0
    for item in all_data:
        daysperbook += len(item['progress'])
    averagedays = int(daysperbook/len(all_data))

    index = np.arange(averagedays)

    averageprogress = []
    for i in range(0, averagedays):
        dayprogress = 0
        amountofbooks = 0
        #print(i)
        for item in all_data:
            if len(item['progress']) > (i+1):
                dayprogress += int(item['progress'][i+1] - item['progress'][i])
                amountofbooks += 1
        print(i, amountofbooks, dayprogress)
        if i == 0:
            averageprogress.append(0)
        else:
            averageprogress.append(averageprogress[-1] + (dayprogress/amountofbooks))

    for book in all_data:
        if book['InSync']:
            plt.plot(book['index'],book['progress'], alpha=0.2, color='grey')
            print('plotted: ' + book['title'])
        else:
            print('skipped: ' + book['title'] + 'it\'s out of sync')

    print(index)
    print(averageprogress)
    plt.plot(index,averageprogress, color='black')

    plt.grid(False)
    plt.title(label='Average Book Progress')
    plt.xlabel(xlabel='Days')
    plt.ylabel(ylabel='Pages')
    ShowPlot(which=1)


def ComparePlot(all_data):
    for rank, book in enumerate(all_data):
        if book['InSync']:
            plt.plot(book['index'],book['progress'], color=tableau20[rank])
            text = [16, 18, 4, 6]
            if rank in text:
                y_pos = book['progress'][-1] - 25
                x_pos = book['dates'][-1]
                plt.text(book['index'][-1], y_pos, '('+ str(rank+1)+')', fontsize=12, color=tableau20[rank])
            print('plotted: ' + book['title'])
        else:
            print('skipped: ' + book['title'] + 'it\'s out of sync')
    plt.grid(False)
    plt.title(label='Progress per book over time, compared')
    plt.xlabel(xlabel='Days')
    plt.ylabel(ylabel='Pages')
    ShowPlot(which=1)

def TotalPages(data):
    total = 0
    for item in data:
        if isinstance(item['progress'][-1], int):
            total += item['progress'][-1]

    return total

def AverageBook(data):
    total = 0
    days = 0
    for item in data:
        days += len(item['progress'])
        if isinstance(item['progress'][-1], int):
            total += item['progress'][-1]

    avg_days = days / len(data)
    avg_pages = total / len(data)

    return avg_days, avg_pages

def CalculateStats(alldata):
    print('Statistics:')
    print(str(TotalPages(alldata)) + ' pages in total' )
    print(str(AverageBook(alldata)[1]) + 'average pages per book' )
    print(str(AverageBook(alldata)[0]) + 'average days per book' )

def ShowPlot(which=0):
    if which == 0:
        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        #plt.xlim(pd.Timestamp(year=2017, month=12, day=14), pd.Timestamp(year=2018, month=12, day=20))
        plt.xlim(pd.Timestamp(year=2018, month=12, day=14), pd.Timestamp(year=2019, month=12, day=31))
        #plt.ylim(0, 880)

        #plt.yticks(range(0, 880, 100), fontsize=10)
        months = mdates.MonthLocator()  # every month
        ax.xaxis.set_major_locator(months)
        yearsFmt = mdates.DateFormatter('%B')
        print(yearsFmt)
        ax.xaxis.set_major_formatter(yearsFmt)

        plt.tick_params(axis="both", which="both", bottom="off", top="off",
                    labelbottom="on", left="off", right="off", labelleft="on")

        plt.show()
    if which == 1:
        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        plt.grid(True)

        #plt.xlim(0, 70)
        #plt.ylim(0, 880)

        #plt.yticks(range(0, 880, 100), fontsize=10)
        #plt.xticks(range(0, 71, 5), fontsize=10)

        plt.show()

def FirstDate(book):
    print(book['dates'][0])
    return book['dates'][0]


all_data = AllBooks(startdir="logs\\2019\\")
all_data.sort(key=FirstDate)

print('Books Loaded and Processed')
print('\n')
CalculateStats(all_data)
ComparePlot(all_data)
AveragePlot(all_data)

#print(all_data)


AddEvents()
for rank, item in enumerate(all_data):
    AddToPLot(item, rank)
    plt.grid(True)
    plt.title(label='Progress per book over time, compared')
    plt.xlabel(xlabel='Days')
    plt.ylabel(ylabel='Pages')
ShowPlot()