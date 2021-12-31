from typing import Dict
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tkinter import *
'''
NEW CODE BASE
'''
class Plotter:
    tableau20 = []
    data_loaded = False
    all_logs = []

    def __init__(self, pos_years):
        self.year = pos_years[-1]
        self.possible_years = pos_years
        self.tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
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
        for i in range(len(self.tableau20)):
            r, g, b = self.tableau20[i]
            self.tableau20[i] = (r / 255., g / 255., b / 255.)
    
    def setYear(self, new_year):
        existing_years = os.listdir("logs\\")
        existing_years = [int(s) for s in existing_years]

        if new_year in existing_years:
            self.year = new_year
            self.data_loaded = False
            return True
        else:
            return False

    def loadOne(self, filepath):
        #TODO make this a seperate class
        response = {}

        print(filepath)
        book = pd.read_excel(filepath, sheet_name='Blad1', header=None)
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
            #print('Processed ' + (filepath[int(filepath.rfind('\\')+1) : -5]))
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

    def GetListOfFiles(self):
        fp = "logs\\" + str(self.year) + "\\" 
        filenames_relative = os.listdir(fp)
        filenames = []
        for item in filenames_relative:
            filenames.append(str(fp + item))
        return filenames

    def loadAll(self):
        if not self.data_loaded:
            self.all_logs = []
            filepaths = self.GetListOfFiles()
            for item in filepaths:
                if not "#" in item:
                    self.all_logs.append(self.loadOne(item))
                else:
                    print("skipping discontinued books")

            self.all_logs.sort(key=lambda x : x['finished'])
            self.data_loaded = True
        
        self.CalculateStats()
    
    def calculateAverage(self):
        daysperbook = 0
        for item in self.all_logs:
            daysperbook += len(item['progress'])
        averagedays = int(daysperbook/len(self.all_logs))

        averageprogress = []
        for i in range(0, averagedays):
            dayprogress = 0
            amountofbooks = 0
            for item in self.all_logs:
                if len(item['progress']) > (i+1):
                    dayprogress += int(item['progress'][i+1] - item['progress'][i])
                    amountofbooks += 1

            if i == 0:
                averageprogress.append(0)
            else:
                averageprogress.append(averageprogress[-1] + (dayprogress/amountofbooks))

        return averageprogress

    def plotTrajectories(self):
        self.loadAll() #make sure data is loaded

        for rank, book in enumerate(self.all_logs):
            if book['InSync']:
                plt.plot(book['index'],book['progress'], color=self.tableau20[rank])
            else:
                print('skipped: ' + book['title'] + 'it\'s out of sync')
            
        plt.grid(False)
        plt.title(label='Progress per book over time, compared')
        plt.xlabel(xlabel='Days')
        plt.ylabel(ylabel='Pages')

        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        plt.grid(True)
        plt.show()
    
    def plotAverageTrajectories(self):
        self.loadAll()

        for book in self.all_logs:
            if book['InSync']:
                plt.plot(book['index'],book['progress'], alpha=0.2, color='grey')
            else:
                print('skipped: ' + book['title'] + 'it\'s out of sync')

        averageprogress = self.calculateAverage()
        index = np.arange(len(averageprogress))
        plt.plot(index,averageprogress, color='black')

        plt.grid(False)
        plt.title(label='Average Book Progress')
        plt.xlabel(xlabel='Days')
        plt.ylabel(ylabel='Pages')

        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        plt.grid(True)
        plt.show()
    
    def plotTimeLine(self):
        self.loadAll() #make sure data is loaded

        for rank, book in enumerate(self.all_logs):
            if book['InSync']:
                plt.plot(book['dates'],book['progress'], lw=2, color=self.tableau20[rank])
                y_pos = book['progress'][-1] -5
                x_pos = book['dates'][-1]
                plt.text(book['dates'][-1], y_pos, '('+ str(rank+1)+')', fontsize=12, color=self.tableau20[rank])
            else:
                print('skipped: ' + book['title'] + 'it\'s out of sync')

        plt.grid(True)
        plt.title(label='Progress per book over time, compared')
        plt.xlabel(xlabel='Days')
        plt.ylabel(ylabel='Pages')

        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        plt.xlim(pd.Timestamp(year=(self.year - 1), month=12, day=14), pd.Timestamp(year=self.year, month=12, day=31))

        months = mdates.MonthLocator()  # every month
        ax.xaxis.set_major_locator(months)
        yearsFmt = mdates.DateFormatter('%B')
        ax.xaxis.set_major_formatter(yearsFmt)

        plt.tick_params(axis="both", which="both", bottom="off", top="off",
                    labelbottom="on", left="off", right="off", labelleft="on")

        plt.show()

    def compareAverages(self):
        for year in self.possible_years:
            #2018
            self.setYear(year)
            self.loadAll()
            for book in self.all_logs:
                if book['InSync']:
                    plt.plot(book['index'],book['progress'], alpha=0.2, color='black')
                else:
                    print('skipped: ' + book['title'] + 'it\'s out of sync')
        
            averageprogress = self.calculateAverage()
            index= np.arange(len(averageprogress))
            plt.plot(index,averageprogress, label=str(year))

        #plot final
        plt.legend()

        plt.grid(False)
        plt.title(label='Average Book Progress')
        plt.xlabel(xlabel='Days')
        plt.ylabel(ylabel='Pages')

        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        plt.grid(True)
        plt.show()
    
    def TotalPages(self):
        total = 0
        for item in self.all_logs:
            if isinstance(item['progress'][-1], int):
                total += item['progress'][-1]

        return total

    def AverageBook(self):
        total = 0
        days = 0
        for item in self.all_logs:
            days += len(item['progress'])
            if isinstance(item['progress'][-1], int):
                total += item['progress'][-1]

        avg_days = days / len(self.all_logs)
        avg_pages = total / len(self.all_logs)

        return round(avg_days, 2), round(avg_pages,2)

    def CalculateStats(self):
        print('Statistics for ' + str(self.year) + ':')
        print(str(self.TotalPages()) + ' pages in total' )
        print(str(self.AverageBook()[1]) + ' average pages per book' )
        print(str(self.AverageBook()[0]) + ' average days per book' )
        print('\n')


