# Hockey Photo Day Workflow Guide

This guide walks you through the complete annual process for organizing team photos, from receiving roster data to distributing photo day materials.

## 📅 Annual Timeline Overview

```
Week 1-2:   Receive roster data → Generate photo sheets
Week 3-4:   Create photo schedule → Generate envelope labels
Photo Week: Print & distribute materials → Take photos
Post-Photo: Verify player counts → Create Memory Mates
```

---

## 🔄 Complete Workflow

### **STEP 1: Receive and Process Roster Data**

**Input:** Excel spreadsheet with all team rosters (one sheet per team)

**Action:**
```bash
cd /Users/srs/src/latex-rosters
python3 bin/1_export_csv_from_excel.py seasons/2025-26/input/rosters.xlsx
```

**Output:** Individual CSV files for each team in `seasons/2025-26/output/csv/`

**What it does:**
- Reads the Excel workbook
- Exports each sheet as a separate CSV file
- Names files based on sheet names (e.g., `12U_Black.csv`)
- Cleans and formats player data

---

### **STEP 2: Generate Photo Roster Sheets**

**Input:** CSV files from Step 1

**Action:**
```bash
python3 bin/2_create_latex_rosters.py csv
```

**Output:** 
- LaTeX files in `seasons/2025-26/output/rosters_latex/`
- PDF files in `seasons/2025-26/output/rosters_pdf/`

**What it does:**
- Reads all CSV files from the csv directory
- Generates formatted LaTeX documents with player names and numbers
- Compiles LaTeX to PDF using pdflatex
- Creates one photo sheet per team

**Purpose:** These sheets are used during photo day to track which players have been photographed.

---

### **STEP 3: Create Photo Schedule**

**Input:** Manual - you create this based on photo day logistics

**Action:**
1. Copy the template: `config/photo_schedule_template.csv`
2. Fill in team names and photo times
3. Save as: `seasons/2025-26/input/photo_schedule.csv`

**Format:**
```csv
Team Name,Individual Photo Time,Group Photo Time
12U Black,9:00 AM,9:30 AM
12U Red,9:45 AM,10:15 AM
```

---

### **STEP 4: Generate Envelope Labels**

**Input:** Photo schedule CSV from Step 3

**Action:**
```bash
python3 bin/3_create_envelopes.py seasons/2025-26/input/photo_schedule.csv
```

**Output:**
- LaTeX file: `seasons/2025-26/output/envelopes_latex/Team_Envelopes.tex`
- PDF file: `seasons/2025-26/output/envelopes_pdf/Team_Envelopes.pdf`

**What it does:**
- Reads the photo schedule
- Generates formatted envelope labels with team names and photo times
- Creates printable PDF for envelope stuffing

**Purpose:** Print these labels, cut them out, and place them in envelopes for distribution to coaches.

---

### **STEP 5: Verify Player Count (Quality Check)**

**Input:** CSV files from Step 1

**Action:**
```bash
python3 bin/count_players.py seasons/2025-26/output/csv
```

**Output:** `seasons/2025-26/output/reports/player_count.csv`

**What it does:**
- Counts players on each team
- Generates summary report with team names and player counts
- Helps verify all players are accounted for in photo management software

**Purpose:**
- ✅ Double-check player counts before photo day
- 💰 Use for billing the organization (per-player pricing)
- 🔍 Verify data accuracy

---

### **STEP 6: Create Memory Mates Data (Post-Photos)**

**Input:** 
- CSV roster file (e.g., `seasons/2025-26/output/csv/12U_Black.csv`)
- Directory with individual player photos
- Team name

**Action:**
```bash
python3 bin/create_mm_csv_data.py "12U Black" \
    seasons/2025-26/output/csv/12U_Black.csv \
    seasons/2025-26/photos/12U_Black/
```

**Output:** `seasons/2025-26/output/reports/12U_Black_mm.csv`

**What it does:**
- Reads player roster
- Maps player names to photo filenames
- Includes team photo path
- Generates CSV for Photoshop data merge

**Purpose:** Automate Memory Mate creation in Photoshop using data merge feature.

---

## 📁 File Organization by Season

All generated files are organized by season to keep historical records:

```
seasons/2025-26/
├── input/
│   ├── rosters.xlsx              # Original Excel from organization
│   └── photo_schedule.csv        # Your photo timing schedule
│
├── output/
│   ├── csv/                      # Extracted team rosters
│   ├── rosters_latex/            # LaTeX source for photo sheets
│   ├── rosters_pdf/              # Final printable photo sheets
│   ├── envelopes_latex/          # LaTeX source for envelopes
│   ├── envelopes_pdf/            # Final printable envelopes
│   └── reports/
│       ├── player_count.csv      # Team counts for billing
│       └── *_mm.csv              # Memory Mate data files
│
└── photos/                       # Actual photos (typically external)
    └── [Team Name]/
        ├── Team Photo.jpg
        ├── player1.jpg
        └── player2.jpg
```

---

## 🎯 Quick Reference: Photo Week Checklist

- [ ] Step 1: Export rosters from Excel to CSV
- [ ] Step 2: Generate photo roster sheets (PDF)
- [ ] Step 3: Create photo schedule CSV
- [ ] Step 4: Generate envelope labels (PDF)
- [ ] Step 5: Run player count verification
- [ ] **Print** roster sheets and envelope labels
- [ ] **Cut** envelope labels
- [ ] **Stuff** envelopes with labels
- [ ] **Distribute** envelopes to coaches
- [ ] 📸 **Photo Day!**
- [ ] Step 6: Generate Memory Mate data (per team)
- [ ] Create Memory Mates in Photoshop
- [ ] Deliver final products

---

## 🔧 Troubleshooting

### "pdflatex not found"
LaTeX is not installed. Install MacTeX:
```bash
brew install --cask mactex
```

### "Template file not found"
Ensure you're running scripts from the project root directory.

### Wrong player count
- Check for empty rows in Excel
- Verify CSV export completed successfully
- Compare with organization's official roster

### Script can't find CSV files
Verify the season directory structure exists and CSV files are in the correct location.

---

## 💡 Tips for Success

1. **Backup Original Excel:** Always keep a copy of the original roster file
2. **Test Early:** Run Steps 1-2 as soon as you receive rosters to catch issues
3. **Print Extra Sheets:** Always print 2-3 extra roster sheets for backups
4. **Label Envelopes Clearly:** Include team name and level on envelope exterior
5. **Season Naming:** Use `YYYY-YY` format (e.g., `2025-26`) for consistency

---

## 📞 Support

For issues or questions, refer to:
- `README.md` for technical setup
- `examples/` directory for sample files
- Script help: `python3 bin/[script_name].py --help`
