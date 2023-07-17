#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

# This script will read an excel file and create a CSV file for each sheet
# in the excel file. The CSV files will be created in the a cvs sub-directory

import csv
import openpyxl
import os
import sys

# Get the filename from the command line
if len(sys.argv) < 2:
    print("Usage: python export_excel_to_csv.py <filename>")
    sys.exit(1)
filename = sys.argv[1]

# Create the "csv" directory if it doesn't exist
if not os.path.exists("csv"):
    os.makedirs("csv")

# Open the Excel file
wb = openpyxl.load_workbook(filename)

# Iterate through each sheet in the workbook
for sheet in wb:
    # Get the first row (which should contain the headers)
    headers = [cell.value for cell in next(sheet.rows)]

    # Check if the required headers are present
    if not all(header in headers for header in ['Firstname', 'Lastname', 'Team', 'Sweater']):
        # Check for alternative variations of the headers
        if 'First Name' in headers:
            headers[headers.index('First Name')] = 'Firstname'
        if 'Last Name' in headers:
            headers[headers.index('Last Name')] = 'Lastname'
        if not all(header in headers for header in ['Firstname', 'Lastname', 'Team', 'Sweater']):
            print(
                f"Error: Required headers not found in sheet '{sheet.title}'")
            continue

    # If sheet.title has a space in the name, replace it with an underscore
    if ' ' in sheet.title:
        sheet.title = sheet.title.replace(' ', '_')
        
    # Create a CSV file for the sheet
    with open(f'csv/{sheet.title}.csv', 'w', newline='') as csv_file:
        # Create a CSV writer
        writer = csv.writer(csv_file)
        # Write the headers to the CSV file
        writer.writerow(headers)
        # Iterate through the rest of the rows in the sheet and write them to the CSV file
        for row in sheet.rows:
            # If row has headers, skip it
            if row[0].value in headers:
                continue
            writer.writerow([cell.value for cell in row])
