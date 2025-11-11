#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: 2_create_latex_rosters.py
# STEP 2: Create LaTeX photo roster sheets from CSV files
# Reads from: seasons/YYYY-YY/output/csv/
# Outputs to: seasons/YYYY-YY/output/rosters_latex/ and rosters_pdf/
#
import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for paths
PDFLATEX_PATH = '/Library/TeX/texbin/pdflatex'


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


def get_project_root():
    """Get the root of the project."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(current_dir, 'bin')):
        current_dir = os.path.dirname(current_dir)
    return current_dir

def get_csv_dir_and_template(args):
    """Parse command line arguments to get the CSV directory and optional template file."""
    project_root = get_project_root()
    templates_dir = os.path.join(project_root, 'templates')
    
    if len(args) < 2:
        raise ValueError('Please provide the CSV subdirectory name (e.g., "csv" or "super-8-csv") as a command line argument.')
    
    # Determine season
    season = get_season_year()
    for arg in args[1:]:
        if arg.startswith('20') and '-' in arg:  # Season format like 2025-26
            season = arg
            break
    
    # Determine CSV directory
    csv_subdir = args[1] if not args[1].startswith('20') else 'csv'
    seasons_dir = os.path.join(project_root, 'seasons', season, 'output')
    csv_dir = os.path.join(seasons_dir, csv_subdir)
    
    # Determine template file
    template_file = os.path.join(templates_dir, 'RosterTemplate.tex')  # Default template
    for arg in args:
        if arg.endswith('.tex'):
            template_file = os.path.join(templates_dir, arg)

    return os.path.abspath(csv_dir), template_file, season


def check_dependencies(pdflatex_path, template_file):
    """Check if pdflatex and the template file exist."""
    if not os.path.exists(pdflatex_path):
        raise FileNotFoundError(f'pdflatex not found at {pdflatex_path}. Please install it and try again.')
    
    if not os.path.exists(template_file):
        raise FileNotFoundError(f'Template file {template_file} not found. Please create it or pass the correct path.')


def create_latex_directory(season, latex_subdir='rosters_latex'):
    """Create the LaTeX output directory if it doesn't exist."""
    root_dir = get_project_root()
    latex_dir = os.path.join(root_dir, 'seasons', season, 'output', latex_subdir)
    if not os.path.exists(latex_dir):
        os.makedirs(latex_dir)
    return latex_dir

def create_pdf_directory(season, pdf_subdir='rosters_pdf'):
    """Create the PDF output directory if it doesn't exist."""
    root_dir = get_project_root()
    pdf_dir = os.path.join(root_dir, 'seasons', season, 'output', pdf_subdir)
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    return pdf_dir


def process_csv_files(csv_dir, template_file, latex_dir):
    """Create LaTeX files for each CSV file by using the template."""
    for csv_file in os.listdir(csv_dir):
        if csv_file.endswith('.csv'):
            csv_file_path = os.path.join(csv_dir, csv_file)
            output_file_path = os.path.join(latex_dir, csv_file.replace('.csv', '.tex'))

            create_latex_file_from_template(template_file, csv_file_path, output_file_path)


def create_latex_file_from_template(template_file, csv_file_path, output_file_path):
    """Generate a LaTeX file by replacing CSV_FILE placeholder in the template."""
    with open(template_file, 'r') as f:
        template_content = f.read()

    # Replace CSV_FILE in the template
    output_content = template_content.replace('CSV_FILE', csv_file_path)

    with open(output_file_path, 'w') as f:
        f.write(output_content)
    
    logging.info(f'Created LaTeX file: {output_file_path}')


def compile_latex_files(latex_dir, pdf_dir, pdflatex_path):
    """Run pdflatex command to compile LaTeX files into PDFs."""
    for tex_file in os.listdir(latex_dir):
        if tex_file.endswith('.tex'):
            tex_file_path = os.path.join(latex_dir, tex_file)
            compile_latex_file(tex_file_path, pdf_dir, pdflatex_path)


def compile_latex_file(tex_file_path, pdf_dir, pdflatex_path):
    """Compile a single LaTeX file using pdflatex."""
    logging.info(f'Compiling LaTeX file: {tex_file_path}')
    result = subprocess.run(
        [pdflatex_path, '-output-directory', pdf_dir, tex_file_path],
        stdout=open('latex_logfile.log', 'a'),
        stderr=subprocess.STDOUT
    )
    if result.returncode != 0:
        logging.error(f'Error compiling {tex_file_path}, check latex_logfile.log for details.')


def cleanup_auxiliary_tex_files(pdf_dir):
    """Remove auxiliary LaTeX files after compilation."""
    for file in os.listdir(pdf_dir):
        if file.endswith('.log') or file.endswith('.aux'):
            os.remove(os.path.join(pdf_dir, file))

def main(args):
    try:
        csv_dir, template_file, season = get_csv_dir_and_template(args)
        check_dependencies(PDFLATEX_PATH, template_file)

        latex_dir = create_latex_directory(season)
        pdf_dir = create_pdf_directory(season)

        logging.info(f'Season: {season}')
        logging.info(f'Processing CSV directory: {csv_dir}')
        process_csv_files(csv_dir, template_file, latex_dir)

        logging.info(f'Compiling LaTeX files to PDFs')
        logging.info(f'LaTeX source: {latex_dir}')
        logging.info(f'PDF output: {pdf_dir}')
        compile_latex_files(latex_dir, pdf_dir, PDFLATEX_PATH)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

    cleanup_auxiliary_tex_files(pdf_dir)
    logging.info('Finished creating PDF rosters.')
    logging.info(f'PDF files saved to: {pdf_dir}')
    

if __name__ == "__main__":
    main(sys.argv)
