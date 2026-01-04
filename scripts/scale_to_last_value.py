# %%
from datetime import datetime
import pandas as pd
import os
from pathlib import Path


def scale_last_value(filepath, target_value):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(
        filepath,
        header=None,
        names=["Date", "Value"],
        parse_dates=["Date"],
    )

    # Linearly scale the values based on the last value
    last_value = df["Value"].iloc[-1]
    if last_value == target_value:
        return

    scaling_factor = target_value / last_value
    df["Value"] = df["Value"] * scaling_factor
    # to int
    df["Value"] = df["Value"].astype(int)
    # to string dd-mm-yyyy
    # df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

    # Save the scaled data back to the Excel file
    df.to_excel(filepath, index=False, header=None, sheet_name="Blad1")

def return_start(fp: Path):
    """
    Read an excel and return the datetime object of the last date in the first column.

    Checks whether the value is a string or datetime object, and converts assuming (dd-mm-yyyy) format.
    """
    book_sheet = pd.read_excel(fp, header=None)
    date_raw = book_sheet[book_sheet.columns[0]].tolist()[-1]

    if isinstance(date_raw, str):
        try:
            date_formatted = datetime.strptime(date_raw, "%d-%m-%Y")
        except ValueError:
            date_formatted = datetime.strptime(date_raw, "%d-%m-%y")
    else:
        date_formatted = date_raw

    return date_formatted





year = "2025"
fp = "../logs/" + year
paths = Path(fp).iterdir()
# Filter out non-Excel files
paths = [p for p in paths if p.suffix == ".xlsx"]
# sort
paths = sorted(paths, key=return_start)
for p in paths:
    print(p)

# actual book lengths in pages
pages = [ 
    608,
    448,
    131,
    316,
    246,
    272,
    400,
    120,
    225,
    400,
    92,
    433,
    405,
    422,
    272,
    223,
    240,
    112,
    232,
    296,
    261,
    277,
    277,
    280,
    256,
    1276,
    520,
]

assert len(paths) == len(pages), [len(paths), len(pages)]

# %%
for item, length in zip(paths, pages):
    scale_last_value(item, length)

# Example usage:
# Replace 'your_file.xlsx' with the actual file path and provide the desired target value
# scale_last_value("/home/ltouwen/reading-process/logs/2023/V2_ A Novel of World War II - Robert Harris.xlsx", 317)
