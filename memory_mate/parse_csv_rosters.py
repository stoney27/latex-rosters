#!/usr/bin/env python3
#
# Programmer: Scott Stonefield (stoney27@gmail.com)
# Date: Sat Jul  9 18:09:14 EDT 2022
#

import csv
import pprint
import sys
import os

pp = pprint.PrettyPrinter(indent=4)

# Function to read in the csv file and return a list of lists
def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        return list(reader)

# Function to break up the list into teams 
def break_up_by_team(list_of_lists):
    # dictionary to hold the teams, player name and number
    teams = {}
    team_name = ''
    lines_skipped = 0
    total_players = 0
    
    for i in range(len(list_of_lists)):
        if list_of_lists[i][1] == "Team" or list_of_lists[i][1] == "Program":
            # Skip header rows
            lines_skipped += 1
            continue
        if list_of_lists[i][0] == "" or list_of_lists[i][0] == " ":
            # Skip blank rows
            lines_skipped += 1
            continue
        
        # set team name to upper case
        list_of_lists[i][1] = list_of_lists[i][1].upper()
        
        # Fix the team name (we want mixed case Black, White, etc.)
        list_of_lists[i][1] = list_of_lists[i][1].replace('BLACK', 'Black')
        list_of_lists[i][1] = list_of_lists[i][1].replace('WHITE', 'White')
        list_of_lists[i][1] = list_of_lists[i][1].replace('RED', 'Red')
        
        if list_of_lists[i][1] != team_name:
            # Start new team
            team_name = list_of_lists[i][1]
            # Check if team name is not in the dictionary start new team
            if team_name not in teams:
                teams[team_name] = {}
        
        # Add the player to the team
        teams[team_name][list_of_lists[i][0]] = list_of_lists[i][2]
        total_players += 1
    
    print("Lines skipped: %d" % lines_skipped)
    print("Total players: %d" % total_players)
    return teams

# Function to seperate first and last name
def separate_first_last_name(name):
    # Check for the number of spaces in the name
    splitname = name.split()  
    case = len(splitname)
    if case == 1:
        # Only one name, return it
        return splitname[0].capitalize(), ''
    if case == 2:
        return splitname[0].capitalize(), splitname[1].capitalize()
    if case == 3:
        if splitname[2] == 'III' or splitname[2] == 'II' or splitname[2] == 'IV' or splitname[1] == 'Van':
            return splitname[0].capitalize(), splitname[1].capitalize() + ' ' + splitname[2]
        if splitname[1].find('(') != -1:
            return splitname[0].capitalize() + ' ' + splitname[1], splitname[2].capitalize()
        else:
            return splitname[0].capitalize() + ' ' + splitname[1].capitalize(), splitname[2].capitalize()
    else:
        print("Error: %s" % name)
    
# Function to write the teams to a separate csv file (per team)
def write_teams_to_csv(team, team_name):
    file_team_name = team_name.replace(' ', '_')
    
    with open(file_team_name + '.csv', 'w') as f:
        writer = csv.writer(f)
        # write header row
        writer.writerow(["Firstname", "Lastname", "Sweater" ,"Team"])

        for player, number in team.items():
            firstName, lastName = separate_first_last_name(player)
            # Check for only one name
            if lastName == '':
                print("UPDATE Needed - Only one name: %s - %s" % (firstName, team_name))

            if firstName.find('.') != -1:
                print("UPDATE Needed - Dot in first name: %s %s - %s" % (firstName, lastName, team_name))
            
            # if lastName has - in it capitalize second name
            if lastName.find('-') != -1:
                lastName_split = lastName.split('-')
                lastName_split[1] = lastName_split[1].capitalize()
                lastName = '-'.join(lastName_split)
            writer.writerow([firstName, lastName, number, team_name])
    
    # print("Wrote team to csv file: {}.csv".format(file_team_name))
    return

# Main function
def main():
    # get command line arguments for file name
    if len(sys.argv) != 2:
        print("Usage: python parse_csv_rosters.py <filename>")
        exit(1)
        
    filename = sys.argv[1]
    
    # Check if file exists
    if not os.path.isfile(filename):
        print("Error: File does not exist: %s" % filename)
        exit(1)
    
    # Read in the csv file
    list_of_lists = read_csv(filename)
    
    # Break up the list of lists by team
    teams = break_up_by_team(list_of_lists)
    
    # Loop through the teams and write them to csv files
    for team in teams:
        write_teams_to_csv(teams[team], team)
    
    print("Done")
    

if __name__ == "__main__":
    main()
    exit(0)