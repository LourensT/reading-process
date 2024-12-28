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
        sheet_name="Blad1",
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


year = "2023"
fp = "./logs/" + year
paths = sorted(Path(fp).iterdir(), key=os.path.getmtime)
pages = [
    310,
    317,
    229,
    271,
    95,
    388,
    157,
    487,
    96,
    212,
    285,
    319,
    264,
    496,
    383,
    272,
    393,
    313,
    314,
    208,
    200,
    366,
    578,
    380,
    134,
    299,
    688,
    440,
    131,
    251,
    188,
    226,
    234,
    253,
]

for item, l in zip(paths, pages):
    scale_last_value(item, l)

# Example usage:
# Replace 'your_file.xlsx' with the actual file path and provide the desired target value
# scale_last_value("/home/ltouwen/reading-process/logs/2023/V2_ A Novel of World War II - Robert Harris.xlsx", 317)
