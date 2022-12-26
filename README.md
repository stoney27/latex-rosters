# LaTeX Rosters creatioin script

This script is used to create a LaTeX roster for a given CVS files.  It will create one roster for each CVS file in the given roster directory.  It will then porcess the LateX files and create a PDF file for each roster.  These PDF files can then be printed and used for photos.

## Usage

    ./create_rosters.sh roster_dir

## Output

In a latex directory there will be a tex file for each roster file in the roster directory.  There will also be a PDF file for each roster file in the roster directory.

## Requirements

* Python 3 installed
* TeXLive installed
* Path for pdflatex installed if not in the default path
* Individual roster files in CVS format the roster directory
* Roster files must include, First Name, Last Name, Sweater Number, and Team Name

## License

This script is licensed under the MIT license.  See the LICENSE file for more information.
