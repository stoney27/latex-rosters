#!/usr/bin/env python3
#
# Programmer: Scott Stonefield (stoney27@gmail.com)
# Date: Tue Nov 24 19:49:03 EDT 2020
#
# This program reads in a CSV file of Players' names and numbers.
# It also, as a parameter, takes the directory for the individual photos,
# including a file called team_photo and the team name, and builds a new 
# CSV file for Photoshop to automating building memory mates.

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

#--------------------------------------------------------------

if len(sys.argv) != 4:
    print("Inputs needed team name, csv file, and path to photos")
    exit(1)

# csv fileused id Geeks.csv
team_name = sys.argv[1]
filename= sys.argv[2]
path = sys.argv[3]

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

newfile = os.path.splitext(os.path.basename(filename))[0] + "_mm.csv"
csv_file_path = os.path.dirname(filename)

new_csv_file = csv_file_path + '/' + newfile

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

        # look for player photos:
        for player in file_names:
            if row["Lastname"] in player and row["Firstname"] in player:
                row["Photo"] = player

        if row["Photo"] is None:
            print("Error: could not find player photo: {}".format(row["Lastname"]))
            row["Photo"] = "blank"
        
        row["Team"] = team_photo
        csv_writer.writerow(row)
