# Hockey Photo Day Management System

Automated workflow tools for managing team photo days at hockey organizations. This system processes roster data, generates photo sheets, creates scheduling materials, and prepares data for Memory Mate production.

## 🎯 What This Does

This toolkit automates the complete photo day workflow:
1. **Extract rosters** from Excel spreadsheets
2. **Generate photo sheets** with player names and numbers  
3. **Create envelope labels** with photo schedules
4. **Verify player counts** for billing and quality control
5. **Prepare Memory Mate data** for Photoshop automation

## 🚀 Quick Start

### Prerequisites

* **Python 3.9+**
* **LaTeX** (pdflatex) - Install via: `brew install --cask mactex`
* **Python packages**: `pip install -r Requirements.txt`

### Basic Usage

1. **Place your roster Excel file** in `seasons/2025-26/input/rosters.xlsx`
2. **Run the workflow** (see [WORKFLOW.md](WORKFLOW.md) for detailed steps)
3. **Collect outputs** from `seasons/2025-26/output/`

## 📁 Project Structure

```
latex-rosters/
├── WORKFLOW.md              # 📖 Complete step-by-step guide (START HERE!)
├── README.md                # This file
├── Requirements.txt         # Python dependencies
│
├── bin/                     # Executable scripts
│   ├── 1_export_csv_from_excel.py    # Extract rosters from Excel
│   ├── 2_create_latex_rosters.py     # Generate photo sheets
│   ├── 3_create_envelopes.py         # Create envelope labels
│   ├── count_players.py              # Verify player counts
│   └── create_mm_csv_data.py         # Memory Mate data prep
│
├── templates/               # LaTeX templates (customizable)
│   └── RosterTemplate.tex
│
├── config/                  # Configuration templates
│   └── photo_schedule_template.csv
│
├── examples/                # Sample files for reference
│   ├── input/
│   └── output/
│
└── seasons/                 # Your data (NOT in git)
    └── 2025-26/
        ├── input/           # Original rosters & schedules
        └── output/          # Generated files
```

## 📚 Documentation

* **[QUICKREF.md](QUICKREF.md)** ⭐ **START HERE!** - One-page cheat sheet for daily use
* **[WORKFLOW.md](WORKFLOW.md)** - Complete annual process guide
* **[WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md)** - Visual workflow diagram
* **[MIGRATION.md](MIGRATION.md)** - Guide for transitioning from old structure
* **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Summary of recent restructuring
* **[Examples Directory](Examples/)** - Sample inputs and outputs
* **Script Help** - Run any script with `--help` flag for usage info

## 🔧 Core Scripts

### 1. Export CSV from Excel
```bash
python3 bin/1_export_csv_from_excel.py seasons/2025-26/input/rosters.xlsx
```
Converts Excel workbook (one sheet per team) into individual CSV files.

### 2. Create Photo Roster Sheets
```bash
python3 bin/2_create_latex_rosters.py csv
```
Generates formatted LaTeX/PDF photo sheets for tracking players on photo day.

### 3. Count Players
```bash
python3 bin/count_players.py seasons/2025-26/output/csv
```
Creates player count report for billing and verification.

### 4. Create Memory Mate Data
```bash
python3 bin/create_mm_csv_data.py "Team Name" roster.csv photos/
```
Prepares CSV data for Photoshop Memory Mate automation.

## 🧪 Testing

Run the test suite:
```bash
pytest -v
```

Or use the validation script:
```bash
./bin/validate_tests.sh
```

**Test Coverage:** 42 comprehensive tests across all core scripts

Tests verify:
- CSV export functionality
- LaTeX generation
- File handling and data processing
- Player counting and reporting
- Memory Mate data preparation

See [TEST_COVERAGE.md](TEST_COVERAGE.md) for detailed coverage report.

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/stoney27/latex-rosters.git
   cd latex-rosters
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r Requirements.txt
   ```

3. **Install LaTeX** (if not already installed)
   ```bash
   brew install --cask mactex  # macOS
   ```

4. **Create season directory**
   ```bash
   mkdir -p seasons/2025-26/{input,output/{csv,rosters_latex,rosters_pdf,envelopes_latex,envelopes_pdf,reports}}
   ```

## 🎓 Examples

See the `Examples/` directory for:
- Sample roster CSV files
- Generated LaTeX files
- Final PDF outputs

## 🤝 Contributing

This is a specialized tool for annual photo day management. Feel free to fork and adapt for your organization's needs.

## 📄 License

See [LICENSE](LICENSE) file for details.

## 💡 Tips

- **Always backup** your original Excel roster file
- **Test early** - run Steps 1-2 when you receive rosters to catch issues
- **Season organization** - Use `YYYY-YY` format for season directories
- **Git clean** - All generated files are automatically excluded from version control

---

**Need help?** Check [WORKFLOW.md](WORKFLOW.md) for the complete step-by-step guide.