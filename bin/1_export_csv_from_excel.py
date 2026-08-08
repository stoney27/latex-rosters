#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: 1_export_csv_from_excel.py
# Author: Scott Stonefield
#
# STEP 1: Read in an Excel file and export each sheet as a CSV file
# Outputs to: seasons/YYYY-YY/output/csv/
#
import csv
import openpyxl
import os
import argparse
import sys

# Initial player count
player_count = 0

# Header constants needs to match the headers in the Excel file
HEADER_FIRSTNAME = 'Players First Name'
HEADER_LASTNAME = 'Players Last Name'
HEADER_TEAM = 'Players Team'
HEADER_SWEATER = 'Jersey Number'

# Create mapping for header names to original header names
header_mapping = {
    HEADER_FIRSTNAME: 'Firstname',
    HEADER_LASTNAME: 'Lastname',
    HEADER_TEAM: 'Team',
    HEADER_SWEATER: 'Sweater'
}

def get_season_year():
    """Determine the current season year (e.g., '2025-26')."""
    from datetime import datetime
    now = datetime.now()
    year = now.year
    # If we're in the latter half of the year (Aug-Dec), it's the start of a new season
    if now.month >= 8:
        return f"{year}-{str(year + 1)[-2:]}"
    else:
        return f"{year - 1}-{str(year)[-2:]}"

def get_csv_output_dir(season=None):
    """Get or create the CSV output directory for the season."""
    if season is None:
        season = get_season_year()
    
    csv_dir = f"seasons/{season}/output/csv"
    
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    
    return csv_dir

def clean_name(name, is_last_name=False):
    """Clean a name by removing leading/trailing spaces and capitalizing the first letter."""
    if name is None:
        return None
    name = name.strip()
    if len(name) == 2 and is_last_name:  # if it's a last name and has only two letters
        return name[0].upper() + name[1].lower()
    
    # if name is not a last_namd capitalize both letters unless it matches 'Ty'
    if len(name) == 2 and name.lower() != 'ty':
        return name[0].upper() + name[1].upper()
    
    # if the name has a hyphen, capitalize the first letter after the hyphen
    if '-' in name:
        return '-'.join(word.capitalize() for word in name.split('-'))

    # if the last_name has two c next two each other in the name, capitalize the second c
    if 'mcc' in name.lower() or 'macc' in name.lower():
        print(f"Alert: Found 'cc' in name '{name}'")
        name = name.replace('cc', 'cC')
    # if the name has two words, capitalize each word
    if len(name.split()) == 2:
        return ' '.join(word.capitalize() if word.lower() not in ['iii', 'iv'] else word.upper() for word in name.split())
    return name.capitalize()

def clean_sweater_number(sweater_number):
    """Clean a sweater number by removing non-digit characters."""
    if not sweater_number:
        return '00'
    cleaned_number = ''.join(filter(str.isdigit, str(sweater_number)))
    return cleaned_number if cleaned_number else '00'

def clean_row(row, headers):
    global player_count

    # Skip completely empty rows
    if not row or all(cell is None or str(cell).strip() == "" for cell in row):
        return None

    firstname_index = headers.index(HEADER_FIRSTNAME)
    lastname_index = headers.index(HEADER_LASTNAME)
    sweater_index = headers.index(HEADER_SWEATER)

    row = list(row)

    row[firstname_index] = clean_name(row[firstname_index])
    if row[firstname_index] is None:
        print(f"Error: {HEADER_FIRSTNAME} is empty in row '{row[lastname_index]}' -- team: {row[headers.index(HEADER_TEAM)]}")

    # if the last name is all caps then call clean_name with is_last_name=True
    if row[lastname_index] is not None and row[lastname_index].isupper():
        row[lastname_index] = clean_name(row[lastname_index], is_last_name=True)
    # if last name is all lower case, capitalize the first letter
    elif row[lastname_index] is not None and row[lastname_index].islower():
        row[lastname_index] = clean_name(row[lastname_index])
        
    if row[lastname_index] is None:
        print(f"Error: {HEADER_LASTNAME} is empty in row '{row[firstname_index]}' -- team: {row[headers.index(HEADER_TEAM)]}")

    row[sweater_index] = clean_sweater_number(row[sweater_index])

    player_count += 1
    return row


def sanitize_filename(name):
    """Sanitize a filename by replacing invalid characters and spaces."""
    if not name:
        return ''
    file_name = str(name).replace(' ', '_')
    return ''.join(c if c.isalnum() else '_' for c in file_name)


def is_valid_roster_headers(headers):
    return all(header in headers for header in header_mapping.keys())


def get_headers(sheet):
    """Get the headers from the first row of the sheet."""
    return [cell.value for cell in next(sheet.rows)]


def get_sheet_team_names(sheet, headers, max_rows=1000):
    """Return a set of distinct team names found in the sheet."""
    team_index = headers.index(HEADER_TEAM)
    team_names = set()
    row_count = 0

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row is None or all(cell is None or str(cell).strip() == '' for cell in row):
            continue

        team_name = row[team_index]
        if team_name is not None and str(team_name).strip() != '':
            team_names.add(str(team_name).strip())
            if len(team_names) > 1:
                break

        row_count += 1
        if row_count >= max_rows:
            break

    return team_names


