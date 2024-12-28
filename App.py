import tkinter as tk
from Plotter import Plotter
import os


class Application:
    COLOR1 = "black"
    COLOR2 = "white"

    def __init__(self):
        # get names of all directories in logs folder
        possible_years = [
            int(name)
            for name in os.listdir("logs")
            if os.path.isdir(os.path.join("logs", name))
        ]


        self.window = tk.Tk()
        self.window.title("Reading Process Progress")

        self.window.configure(background=self.COLOR2)
        # self.window.grid_rowconfigure(1, minsize=20)
        self.window.grid_rowconfigure(4, minsize=10)
        self.window.grid_columnconfigure(2, minsize=100)
        
        self.plotter = Plotter(possible_years)

        self.label1 = tk.Label(
            self.window, text="Aggregate:", bg=self.COLOR2, fg=self.COLOR1
        )
        self.label1.grid(column=1, row=0)
        btnCompareAverage = tk.Button(
            self.window,
            text="average year by year",
            command=self.plotter.compareAverages,
        )
        btnCompareAverage.grid(column=2, row=1)

        self.label2 = tk.Label(
            self.window, text="Year specific:", bg=self.COLOR2, fg=self.COLOR1
        )
        self.label2.grid(column=1, row=2)

        self.selectedYear = tk.StringVar(self.window)
        self.selectedYear.set(possible_years[-1])  # default value
        yearSelection = tk.OptionMenu(
            self.window, self.selectedYear, *possible_years, command=self.yearEntered
        )
        yearSelection.grid(column=1, row=3)
        btnTimeline = tk.Button(
            self.window, text="timeline of reading", command=self.plotter.plotTimeLine
        )
        btnTimeline.grid(column=2, row=3)
        btnAllTrajectories = tk.Button(
            self.window, text="all trajectories", command=self.plotter.plotTrajectories
        )
        btnAllTrajectories.grid(column=3, row=3)
        btnplotAverageTrajectories = tk.Button(
            self.window,
            text="average trajectories",
            command=self.plotter.plotAverageTrajectories,
        )
        btnplotAverageTrajectories.grid(column=4, row=3)

    def run(self):
        self.window.mainloop()

    def yearEntered(self, val):
        self.plotter.setYear(val)


if __name__ == "__main__":
    app = Application()
    app.run()
