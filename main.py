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

    response['dates'] = book[book.columns[0]].tolist()
    response['progress'] = book[book.columns[1]].tolist()

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
    plt.plot(book['dates'],book['progress'])

def ShowPlot():
    plt.show()

all_data = AllBooks()
for item in all_data:
    AddToPLot(item)
ShowPlot()
