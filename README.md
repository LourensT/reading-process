# Visualizing book reading progress

Data Source: I log progress manually in my notes app and then I put it on google sheets. It's a bit of a holiday tradition for me to process this data at the end of the year.

Visualization: Python 3.12 with matplotlib

Beginning 2018, I wanted to take reading a bit more serious, and to motivate myself, I'd log my progress (don't ask me why, but it worked). At the end of 2018 I then wrote some code to make some visualizations out of it. I continued reading and logging my progress, so at the end of 2019 I reworked some of the code with the goal of making this tool a bit more dynamic for years to come.

# Reading per year

* In 2018 I read 25 books, (7645 pages, 305 page average per book, 14 days average per book). 

* In 2019 I read 36 books, (12145 pages, 328.24 page average per book, 11.76 days average per book).

* In 2020, I read 26 books, (8318 pages, 346.58 average pages per book, 18.29 average days per book).

* In 2021, I read 37 books, (10078 pages, 272.38 average pages per book, 13.59 average days per book).

* In 2022, I read 35 books, (9572 pages, 273.49 average pages per book, 13.26 average days per book).

* In 2023, I read 37 books, (10017 pages, 270.73 average pages per book, 15.41 average days per book).

* In 2024, I read 27 books, (8422 pages, 311.93 average pages per book, 31.93 average days per book).

# Install 
Using `uv` as package manager:
```bash
uv venv # create virtual environment
source .venv/bin/activate # activate virtual environment
uv pip install -e .
```
# Usage

For a given period, plots can be generated using the following command:
```bash
uv run -m readingprocess input/dir output/dir --period_name 2024
```
where `--period_name` is an optional argument to name the period in `input/dir`.

If there is a directory with subdirectories corresponding to different periods, the following command can be used to generate plots comparing the periods.
```bash
uv run -m readingprocess input/dir output/dir --grouped
```

# Not using uv
```bash
python -m virtualenv env
source env/bin/activate
pip install -e .
python -m readingprocess input/dir output/dir --period_name 2024
python -m readingprocess input/dir output/dir --grouped
```
