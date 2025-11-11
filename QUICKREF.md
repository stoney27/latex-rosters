# Quick Reference Guide

## 🎯 One-Page Workflow Cheat Sheet

### Pre-Photo Day (2-3 weeks before)

```bash
# STEP 1: Export rosters from Excel
python3 bin/1_export_csv_from_excel.py seasons/2025-26/input/rosters.xlsx

# STEP 2: Generate photo roster sheets
python3 bin/2_create_latex_rosters.py csv

# STEP 3: Verify player counts
python3 bin/count_players.py seasons/2025-26/output/csv

# STEP 4: Print roster sheets
open seasons/2025-26/output/rosters_pdf/
```

### Photo Schedule Setup

1. Copy template: `config/photo_schedule_template.csv`
2. Fill in team names and times
3. Save as: `seasons/2025-26/input/photo_schedule.csv`
4. Generate envelopes (manual process for now)

### Post-Photo Day

```bash
# Create Memory Mate data for each team
python3 bin/create_mm_csv_data.py "12U Black" \
    seasons/2025-26/output/csv/12U_Black.csv \
    seasons/2025-26/photos/12U_Black/
```

---

## 📂 Key File Locations

| What | Where |
|------|-------|
| Original Excel roster | `seasons/2025-26/input/rosters.xlsx` |
| Photo schedule | `seasons/2025-26/input/photo_schedule.csv` |
| Team CSV files | `seasons/2025-26/output/csv/` |
| Photo roster PDFs | `seasons/2025-26/output/rosters_pdf/` |
| Player count report | `seasons/2025-26/output/reports/player_count.csv` |
| Memory Mate data | `seasons/2025-26/output/reports/*_mm.csv` |

---

## 🔧 Script Quick Help

### 1_export_csv_from_excel.py
```bash
# Basic usage
python3 bin/1_export_csv_from_excel.py seasons/2025-26/input/rosters.xlsx

# Export by team (separate CSV per team from single sheet)
python3 bin/1_export_csv_from_excel.py rosters.xlsx --by-team

# Specify season manually
python3 bin/1_export_csv_from_excel.py rosters.xlsx --season 2025-26
```

### 2_create_latex_rosters.py
```bash
# Default: uses csv/ subdirectory
python3 bin/2_create_latex_rosters.py csv

# For Super 8 teams (different subdirectory)
python3 bin/2_create_latex_rosters.py super-8-csv

# Custom template
python3 bin/2_create_latex_rosters.py csv CustomTemplate.tex

# Specify season
python3 bin/2_create_latex_rosters.py csv 2025-26
```

### count_players.py
```bash
# Generate player count report
python3 bin/count_players.py seasons/2025-26/output/csv
```

### create_mm_csv_data.py
```bash
# Create Memory Mate CSV (quotes if team name has spaces)
python3 bin/create_mm_csv_data.py "Team Name" roster.csv photos_dir/
```

---

## 🚨 Common Issues

| Problem | Solution |
|---------|----------|
| `pdflatex not found` | `brew install --cask mactex` |
| `Directory not found` | Run commands from project root |
| `CSV files not found` | Check Step 1 completed successfully |
| Wrong player count | Verify no empty rows in Excel |
| Script uses old paths | Use numbered scripts (`1_`, `2_`) not old ones |

---

## 📋 Print Checklist

Photo Week To-Do:
- [ ] Roster sheets printed (from `rosters_pdf/`)
- [ ] Envelope labels printed and cut
- [ ] Envelopes stuffed with labels
- [ ] Extra blank roster sheets (2-3)
- [ ] Player count matches organization records
- [ ] Photo schedule confirmed with organization

---

## 💾 Backup Strategy

Before photo day:
```bash
# Backup entire season directory
cp -r seasons/2025-26 seasons/2025-26_backup_$(date +%Y%m%d)

# Or just backup to external drive
rsync -av seasons/2025-26/ /path/to/backup/2025-26/
```

---

## 🆕 New Season Setup

```bash
# Create structure for next season
mkdir -p seasons/2026-27/{input,output/{csv,rosters_latex,rosters_pdf,envelopes_latex,envelopes_pdf,reports}}

# Or use the automated script (auto-detects season from date)
python3 bin/1_export_csv_from_excel.py seasons/2026-27/input/rosters.xlsx
```

---

## 📖 Full Documentation

- `README.md` - Complete project overview
- `WORKFLOW.md` - Detailed step-by-step guide
- `MIGRATION.md` - Transitioning from old structure
- `Examples/` - Sample files

---

## ⌨️ Keyboard Shortcuts (macOS)

| Task | Shortcut |
|------|----------|
| Open Terminal | `Cmd + Space`, type "Terminal" |
| Navigate to project | `cd ~/src/latex-rosters` |
| List files | `ls -la` |
| View PDF | `open file.pdf` |
| Open directory in Finder | `open .` |