class Application():
    COLOR1 = 'black'
    COLOR2 = 'white'


    def __init__(self) :

        possible_years = [int(i) for i in os.listdir(os.getcwd() + "\\logs\\")]
        self.plotter = Plotter(possible_years)

        self.window = Tk()
        self.window.title("Reading Process Progress")

        self.window.configure(background=self.COLOR1)
        self.window.grid_rowconfigure(1, minsize=20)
        self.window.grid_rowconfigure(4, minsize=10)
        self.window.grid_columnconfigure(2, minsize=100)

        self.selectedYear = StringVar(self.window)
        self.selectedYear.set(possible_years[-1]) # default value
        yearSelection = OptionMenu(self.window, self.selectedYear, *possible_years, command = self.yearEntered)
        yearSelection.grid(column=2, row=0)

        self.plotText = Label(self.window, text="click a button for plot", bg=self.COLOR1, fg=self.COLOR2)
        self.plotText.grid(column=1,row=3)
        btnAllTrajectories = Button(self.window, text="all trajectories", command=self.plotter.plotTrajectories)
        btnAllTrajectories.grid(column=2, row=3)
        btnplotAverageTrajectories = Button(self.window, text="average trajectories", command=self.plotter.plotAverageTrajectories)
        btnplotAverageTrajectories.grid(column=3, row=3)
        btnCompareAverage = Button(self.window, text="average year by year", command=self.plotter.compareAverages)
        btnCompareAverage.grid(column=2, row=5)
        btnTimeline = Button(self.window, text="timeline of reading", command=self.plotter.plotTimeLine)
        btnTimeline.grid(column=3, row=5)

    def run(self):
        self.window.mainloop()

    def yearEntered(self, val):
        self.plotter.setYear(val)



if __name__ == "__main__":
    app = Application()
    app.run()