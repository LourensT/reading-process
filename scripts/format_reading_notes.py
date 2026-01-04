#!/usr/bin/env python3
"""
Script to format unstructured reading notes into an Excel file using Mistral API.

Takes an input text file with unstructured notes (date - page format)
and outputs an Excel file with two columns: date (DD-MM-YY) and page.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple
import os
import json

import pandas as pd
from dotenv import load_dotenv
from mistralai import Mistral
from mistralai.extra import response_format_from_pydantic_model

from pydantic import BaseModel, Field


class Datapoint(BaseModel):
    day: int = Field(..., description="Day of the month")
    month : int = Field(..., description="Month of the year")
    year : int = Field(..., description="Year (4 digits)")
    value: int = Field(..., description="datapoint value")

class Data(BaseModel):
    datapoints: list[Datapoint] = Field(..., description="List of datapoints")


def parse_input_file(file_path: str) -> List[str]:
    """Parse the input text file and return lines."""
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and line.strip().lower() != 'done']
    return lines


def format_with_mistral(lines: List[str], year: int) -> List[Tuple[str, str]]:
    """Use Mistral API to format the reading notes."""
    load_dotenv()
    
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY not found in .env file")
    
    client = Mistral(api_key=api_key)
    
    # Prepare prompt for Mistral
    prompt = (
        "I have unstructured reading notes in the format 'd page'. "
        "Please extract the date and page number from each line and format them "
        "as 'DD-MM-YY, page'. The year is provided separately, unless explicitly stated in the line. "
        "Here are the lines to process:\n\n"
    )
    
    for line in lines:
        prompt += f"- {line}\n"
    
    prompt += f"\nThe year is: {year}"
    
    messages = [
        {
            "role": "user", 
            "content": prompt
        }
    ]
    
    # Call Mistral API
    chat_response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages,
        temperature=0,
        response_format=response_format_from_pydantic_model(Data)
    )
    
    return json.loads(chat_response.choices[0].message.content)


def create_excel_file(formatted_notes: Data, output_path: str):
    """Create Excel file from formatted notes."""
    rows = []
    for v in formatted_notes["datapoints"]:
        rows.append([f"{v['day']:02d}-{v['month']:02d}-{v['year']}", v["value"]])

    df = pd.DataFrame(rows, columns=["date", "page"])
    df.to_excel(output_path, index=False, header=False)
    print(f"Excel file created: {output_path}")


def infer_output_filename(input_path: str) -> str:
    """Infer output filename from input file path."""
    input_path = Path(input_path)
    base_name = input_path.stem
    output_name = f"{base_name}.xlsx"
    return str(input_path.parent / output_name)


def main():

    input_dir = Path("scripts/unstructured/")

    print(f"Number of files to process: {len(list(input_dir.iterdir()))}")


    for fp in input_dir.iterdir():
        if fp.suffix == ".txt":

            # check if the .xlsx file already exists
            output = infer_output_filename(fp)

            if Path(output).exists():
                print(f"File already exists, skipping: {output}")
                continue


            lines = parse_input_file(str(fp))
            data = format_with_mistral(lines, 2025)
            create_excel_file(data, output)


if __name__ == "__main__":
    main()