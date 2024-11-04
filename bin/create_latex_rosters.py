#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for paths
PDFLATEX_PATH = '/Library/TeX/texbin/pdflatex'


def get_project_root():
    """Get the root of the project."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(current_dir, 'bin')):
        current_dir = os.path.dirname(current_dir)
    return current_dir

def get_csv_dir_and_template(args):
    """Parse command line arguments to get the CSV directory and optional template file."""
    project_root = get_project_root()
    data_dir = os.path.join(project_root, 'data')
    templates_dir = os.path.join(project_root, 'templates')
    
    if len(args) < 2:
        raise ValueError('Please provide the path to the CSV directory as a command line argument.')
    
    template_file = os.path.join(templates_dir, 'RosterTemplate.tex')  # Default template
    csv_dir = os.path.join(data_dir, args[1])

    if len(args) > 2:
        for arg in args:
            if arg.endswith('.tex'):
                template_file = os.path.join(templates_dir, arg)
            else:
                csv_dir = os.path.join(data_dir, arg)

    return os.path.abspath(csv_dir), template_file


def check_dependencies(pdflatex_path, template_file):
    """Check if pdflatex and the template file exist."""
    if not os.path.exists(pdflatex_path):
        raise FileNotFoundError(f'pdflatex not found at {pdflatex_path}. Please install it and try again.')
    
    if not os.path.exists(template_file):
        raise FileNotFoundError(f'Template file {template_file} not found. Please create it or pass the correct path.')


def create_latex_directory(latex_dir='output/latex'):
    """Create the LaTeX output directory if it doesn't exist."""
    root_dir = get_project_root()
    latex_dir = os.path.join(root_dir, latex_dir)
    if not os.path.exists(latex_dir):
        os.makedirs(latex_dir)
    return latex_dir


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


def compile_latex_files(latex_dir, pdflatex_path):
    """Run pdflatex command to compile LaTeX files into PDFs."""
    for tex_file in os.listdir(latex_dir):
        if tex_file.endswith('.tex'):
            tex_file_path = os.path.join(latex_dir, tex_file)
            compile_latex_file(tex_file_path, latex_dir, pdflatex_path)


def compile_latex_file(tex_file_path, latex_dir, pdflatex_path):
    """Compile a single LaTeX file using pdflatex."""
    logging.info(f'Compiling LaTeX file: {tex_file_path}')
    result = subprocess.run(
        [pdflatex_path, '-output-directory', latex_dir, tex_file_path],
        stdout=open('latex_logfile.log', 'a'),
        stderr=subprocess.STDOUT
    )
    if result.returncode != 0:
        logging.error(f'Error compiling {tex_file_path}, check latex_logfile.log for details.')


def cleanup_auxiliary_tex_files(latex_dir):
    """Remove LaTeX files after compilation."""
    for file in os.listdir(latex_dir):
        if file.endswith('.log') or file.endswith('.aux'):
            os.remove(os.path.join(latex_dir, file))

def main(args):
    try:
        csv_dir, template_file = get_csv_dir_and_template(args)
        check_dependencies(PDFLATEX_PATH, template_file)

        latex_dir = create_latex_directory()

        logging.info(f'Processing CSV directory: {csv_dir}')
        process_csv_files(csv_dir, template_file, latex_dir)

        logging.info(f'Compiling LaTeX files in directory: {latex_dir}')
        compile_latex_files(latex_dir, PDFLATEX_PATH)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

    cleanup_auxiliary_tex_files(latex_dir)
    logging.info('Finished creating PDF rosters.')
    

if __name__ == "__main__":
    main(sys.argv)
