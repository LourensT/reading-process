from typing import Dict
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os


def LogBook(filepath):
    response = {}

    book = pd.read_excel(filepath, sheet_name='Blad1')
    dates = book[book.columns[0]].tolist()
    progress = book[book.columns[1]].tolist()

    response['dates'] = book[book.columns[0]].tolist()
    response['progess'] = book[book.columns[1]].tolist()

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
#a = LogBook('C:\\Projects\\reading-process\\logs\\Angela_s Ashes - Frankie McCourt.xlsx')
#print(a)
print(AllBooks())
