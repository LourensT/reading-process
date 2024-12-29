from .book import Book

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class Plotter:
    def __init__(self, directory: str, period: str):
        self.period = period
        self.tableau20 = [
            (31, 119, 180),
            (174, 199, 232),
            (255, 127, 14),
            (255, 187, 120),
            (44, 160, 44),
            (152, 223, 138),
            (214, 39, 40),
            (255, 152, 150),
            (148, 103, 189),
            (197, 176, 213),
            (140, 86, 75),
            (196, 156, 148),
            (227, 119, 194),
            (247, 182, 210),
            (127, 127, 127),
            (199, 199, 199),
            (188, 189, 34),
            (219, 219, 141),
            (23, 190, 207),
            (158, 218, 229),
            (31, 119, 180),
            (174, 199, 232),
            (255, 127, 14),
            (255, 187, 120),
            (44, 160, 44),
            (152, 223, 138),
            (214, 39, 40),
            (255, 152, 150),
            (148, 103, 189),
            (197, 176, 213),
            (140, 86, 75),
            (196, 156, 148),
            (227, 119, 194),
            (247, 182, 210),
            (127, 127, 127),
            (199, 199, 199),
            (188, 189, 34),
            (219, 219, 141),
            (23, 190, 207),
            (158, 218, 229),
        ]

        # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
        for i in range(len(self.tableau20)):
            r, g, b = self.tableau20[i]
            self.tableau20[i] = (r / 255.0, g / 255.0, b / 255.0)

        self.data_loaded = False
        self._load_all_logs(directory)

    def _get_list_of_logs(self, fp):
        filenames_relative = os.listdir(fp)
        filenames = []
        for item in filenames_relative:
            if ".xlsx" in item:
                filenames.append(os.path.join(fp, item))

        return filenames

    def _load_all_logs(self, fp):
        if not self.data_loaded:
            self.all_books = []

            filepaths = self._get_list_of_logs(fp)

            for item in filepaths:
                print("Loading: " + item)
                if "#DNF" not in item:
                    self.all_books.append(Book.from_filepath(item))
                else:
                    print("Skipping discontinued book.")

            # sort the books
            self.all_books.sort()

            # print the index
            print("=====================")
            print("OVERVIEW OF BOOKS:")
            for e, book in enumerate(self.all_books):
                print(f"* ({e+1}) {book.title}")
            print("=====================")
            self.data_loaded = True

            self._calculate_stats()


    def plot_trajectories(self):
        if not self.data_loaded:
            raise Exception("Data not loaded, call loadAll() first")

        fig = plt.figure(figsize=(15, 7), dpi=200)
        ax = fig.add_subplot(111)

        for rank, book in enumerate(self.all_books):
            if book.valid:
                ax.plot(book.index, book.progress, color=self.tableau20[rank])
            else:
                print("skipped: " + book.title + "it's out of sync")

        ax.set_title(label=f"{self.period}: Progress per book over time, compared")
        ax.set_xlabel(xlabel="Days")
        ax.set_ylabel(ylabel="Pages")

        ax.grid(True)
        Plotter._disable_spines(ax)

        return fig

    def plot_average_trajectories(self):
        if not self.data_loaded:
            raise Exception("Data not loaded, call loadAll() first")

        fig = plt.figure(figsize=(15, 7), dpi=200)
        ax = fig.add_subplot(111)

        for book in self.all_books:
            if book.valid:
                ax.plot(book.index, book.progress, alpha=0.2, color="grey")
            else:
                print("skipped: " + book.title + "it's out of sync")

        averageprogress = self._calculate_average()
        index = np.arange(len(averageprogress))
        plt.plot(index, averageprogress, color="black")

        ax.set_title(label=f"{self.period}: Average Book Progress")
        ax.set_xlabel(xlabel="Days")
        ax.set_ylabel(ylabel="Pages")

        Plotter._disable_spines(ax)
        ax.grid(True)

        return fig

    def plot_timeline(self):
        if not self.data_loaded:
            raise Exception("Data not loaded, call loadAll() first")

        fig = plt.figure(figsize=(15, 7), dpi=200)
        ax = fig.add_subplot(111)

        for rank, book in enumerate(self.all_books):
            if book.valid:
                ax.plot(book.dates, book.progress, lw=2, color=self.tableau20[rank])
                y_pos = book.progress[-1] - 5
                x_pos = book.dates[-1]

                ax.text(
                    x_pos,
                    y_pos,
                    "(" + str(rank + 1) + ")",
                    fontsize=12,
                    color=self.tableau20[rank],
                )
            else:
                print("skipped: " + book.title + "it's out of sync")

        ax.grid(True)
        ax.set_title(f"{self.period}: Progress per book over time, compared")
        ax.set_xlabel("Days")
        ax.set_ylabel("Pages")

        Plotter._disable_spines(ax)

        first_day = self.all_books[0].date_started - pd.Timedelta("1 days")
        last_day = self.all_books[-1].date_finished + pd.Timedelta("1 days")

        # set the months on the x-axis
        ax.set_xlim(first_day, last_day)

        months = mdates.MonthLocator()  # every month
        ax.xaxis.set_major_locator(months)

        yearsFmt = mdates.DateFormatter("%B")  # every year
        ax.xaxis.set_major_formatter(yearsFmt)

        ax.tick_params(
            axis="both",
            which="both",
            bottom="off",
            top="off",
            labelbottom="on",
            left="off",
            right="off",
            labelleft="on",
        )

        return fig

    def _calculate_average(self):
        daysperbook = 0
        for item in self.all_books:
            daysperbook += len(item.progress)
        averagedays = int(daysperbook / len(self.all_books))

        averageprogress = []
        for i in range(0, averagedays):
            dayprogress = 0
            amountofbooks = 0
            for item in self.all_books:
                if len(item.progress) > (i + 1):
                    dayprogress += int(item.progress[i + 1] - item.progress[i])
                    amountofbooks += 1

            if i == 0:
                averageprogress.append(0)
            else:
                averageprogress.append(
                    averageprogress[-1] + (dayprogress / amountofbooks)
                )

        return averageprogress

    def _total_pages(self):
        total = 0
        for item in self.all_books:
            if isinstance(item.progress[-1], int):
                total += item.progress[-1]

        return total

    def _stats_of_an_average_book(self):
        total = 0
        days = 0
        for item in self.all_books:
            days += len(item.progress)
            if isinstance(item.progress[-1], int):
                total += item.progress[-1]

        avg_days = days / len(self.all_books)
        avg_pages = total / len(self.all_books)

        return round(avg_days, 2), round(avg_pages, 2)

    def _disable_spines(ax):
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    def _calculate_stats(self):
        print("Statistics:")
        print(str(self._total_pages()) + " pages in total")
        print(str(self._stats_of_an_average_book()[1]) + " average pages per book")
        print(str(self._stats_of_an_average_book()[0]) + " average days per book")
        print("\n")
