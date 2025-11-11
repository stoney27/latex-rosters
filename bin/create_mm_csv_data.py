#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: create_mm_csv_data.py
# Programmer: Scott Stonefield (stoney27@gmail.com)
# Date: Tue Nov 24 19:49:03 EDT 2020
#
# UTILITY: Create Memory Mate CSV data for Photoshop automation
# This program reads in a CSV file of Players' names and numbers.
# It also takes the directory for the individual photos (including team photo),
# and builds a new CSV file for Photoshop to automate building memory mates.
#
# Usage: python3 bin/create_mm_csv_data.py "Team Name" roster.csv photos_dir/
# Output: seasons/YYYY-YY/output/reports/TeamName_mm.csv
#

import csv
import sys
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

# 
def photos_full_path(directory):
    '''return the file names with full path'''
    entries = os.listdir(directory)

    fp_names = []
    for entry in entries:
        fp_names.append(directory + '/' + entry)

    return fp_names

def find_team_photo(photo_list):
    '''Finds the team photo from the list'''

    for file in photo_list:
        if "Team Photo" in file:
            return file

    return(None)

def create_mm_csv_path(photo_directory, roster_filename):
    """Creates the new csv file path for Memory Mate data."""
    # Extract season from roster path if available
    if 'seasons' in roster_filename:
        parts = roster_filename.split(os.sep)
        season_idx = parts.index('seasons') + 1
        season = parts[season_idx]
        reports_dir = os.path.join(os.sep.join(parts[:season_idx+1]), 'output', 'reports')
    else:
        # Fallback to photo directory
        reports_dir = photo_directory
    
    # Create reports directory if it doesn't exist
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    newfile = os.path.splitext(os.path.basename(roster_filename))[0] + "_mm.csv"
    return os.path.join(reports_dir, newfile)

#--------------------------------------------------------------
# Main execution function
#--------------------------------------------------------------

def main():
    """Main function to create Memory Mate CSV"""
    if len(sys.argv) != 4:
        print("Usage: python3 bin/create_mm_csv_data.py <team_name> <csv_file> <photos_directory>")
        print("Example: python3 bin/create_mm_csv_data.py \"12U Black\" seasons/2025-26/output/csv/12U_Black.csv seasons/2025-26/photos/12U_Black/")
        print("\nInputs needed:")
        print("  1. Team name (in quotes if it contains spaces)")
        print("  2. Path to CSV roster file")
        print("  3. Path to directory containing player photos and team photo")
        exit(1)

    # csv fileused id Geeks.csv
    team_name = sys.argv[1]
    filename= sys.argv[2]
    path = sys.argv[3]

    print("Team: {}".format(team_name))
    print("Path = {}".format(path))
    print("Filename = {}".format(filename))

    file_names = photos_full_path(path)

    team_photo = find_team_photo(file_names)
    if team_photo is None:
        print("ERROR: Could not find team photo, exiting...")
        exit(1)

    file_names.remove(team_photo)
    print("Team photo: {}".format(team_photo))

    #
    player_data = csv.DictReader(open(filename))
    field_names = player_data.fieldnames
    csv_file_path = os.path.dirname(filename)
    new_csv_file = create_mm_csv_path(path, filename)

    with open(new_csv_file, "w") as new_csv:

        try:
            field_names.remove("")
        except:
            pass
            
        field_names.append("Teamname")
        field_names.append("Photo")
        
        # if the field name Team is not in the list, add it
        if "Team" not in field_names:
            field_names.append("Team")

        neworder = ['Lastname', 'Firstname', 'Sweater', 'Teamname', 'Photo', 'Team']
        csv_writer = csv.DictWriter(new_csv,fieldnames=neworder)
        csv_writer.writeheader()

        for row in player_data:
            row["Teamname"] = team_name

            # Clean up any blank spaces in Lastname or Firstname
            row["Lastname"] = row["Lastname"].strip()
            row["Firstname"] = row["Firstname"].strip()
            
            # look for player photos:
            for player in file_names:
                if row["Lastname"] in player and row["Firstname"] in player:
                    row["Photo"] = player

            if row["Photo"] is None:
                print("Error: could not find player photo: {}".format(row["Lastname"]))
                row["Photo"] = "blank"
            
            row["Team"] = team_photo
            csv_writer.writerow(row)

    print(f"\nMemory Mate CSV created successfully!")
    print(f"Output file: {new_csv_file}")


if __name__ == "__main__":
    main()
