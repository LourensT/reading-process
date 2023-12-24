import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Book import Book

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
        existing_years = os.listdir(os.path.join(os.getcwd(), "logs"))
        existing_years = [int(s) for s in existing_years]

        if new_year in existing_years:
            self.year = new_year
            self.data_loaded = False
            return True
        else:
            return False

    def _get_list_of_logs(self):
        fp = os.path.join(os.getcwd(), "logs", str(self.year))
        filenames_relative = os.listdir(fp)
        filenames = []
        for item in filenames_relative:
            if ".xlsx" in item:
                filenames.append(os.path.join(fp, item))

        return filenames

    def loadAll(self):
        if not self.data_loaded:
            self.all_books = []
            filepaths = self._get_list_of_logs()
            for item in filepaths:
                print("Loading: " + item)
                if not '#DNF' in item:
                    self.all_books.append(Book.from_filepath(item))
                else:
                    print("Skipping discontinued book.")

            # sort the books
            self.all_books.sort()

            # print the index
            print("=====================")
            print("OVERVIEW OF BOOKS:")
            for e,book in enumerate(self.all_books):
                print(f"* ({e+1}) {book.title}")
            print("=====================")
            self.data_loaded = True
        
            self.CalculateStats()
    
    def calculateAverage(self):
        daysperbook = 0
        for item in self.all_books:
            daysperbook += len(item.progress)
        averagedays = int(daysperbook/len(self.all_books))

        averageprogress = []
        for i in range(0, averagedays):
            dayprogress = 0
            amountofbooks = 0
            for item in self.all_books:
                if len(item.progress) > (i+1):
                    dayprogress += int(item.progress[i+1] - item.progress[i])
                    amountofbooks += 1

            if i == 0:
                averageprogress.append(0)
            else:
                averageprogress.append(averageprogress[-1] + (dayprogress/amountofbooks))

        return averageprogress

    def plotTrajectories(self):
        self.loadAll() #make sure data is loaded

        for rank, book in enumerate(self.all_books):
            if book.valid:
                plt.plot(book.index, book.progress, color=self.tableau20[rank])
            else:
                print('skipped: ' + book.title + 'it\'s out of sync')
            
        plt.grid(False)
        plt.title(label=f'{self.year}: Progress per book over time, compared')
        plt.xlabel(xlabel='Days')
        plt.ylabel(ylabel='Pages')

        ax = plt.subplot(111)
        Plotter._disable_spines(ax)

        plt.grid(True)
        plt.show()
    
    def plotAverageTrajectories(self):
        self.loadAll()

        for book in self.all_books:
            if book.valid:
                plt.plot(book.index,book.progress, alpha=0.2, color='grey')
            else:
                print('skipped: ' + book.title + 'it\'s out of sync')

        averageprogress = self.calculateAverage()
        index = np.arange(len(averageprogress))
        plt.plot(index,averageprogress, color='black')

        plt.grid(False)
        plt.title(label=f'{self.year}: Average Book Progress')
        plt.xlabel(xlabel='Days')
        plt.ylabel(ylabel='Pages')

        ax = plt.subplot(111)
        Plotter._disable_spines(ax)

        plt.grid(True)
        plt.show()
    
    def plotTimeLine(self):
        self.loadAll() #make sure data is loaded

        for rank, book in enumerate(self.all_books):
            if book.valid:
                plt.plot(book.dates, book.progress, lw=2, color=self.tableau20[rank])
                y_pos = book.progress[-1] -5
                x_pos = book.dates[-1]
                plt.text(book.dates[-1], y_pos, '('+ str(rank+1)+')', fontsize=12, color=self.tableau20[rank])
            else:
                print('skipped: ' + book.title + 'it\'s out of sync')

        plt.grid(True)
        plt.title(label=f'{self.year}: Progress per book over time, compared')
        plt.xlabel(xlabel='Days')
        plt.ylabel(ylabel='Pages')

        ax = plt.subplot(111)
        Plotter._disable_spines(ax)

        # set the months on the x-axis
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
            self.setYear(year)
            self.loadAll()
            for book in self.all_books:
                if book.valid:
                    plt.plot(book.index,book.progress, alpha=0.2, color='black')
                else:
                    print('skipped: ' + book.title + 'it\'s out of sync')
        
            averageprogress = self.calculateAverage()
            index= np.arange(len(averageprogress))
            plt.plot(index,averageprogress, label=str(year))

        #plot final
        plt.legend()

        plt.grid(False)
        plt.title(label='Average Book Progress for all years')
        plt.xlabel(xlabel='Days')
        plt.ylabel(ylabel='Pages')

        ax = plt.subplot(111)
        Plotter._disable_spines(ax)

        plt.grid(True)
        plt.show()
    
    def TotalPages(self):
        total = 0
        for item in self.all_books:
            if isinstance(item.progress[-1], int):
                total += item.progress[-1]

        return total

    def stats_of_an_average_book(self):
        total = 0
        days = 0
        for item in self.all_books:
            days += len(item.progress)
            if isinstance(item.progress[-1], int):
                total += item.progress[-1]

        avg_days = days / len(self.all_books)
        avg_pages = total / len(self.all_books)

        return round(avg_days, 2), round(avg_pages,2)

    def _disable_spines(ax):
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    def CalculateStats(self):
        print('Statistics for ' + str(self.year) + ':')
        print(str(self.TotalPages()) + ' pages in total' )
        print(str(self.stats_of_an_average_book()[1]) + ' average pages per book' )
        print(str(self.stats_of_an_average_book()[0]) + ' average days per book' )
        print('\n')