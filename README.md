# LaTeX Rosters creation script

This script creates a LaTeX roster for a given CVS file.  It will make one roster for each CVS file in the given roster directory.  It will then process the LateX files and create a PDF file for each roster.  These PDF files can then be printed and used for photos.

## Create Rosters Usage

    ./create_rosters.sh roster_dir <LaTeX template file>
    The path to the LaTeX template file is optional.  If not given, the default template file will be used.

### Rosters Output

In a latex directory, there will be a tex file for each roster file in the roster directory.  There will also be a PDF file for each roster file in the roster directory.

Find example of the CSV file in the Example directory.

* [CSV file](./Examples/csv_files/12U_AAA.csv)

* [LaTeX file](./Examples/latex/12U_AAA.tex)

* [PDF file](./Examples/latex/12U_AAA.pdf)

## Create CSV Files Usage

    ./create_csv_from_excel.py excel_file

### CSV Output

In a CSV directory, there will be a CSV file for each roster for each sheet in the excel file.

## Requirements

* Python 3 installed
* Python 3 modules installed: CSV, openpyxl
* TeXLive installed
* Path for pdflatex installed if not in the default path
* Individual roster files in CVS format in the roster directory
* Roster files must include, First Name, Last Name, Sweater Number, and Team Name

## License

This script is licensed under the MIT license.  See the LICENSE file for more information.
