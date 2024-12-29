# %%
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


year = "2024"
fp = "../logs/" + year
paths = sorted(Path(fp).iterdir(), key=os.path.getmtime)

# Filter out non-Excel files
paths = [p for p in paths if p.suffix == ".xlsx"]
for p in paths:
    print(p)

# actual book lengths in pages
pages = [
    90,
    148,
    213,
    175,
    288,
    855,
    256,
    248,
    341,
    314,
    311,
    304,
    289,
    176,
    279,
    116,
    382,
    234,
    314,
    164,
    376,
    140,
    207,
    207,
    148, 
    224,
    1625
]

assert len(paths) == len(pages), [len(paths), len(pages)]

# %%
for item, length in zip(paths, pages):
    scale_last_value(item, length)

# Example usage:
# Replace 'your_file.xlsx' with the actual file path and provide the desired target value
# scale_last_value("/home/ltouwen/reading-process/logs/2023/V2_ A Novel of World War II - Robert Harris.xlsx", 317)
