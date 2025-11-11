#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# UTILITY: Count players per team for billing and verification
# Reads from: seasons/YYYY-YY/output/csv/
# Outputs to: seasons/YYYY-YY/output/reports/player_count.csv
#
import csv
import os
import sys
    
def count_lines_in_csv(file_path):
    # Count the numbers of lines in the CSV file minus the header and return the count
    with open(file_path, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        data = list(reader)
        return len(data) - 1

# Take a string and remove the .csv extension and remove underscores replacing them with spaces
def format_filename(filename):
    """Format the filename to remove the .csv extension and replace underscores with spaces."""
    return filename.replace('.csv', '').replace('_', ' ')

def main(directory):
    """Read through a directory list of csv files and count the number of lines."""
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return
    
    output_data = []

    # Iterate over each file in the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Check if the file is a CSV file
        if file_name.endswith('.csv') and os.path.isfile(file_path):
            num_lines = count_lines_in_csv(file_path)
            cleaned_file_name = format_filename(file_name)
            output_data.append((cleaned_file_name, num_lines))

    # Determine output path based on input directory
    if 'seasons' in directory:
        # Extract season from path and save to reports directory
        parts = directory.split(os.sep)
        season_idx = parts.index('seasons') + 1
        season = parts[season_idx]
        output_dir = os.path.join(os.sep.join(parts[:season_idx+1]), 'output', 'reports')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, 'player_count.csv')
    else:
        # Fallback to current directory
        output_file = "player_count.csv"

    # Write the results to a new CSV file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Team Name", "Number of Players"])
        writer.writerows(output_data)

    print(f"Done! Player count report saved to: {output_file}")
    
    # Print summary
    total_players = sum(count for _, count in output_data)
    print(f"\nTotal teams: {len(output_data)}")
    print(f"Total players: {total_players}")

if __name__ == "__main__":
    # Get the directory path from the command line
    if len(sys.argv) < 2:
        print("Usage: python3 bin/count_players.py <csv_directory>")
        print("Example: python3 bin/count_players.py seasons/2025-26/output/csv")
        sys.exit(1)
    dir_path = sys.argv[1]
    main(dir_path)
