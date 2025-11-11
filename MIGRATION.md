# Migration Guide: Transitioning to New Project Structure

This guide helps you migrate from the old data structure to the new season-based organization.

## What Changed?

### Old Structure
```
data/
  csv/              # All CSV files mixed together
output/
  latex/            # LaTeX and PDF files in same directory
```

### New Structure
```
seasons/
  2025-26/
    input/          # Original files from organization
    output/
      csv/          # Extracted rosters
      rosters_latex/  # LaTeX source
      rosters_pdf/    # Final PDFs
      reports/      # Player counts, MM data
```

## Migration Steps

### Step 1: Move Existing Data (Optional)

If you have existing data in `data/csv/` that you want to preserve:

```bash
# Create the season directory if it doesn't exist
mkdir -p seasons/2025-26/output/csv

# Move existing CSV files
mv data/csv/*.csv seasons/2025-26/output/csv/

# Move existing output files (if any)
mkdir -p seasons/2025-26/output/{rosters_latex,rosters_pdf}
mv output/latex/*.tex seasons/2025-26/output/rosters_latex/ 2>/dev/null || true
mv output/latex/*.pdf seasons/2025-26/output/rosters_pdf/ 2>/dev/null || true
```

### Step 2: Update Your Workflow

#### Old Way
```bash
python3.9 export_csv_from_excel.py rosters.xlsx
python3 create_latex_rosters.py csv
python3 count_players.py data/csv
```

#### New Way
```bash
python3 bin/1_export_csv_from_excel.py seasons/2025-26/input/rosters.xlsx
python3 bin/2_create_latex_rosters.py csv
python3 bin/count_players.py seasons/2025-26/output/csv
```

### Step 3: Script Naming

The scripts now have numbered prefixes to clarify the workflow order:

| Old Name | New Name | Purpose |
|----------|----------|---------|
| `export_csv_from_excel.py` | `1_export_csv_from_excel.py` | Extract rosters from Excel |
| `create_latex_rosters.py` | `2_create_latex_rosters.py` | Generate photo sheets |
| N/A | `3_create_envelopes.py` | Create envelope labels (placeholder) |
| `count_players.py` | `count_players.py` | Count players (utility) |
| `create_mm_csv_data.py` | `create_mm_csv_data.py` | Memory Mates data (utility) |

**Note:** The old scripts still exist and work with the old structure. You can delete them once you've verified the new scripts work correctly.

## Testing the New Structure

### Test with Example Data

1. **Place your Excel file:**
   ```bash
   cp your_rosters.xlsx seasons/2025-26/input/rosters.xlsx
   ```

2. **Run Step 1 (Export CSV):**
   ```bash
   python3 bin/1_export_csv_from_excel.py seasons/2025-26/input/rosters.xlsx
   ```
   
   **Expected output:** CSV files in `seasons/2025-26/output/csv/`

3. **Run Step 2 (Create Rosters):**
   ```bash
   python3 bin/2_create_latex_rosters.py csv
   ```
   
   **Expected output:** 
   - LaTeX files in `seasons/2025-26/output/rosters_latex/`
   - PDF files in `seasons/2025-26/output/rosters_pdf/`

4. **Run Player Count (Verification):**
   ```bash
   python3 bin/count_players.py seasons/2025-26/output/csv
   ```
   
   **Expected output:** `seasons/2025-26/output/reports/player_count.csv`

## Benefits of New Structure

✅ **Organization**: Each season's data is self-contained
✅ **History**: Keep previous seasons for reference
✅ **Clean Git**: Generated files never committed
✅ **Clear Workflow**: Numbered scripts show execution order
✅ **Scalability**: Easy to add new seasons each year

## Cleaning Up Old Files (Optional)

After verifying the new structure works:

```bash
# Remove old data directories (after backing up!)
rm -rf data/csv/
rm -rf output/

# Keep these directories as they're still referenced:
# - Examples/  (documentation)
# - envelops/  (manual envelope process)
```

## Future Seasons

For the 2026-27 season:

```bash
# Create new season structure
mkdir -p seasons/2026-27/{input,output/{csv,rosters_latex,rosters_pdf,envelopes_latex,envelopes_pdf,reports}}

# Place new roster file
cp new_rosters.xlsx seasons/2026-27/input/rosters.xlsx

# Run the same workflow with new season
python3 bin/1_export_csv_from_excel.py seasons/2026-27/input/rosters.xlsx --season 2026-27
```

Or let auto-detection handle it (scripts detect current season from date).

## Troubleshooting

### "Directory not found" errors
- Make sure you're running commands from the project root
- Check that `seasons/2025-26/` exists
- Verify input files are in the correct location

### Scripts still using old paths
- Make sure you're using the NEW numbered scripts (`1_`, `2_`, etc.)
- Old scripts (`export_csv_from_excel.py`, `create_latex_rosters.py`) use old paths

### Can't find CSV files
- Check `seasons/2025-26/output/csv/` not `data/csv/`
- Ensure Step 1 completed successfully before Step 2

## Questions?

Refer to:
- `README.md` - Project overview and quick start
- `WORKFLOW.md` - Detailed step-by-step annual process
- `Examples/` - Sample input/output files
