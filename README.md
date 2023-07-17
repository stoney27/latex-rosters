# Python Excel to CSV and LaTeX PDF Roster Scripts

This repository contains two Python scripts:

1. `export_csv_from_excel.py`: This script takes an Excel file as input and exports each sheet as a CSV file.
2. `csv_to_latex_pdf.py`: This script creates LaTeX files from a given CSV file directory and a LaTeX template file, and then processes them into PDF files.

## export_csv_from_excel.py

This script reads an Excel file, cleaning and exporting each sheet to a CSV file. 

### Requirements

* Python 3.9
* openpyxl, CSV

### Usage

To run the script, use the following command:

```bash
python3.9 export_csv_from_excel.py <filename> [--by-team]
```
    <filename>: Name of the Excel file to export.
    --by-team: Optional flag. If set, the script will export by team. Otherwise, it will export by workbook.

The script will create a csv directory in the current working directory, where it will save the generated CSV files. It prints the total player count after processing all workbooks.

There will also be a PDF file for each roster file in the roster directory.

Find example of the CSV file in the Example directory.

* [CSV file -- 12U_black.csv](./Examples/csv/12U_Black.csv)

* [LaTeX file -- 12U_black.tex](./Examples/latex/12U_Black.tex)

* [PDF file -- 12U_black.pdf](./Examples/latex/12U_Black.pdf)

## csv_to_latex_pdf.py
This script creates LaTeX files from a given CSV file directory and a LaTeX template file, then processes them into PDF files.

### Requirements
* Python 3.9
* LaTeX (pdflatex)

### Usage
To run the script, use the following command:

```bash
Copy code
python3 csv_to_latex_pdf.py <csv_dir> [template_file.tex]
```

    <csv_dir>: Path to the directory that contains the CSV files.
    template_file.tex: Optional LaTeX template file. If not provided, the script will use RosterTemplate.tex by default.

The script will create a latex directory in the current working directory, where it will save the generated LaTeX and PDF files.

Installation of Dependencies
To install the dependencies, you need to have Python installed on your system. If you don't, you can download it from the official Python website.

Once Python is installed, you can install the openpyxl library using pip:

pip install openpyxl

LaTeX needs to be installed separately. You can download it from the official LaTeX Project website.