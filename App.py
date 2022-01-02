
from tkinter import *
from Plotter import Plotter
import os

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