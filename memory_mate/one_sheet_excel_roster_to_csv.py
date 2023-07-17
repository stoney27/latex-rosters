#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import os
import sys
import openpyxl

# Get the file name and sheet name from the command line arguments
file_name = sys.argv[1]
try:
    sheet_name = sys.argv[2]
except IndexError:
    sheet_name = 'Sheet1'

# Open the Excel file
workbook = openpyxl.load_workbook(file_name)

# Get the sheet
sheet = workbook[sheet_name]

# Create a dictionary to hold the team rosters
rosters = {}

# Iterate through the rows of the sheet
for row in sheet.iter_rows():
    # Get the values in the Full Name, Team, and Sweater Name columns
    full_name, team, sweater_name = [cell.value for cell in row[:3]]

    # Skip blank rows
    if full_name is None:
        continue

    # Remove the string ' - Goalie' from the Full Name if it exists
    full_name = full_name.replace(' - Goalie', '')

    # Split the full name into first and last name
    parts = full_name.split(' ')
    first_name = parts[0]
    last_name = ' '.join(parts[1:])

    # Add the player to the roster for their team
    if team not in rosters:
        rosters[team] = []
    rosters[team].append({
        'First Name': first_name,
        'Last Name': last_name,
        'Team': team,
        'Sweater': sweater_name
    })

# Create the "csv" directory if it doesn't already exist
if not os.path.exists('csv'):
    os.makedirs('csv')

# Write out the CSV files for each team
for team, roster in rosters.items():
    # Print the team name
    print(team)
    
    # If the team name has a space in it, replace it with an underscore
    if ' ' in team:
        team = team.replace(' ', '_')
    
    with open(f'csv/{team}.csv', 'w', newline='') as csv_file:
        fieldnames = ['First Name', 'Last Name', 'Team', 'Sweater']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for player in roster:
            writer.writerow(player)
