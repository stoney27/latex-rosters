#!/usr/bin/env python3
import csv

def capitalize_field(field):
    return field.capitalize()

def process_csv(input_filename, output_filename):
    # Read the CSV data
    with open(input_filename, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        data = list(reader)

    # Process each cell in the CSV data
    capitalized_data = []
    for row in data:
        capitalized_row = [capitalize_field(cell) for cell in row]
        capitalized_data.append(capitalized_row)

    # Write the modified data back to CSV
    with open(output_filename, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(capitalized_data)

if __name__ == "__main__":
    # Sample usage: processing "sample.csv" and saving to the same file.
    process_csv('Girls_Team_Red.csv', 'Girls_Team_Red.csv')