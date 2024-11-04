#! /usr/bin/env python3
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

    # Write the results to a new CSV file
    with open("per_team_count.csv", 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Team Name", "Number of Plalyers"])
        writer.writerows(output_data)

    print("Done! Check the file per_team_count.csv for results.")

if __name__ == "__main__":
    # Get the directory path from the command line
    if len(sys.argv) < 2:
        print("Please provide a directory path.")
        sys.exit(1)
    dir_path = sys.argv[1]
    main(dir_path)
