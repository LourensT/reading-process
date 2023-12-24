import pandas as pd

def scale_last_value(filepath, target_value):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(filepath, header=None, names=['Date', 'Value'], parse_dates=['Date'], sheet_name='Blad1')

    # Linearly scale the values based on the last value
    last_value = df['Value'].iloc[-1]
    scaling_factor = target_value / last_value
    df['Value'] = df['Value'] * scaling_factor
    # to int
    df['Value'] = df['Value'].astype(int)
    # to string dd-mm-yyyy
    # df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

    # Save the scaled data back to the Excel file
    df.to_excel(filepath, index=False, header=None, sheet_name='Blad1')

# Example usage:
# Replace 'your_file.xlsx' with the actual file path and provide the desired target value
scale_last_value("/home/ltouwen/reading-process/logs/2023/V2_ A Novel of World War II - Robert Harris.xlsx", 317)