def detect_export_mode(filename):
    """Detect whether the workbook should be exported by workbook or by team."""
    wb = openpyxl.load_workbook(filename, data_only=True)
    valid_sheets = []
    multi_team_sheet_found = False

    for sheet in wb:
        try:
            headers = get_headers(sheet)
        except StopIteration:
            continue

        if not is_valid_roster_headers(headers):
            continue

        valid_sheets.append(sheet)
        if len(get_sheet_team_names(sheet, headers)) > 1:
            multi_team_sheet_found = True
            break

    if multi_team_sheet_found or len(valid_sheets) == 1:
        return 'team'
    return 'workbook'


def export_by_workbook(filename, csv_dir):
    global player_count

    wb = openpyxl.load_workbook(filename, data_only=True)
    player_count = 0

    for sheet in wb:
        headers = get_headers(sheet)
        if not is_valid_roster_headers(headers):
            print(f"Error: Required headers not found in sheet '{sheet.title}'")
            print(f"Found headers:    {headers}")
            print(f"Required headers: {list(header_mapping.keys())}")
            continue

        file_name = sanitize_filename(sheet.title)
        with open(f'{csv_dir}/{file_name}.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([header_mapping[header] for header in headers])

            for row in sheet.iter_rows(min_row=2, values_only=True):
                cleaned_row = clean_row(row, headers)
                if cleaned_row is not None:
                    writer.writerow(cleaned_row)


def create_csv_writer(team_name, headers, csv_dir):
    """Create a new CSV writer for a team."""
    file_name = sanitize_filename(team_name)
    csv_file = open(f'{csv_dir}/{file_name}.csv', 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerow([header_mapping[header] for header in headers])  # write the mapped headers to the CSV file

    return csv_file, writer

def export_by_team(filename, csv_dir):
    global player_count

    wb = openpyxl.load_workbook(filename, data_only=True)
    player_count = 0
    writers = {}
    team_counts = {}

    for sheet in wb:
        headers = get_headers(sheet)
        if not is_valid_roster_headers(headers):
            print(f"Error: Required headers not found in sheet '{sheet.title}'")
            print(f"Found headers:    {headers}")
            print(f"Required headers: {list(header_mapping.keys())}")
            continue

        team_index = headers.index(HEADER_TEAM)

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row is None or all(cell is None or str(cell).strip() == '' for cell in row):
                continue

            team_name = row[team_index]
            if team_name is None or str(team_name).strip() == '':
                continue

            team_name = str(team_name).strip()
            cleaned_row = clean_row(row, headers)
            if cleaned_row is None:
                continue

            file_name = sanitize_filename(team_name)
            if file_name not in writers:
                csv_file, writer = create_csv_writer(team_name, headers, csv_dir)
                writers[file_name] = (csv_file, writer)
                team_counts[file_name] = 0
                print(f"Team: {team_name}")
            else:
                csv_file, writer = writers[file_name]

            writer.writerow(cleaned_row)
            team_counts[file_name] += 1

    for file_name, (csv_file, _) in writers.items():
        csv_file.close()
        if team_counts[file_name] < 10:
            print(f"Alert: Team {file_name} has less than 10 players!")

def main():
    global player_count

    # Command line argument parsing
    parser = argparse.ArgumentParser(
        description='STEP 1: Export Excel roster file to CSV files (one per team).',
        epilog='Example: python3 bin/1_export_csv_from_excel.py seasons/2025-26/input/rosters.xlsx'
    )
    parser.add_argument('filename', help='Path to the Excel file to export (e.g., seasons/2025-26/input/rosters.xlsx)')
    parser.add_argument('--by-team', action='store_true', help='Force export by team.')
    parser.add_argument('--by-workbook', action='store_true', help='Force export by workbook.')
    parser.add_argument('--season', help='Season year (e.g., 2025-26). If not provided, current season is auto-detected.')

    args = parser.parse_args()

    if args.by_team and args.by_workbook:
        print('Error: --by-team and --by-workbook cannot be used together.')
        sys.exit(1)

    # Get the CSV output directory
    csv_dir = get_csv_output_dir(args.season)
    print(f"Output directory: {csv_dir}")

    # Check if the Excel file exists
    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' not found")
        sys.exit(1)

    if args.by_team:
        mode = 'team'
    elif args.by_workbook:
        mode = 'workbook'
    else:
        mode = detect_export_mode(args.filename)
        print(f"Auto-detected export mode: {mode}")

    if mode == 'team':
        export_by_team(args.filename, csv_dir)
    else:
        export_by_workbook(args.filename, csv_dir)
        
    # Print total player count after processing all workbooks
    print(f'\nTotal players: {player_count}')
    print(f'CSV files saved to: {csv_dir}')

if __name__ == '__main__':
    main()
