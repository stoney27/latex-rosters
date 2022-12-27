#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 14:57:48 EST 2022

This script creates LaTeX files from a template and a list of CSV files. It is 
used to create rosters for the player's photo cards. The program takes a single
command line argument, the path to the CSV file directory.
The script will create a LaTeX directory in the current working directory and 
create a LaTeX file for each CSV file in the CSV directory. The LaTeX files are
created by replacing the CSV_FILE string in the RosterTemplate.tex file with the
name of the CSV file. The new LaTeX files are then compiled using pdflatex.
"""
import os
import sys
import subprocess

# Template file with the CSV_FILE string to be replaced
template_file = 'RosterTemplate.tex'
pdflatex_path = '/Library/TeX/texbin/pdflatex'

# Check if a CSV directory was provided as a command line argument
if len(sys.argv) < 2:
    print('Please provide the path to the CSV directory as a command line argument')
    sys.exit(1)

# If the length of the command line argument is greater than 2, then find the
# argument that has .tex in the name and use that as the template file
if len(sys.argv) > 2:
    for arg in sys.argv:
        if arg.endswith('.tex'):
            template_file = arg
        else:
            csv_dir = arg
else:
    # Get the CSV directory from the command line argument
    csv_dir = sys.argv[1]
                    
# Check for the existence of pdflatex, liveTex should be installed
if not os.path.exists(pdflatex_path):
    print('pdflatex not found at {}. Please install it and try again.'.format(pdflatex_path))
    sys.exit(1)

# Check for the existence of the template file
if not os.path.exists(template_file):
    print('Template file {} not found. Please create it and try again. Or pass in the path to the file.'.format(template_file))
    sys.exit(1)

# Get the fully qualified path to the CSV directory
csv_dir = os.path.abspath(csv_dir)

# Create the LaTeX output directory if it doesn't exist
latex_dir = 'LaTeX'
if not os.path.exists(latex_dir):
    os.makedirs(latex_dir)

# Log we are processing the CSV directory
print('Processing CSV directory: {}, and creating LaTeX files...'.format(csv_dir))

# Iterate through the files in the CSV directory
for csv_file in os.listdir(csv_dir):
    # Check if the file is a CSV file
    if csv_file.endswith('.csv'):
        # Construct the full path to the CSV file
        csv_file_path = os.path.join(csv_dir, csv_file)

        # Read the template file
        with open(template_file, 'r') as f:
            template = f.read()

        # Replace the CSV_FILE string with the actual CSV file name
        output = template.replace('CSV_FILE', csv_file_path)

        # Construct the output file name by replacing the .csv extension with .tex
        output_file = csv_file.replace('.csv', '.tex')

        # Save the modified template to a new file in the LaTeX directory with the name of the CSV file and the .tex extension
        with open(os.path.join(latex_dir, output_file), 'w') as f:
            f.write(output)

# Iterate through the files in the LaTeX directory
for tex_file in os.listdir(latex_dir):
    # Check if the file is a .tex file
    if tex_file.endswith('.tex'):
        # Construct the full path to the .tex file
        tex_file_path = os.path.join(latex_dir, tex_file)

        # Log the file we are processing
        print('Processing file: {}'.format(tex_file_path))

        # Run the pdflatex command on the .tex file
        subprocess.run([pdflatex_path, '-output-directory', latex_dir, 
                        tex_file_path], stdout=open('latex_logfile.log', 'a'))

