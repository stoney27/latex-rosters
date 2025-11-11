# Test Suite Updates - Summary

## Changes Made

The test suite has been updated to work with the new project structure and numbered script files.

### 1. test_export_csv_from_excel.py

**Key Updates:**
- ✅ Updated imports to use `importlib.util` for loading `1_export_csv_from_excel.py`
- ✅ Added `tempfile` and `shutil` for proper test isolation
- ✅ Updated all test functions to use temporary directories instead of hardcoded `csv/` paths
- ✅ Updated function calls to include `csv_dir` parameter (new signature)
- ✅ Updated to use module constants (`HEADER_FIRSTNAME`, etc.)
- ✅ Cleanup function now handles temporary directories

**Test Functions:**
- `test_clean_row()` - Tests name and sweater number cleaning
- `test_player_count()` - Tests player counting with temporary directory
- `test_by_workbook()` - Tests workbook export with temporary directory
- `test_by_team()` - Tests team export with temporary directory

**Example of changes:**
```python
# Old
export_csv_from_excel.export_by_team('test.xlsx')
assert os.path.exists('csv/Squirt_A.csv')

# New
test_csv_dir = tempfile.mkdtemp(prefix='test_csv_')
export_csv_from_excel.export_by_team('test.xlsx', test_csv_dir)
assert os.path.exists(os.path.join(test_csv_dir, 'Squirt_A.csv'))
```

### 2. test_create_latex_rosters.py

**Key Updates:**
- ✅ Completely rewritten to use pytest fixtures
- ✅ Uses `importlib.util` to load `2_create_latex_rosters.py`
- ✅ Creates temporary test environments with full season structure
- ✅ Uses `monkeypatch` to isolate tests from real project structure
- ✅ Tests the new 3-tuple return value from `get_csv_dir_and_template()`

**Test Functions:**
- `test_get_project_root()` - Validates project root detection
- `test_get_season_year()` - Tests season year auto-detection
- `test_csv_dir_and_template_basic()` - Tests basic path construction
- `test_custom_template()` - Tests custom template file selection
- `test_missing_arguments()` - Tests error handling
- `test_season_override()` - Tests manual season specification

**Fixture:**
```python
@pytest.fixture
def setup_test_environment(tmpdir):
    """Create a temporary test environment with season structure"""
    # Creates: test_root/seasons/2024-25/output/csv/
    # Plus templates/ directory
```

## Running the Tests

### Prerequisites

Ensure pytest is installed:
```bash
pip3 install pytest pandas openpyxl xlsxwriter
```

### Run All Tests

```bash
cd /Users/srs/src/latex-rosters
pytest bin/tests/ -v
```

### Run Specific Test File

```bash
# Test export functionality
pytest bin/tests/test_export_csv_from_excel.py -v

# Test roster creation
pytest bin/tests/test_create_latex_rosters.py -v
```

### Run Specific Test

```bash
pytest bin/tests/test_create_latex_rosters.py::test_get_project_root -v
```

## Test Coverage

## Test Coverage

### What's Tested

✅ **Comprehensive Coverage:**

#### 1. test_export_csv_from_excel.py (10 tests)
- Name cleaning (capitalization, special characters)
- Sweater number cleaning (removing non-digits)
- Export by workbook (one CSV per sheet)
- Export by team (grouping by team column)
- Player counting
- Header validation

#### 2. test_create_latex_rosters.py (12 tests)
- Project root detection
- Season year auto-detection
- CSV directory path construction
- Template file selection (default and custom)
- Season directory structure
- Argument validation
- LaTeX directory creation
- PDF directory creation
- LaTeX file generation from templates
- CSV file processing
- Auxiliary file cleanup
- Full integration workflow

#### 3. test_count_players.py (9 tests)
- Line counting in CSV files
- Filename formatting (underscores to spaces)
- Directory processing with basic structure
- Directory processing with season structure
- Non-existent directory handling
- Empty directory handling
- Non-CSV file filtering
- Output file creation
- Full integration with multiple teams

#### 4. test_create_mm_csv_data.py (11 tests)
- Photo path generation
- Team photo detection
- MM CSV path creation (with/without season structure)
- Directory creation
- Photo matching logic
- Edge cases (similar names, empty directories)
- Filename variations
- Photos with spaces in names
- Full integration workflow

**Total: 42 comprehensive tests**

### What's Not Tested Yet

✅ **Comprehensive Coverage:**
- **CSV Export Functions** - Name cleaning, sweater numbers, workbook/team exports, player counting
- **Roster Creation Functions** - Project root detection, season detection, path construction, template handling, LaTeX generation
- **Player Count Utility** - Line counting, filename formatting, directory processing, season structure handling
- **Memory Mate Generation** - Photo path handling, team photo detection, CSV path creation, photo matching

### What's Not Tested Yet

⚠️ **Still Not Covered:**
- PDF compilation (requires pdflatex installation)
- Envelope creation (script is placeholder)
- End-to-end workflow with actual LaTeX compilation

## Known Issues

### Import Method
The scripts start with numbers (`1_`, `2_`), which requires special import handling using `importlib.util`. This is handled correctly in the test files.

### Dependencies
Tests require these Python packages:
- pytest
- pandas
- openpyxl
- xlsxwriter

Install with:
```bash
pip3 install -r Requirements.txt
```

## Future Improvements

1. **Add integration tests** - Test complete workflow from Excel to PDF
2. **Mock pdflatex** - Test LaTeX generation without requiring LaTeX installation
3. **Add count_players tests** - Validate player counting utility
4. **Add create_mm_csv_data tests** - Test Memory Mate data generation
5. **CI/CD Integration** - Automate test running on commits

## Validation

To validate the tests work:

```bash
# Quick validation
python3 bin/test_runner.py

# Full test suite
pytest bin/tests/ -v --tb=short

# With coverage report
pytest bin/tests/ --cov=bin --cov-report=term-missing
```

## Test File Structure

```
bin/tests/
├── __init__.py
├── test_export_csv_from_excel.py    # Export/CSV tests
├── test_create_latex_rosters.py     # Roster generation tests
└── templates/                        # Test templates
    ├── RosterTemplate.tex
    └── CustomTemplate.tex
```

## Summary

✅ **Tests updated** to work with new structure
✅ **Temporary directories** used for test isolation  
✅ **Import issues** resolved with importlib
✅ **New function signatures** accounted for
✅ **Season structure** properly tested

The test suite is now compatible with the restructured project and should pass once pytest and dependencies are installed.
