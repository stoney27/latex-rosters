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
import argparse
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Add the full path to the file names
def photos_full_path(directory):
    '''return the file names with full path'''
    entries = os.listdir(directory)

    fp_names = []
    for entry in entries:
        fp_names.append(os.path.join(directory, entry))

    # Sort so our tests will pass :)
    fp_names.sort()
    return fp_names


# Find the team photo
def find_team_photo(photo_list):
    '''Finds the team photo from the list'''

    for file in photo_list:
        if "Team Photo" in file:
            return file

    return(None)

# Write out the new CSV file
# new_csv_file, player_data, photos_list, team_photo, team_name
def write_csv_file(csv_file, Pdata, Pphotos, team_photo, team_name):
    '''Writes the CSV file'''

    with open(csv_file, "w") as mm_csv:
        neworder = ['Lastname', 'Firstname',
                    'Sweater', 'Team', 'Photo', 'TeamPhoto']
        csv_writer = csv.DictWriter(mm_csv, fieldnames=neworder)
        csv_writer.writeheader()

        for row in Pdata:

            # if team name is not None, use it
            if team_name is not None:
                row["Team"] = team_name

            # look for player photos:
            for player in Pphotos:
                if row["Lastname"] in player and row["Firstname"] in player:
                    row["Photo"] = player

            # if we didn't find a photo, use the blank photo
            if row["Photo"] is None:
                print("Error: could not find player photo: {}".format(
                    row["Lastname"]))
                row["Photo"] = "blank"

            row["TeamPhoto"] = team_photo
            csv_writer.writerow(row)


# Get the command line arguments
def get_check_args():
    '''check the command line arguments'''
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("csv_file", help="CSV file to process")
    arg_parser.add_argument("-t", "--team_name", help="Team name")
    arg_parser.add_argument("-p", "--path", help="Path to photos")
    args = arg_parser.parse_args()

    # if no path is given, use the current directory name
    if args.path is None:
        path = os.getcwd()
    else:
        # trim off any leading spaces
        args.path = args.path.strip()
        path = args.path

    if args.team_name is not None:
        args.team_name = args.team_name.strip()
    # Check to see if csv_file exists
    if not os.path.isfile(args.csv_file):
        print("ERROR: CSV file does not exist: {}".format(args.csv_file))
        exit(1)

    print(f"_Path = {path}")
    print(f"_Filename = {args.csv_file}")
    print(f"_Team name = {args.team_name}")

    return args.csv_file, path, args.team_name

# Make sure the list of photos match the player data and we don't have
# more photos then players in the player data
def check_photos(player_data, photos_list):
    '''Check to see if the photos match the player data'''

    # Get the number of players
    num_players = len(player_data)

    for photo in photos_list:
        found = False
        for row in player_data:
            if row["Lastname"] in photo and row["Firstname"] in photo and row["Sweater"] in photo:
                # Count the number of players found
                num_players -= 1
                found = True
                break

        if not found:
            print(f"ERROR: Could not find player for photo: {photo}")
            return False

    if num_players != 0:
        print(f"ERROR: Number of players in player data does not match number of photos: {num_players}")
        # find the missing player photos
        for player in player_data:
            found = False
            for photo in photos_list:
                if player["Lastname"] in photo and player["Firstname"] in photo and player["Sweater"] in photo:
                    found = True
                    break
            if not found:
                print(f"Missing player photo: {player}")
        return False

    return True


#--------------------------------------------------------------

# Main function
def main():
    '''Main function'''
    filename, path, team_name = get_check_args()
    
    print("Path = {}".format(path))
    print("Filename = {}".format(filename))

    photos_list = photos_full_path(path)

    team_photo = find_team_photo(photos_list)
    print(f"Team photo: {team_photo}")
    if team_photo is None:
        print("ERROR: Could not find team photo, exiting...")
        exit(1)

    photos_list.remove(team_photo)
    
    #
    data = csv.DictReader(open(filename))
    field_names = data.fieldnames
    player_data = list(data)

    # check for all the fields we need
    for field in ['Lastname', 'Firstname', 'Sweater']:
        if field not in field_names:
            print(f"ERROR: Missing field: {field}, exiting...")
            exit(1)

    # Check to see if Team is in the field names
    if "Team" not in field_names:
        # Make sure we have a team name from args
        if team_name is None:
            print("ERROR: No team name found, exiting...")
            exit(1)

    # Check to see if player_data match all photos_list
    if not check_photos(player_data, photos_list):
        print("ERROR: Photos do not match player data, exiting...")
        exit(1)

    newfile = os.path.splitext(os.path.basename(filename))[0] + "_mm.csv"
    csv_file_path = os.path.dirname(filename)

    new_csv_file = csv_file_path + '/' + newfile

    write_csv_file(new_csv_file, player_data, photos_list, team_photo, team_name)

    print("Done!")


if __name__ == "__main__":
    main()
    exit(0)
