from datetime import datetime
import functools
import pandas as pd
import numpy as np
from typing import List

"""
data type for the log of a single book
"""


@functools.total_ordering
class Book:
    def __init__(self, title: str, dates: List[datetime], progress: List[int]):
        self.title = title
        self.date_started = dates[1]
        self.date_finished = dates[-1]
        self.length = progress[-1]
        self.dates_raw = dates
        self.progress_raw = progress

        if not self._interpolate_data():
            print(f"{self.title} has invalid (out of sync) data, check file!")

    def _interpolate_data(self):
        # interpolate the dates
        dates_interpolated = []
        progress_interpolated = []
        for i in range(len(self.dates_raw)):
            dates_interpolated.append(self.dates_raw[i])
            progress_interpolated.append(self.progress_raw[i])
            if i != (len(self.dates_raw) - 1):
                iterator_date = self.dates_raw[i] + pd.Timedelta("1 days")
                while self.dates_raw[i + 1] != iterator_date:
                    dates_interpolated.append(iterator_date)
                    progress_interpolated.append(self.progress_raw[i])
                    iterator_date = iterator_date + pd.Timedelta("1 days")

        self.dates = dates_interpolated
        self.progress = progress_interpolated
        self.index = np.arange(len(progress_interpolated))

        # check if the interpolation happned correctly
        if len(dates_interpolated) == len(progress_interpolated):
            self.valid = True
            return True
        else:
            self.valid = False
            return False

    def __eq__(self, other):
        return self.date_finished == other.date_finished

    def __lt__(self, other):
        return self.date_started < other.date_finished

    """
    given a .xlsx file, returns corresponding Book adt.
    """

    def from_filepath(fp, title=None):
        assert ".xlsx" in fp, "Not valid file format, requires .xlsx"

        # get the title
        if title is None:
            title = Book._title_from_fp(fp)

        # load the log
        book_sheet = pd.read_excel(fp, sheet_name="Blad1", header=None)
        dates = book_sheet[book_sheet.columns[0]].tolist()
        progress = book_sheet[book_sheet.columns[1]].tolist()

        # add the additional data point of 0 pages read one day before first datapoint.
        first_date = dates[0] - pd.Timedelta("1 days")
        dates = [first_date] + dates
        progress = [0] + progress

        # create the Book abstract data type
        return Book(title, dates, progress)

    def _title_from_fp(fp):
        raw_name = ".".join(fp.split("/")[-1].split(".")[:-1]) + "."

        # filter out the "_"
        name = raw_name[0]
        for i in range(1, len(raw_name) - 1):
            char = raw_name[i]
            if char == "_":
                if raw_name[i + 1] == " ":
                    if raw_name[i - 1] == " ":
                        name = name + "&"
                    else:
                        name = name + ":"
                else:
                    name = name + "'"
            else:
                name = name + char
        return name
