# Visual Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HOCKEY PHOTO DAY WORKFLOW                        │
│                         Annual Process                              │
└─────────────────────────────────────────────────────────────────────┘

Week 1-2: Data Preparation
╔═══════════════════════════════════════════════════════════════════╗
║  📥 INPUT: rosters.xlsx                                           ║
║     Organization sends Excel file with all team rosters           ║
╚═══════════════════════════════════════════════════════════════════╝
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: Export CSV from Excel                                      │
│  📝 Script: bin/1_export_csv_from_excel.py                          │
│                                                                     │
│  Command:                                                           │
│  $ python3 bin/1_export_csv_from_excel.py \                        │
│      seasons/2025-26/input/rosters.xlsx                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
╔═══════════════════════════════════════════════════════════════════╗
║  📁 OUTPUT: seasons/2025-26/output/csv/                           ║
║     ├── 12U_Black.csv                                             ║
║     ├── 12U_Red.csv                                               ║
║     ├── 13U_AAA.csv                                               ║
║     └── ... (one file per team)                                   ║
╚═══════════════════════════════════════════════════════════════════╝
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: Generate Photo Roster Sheets                              │
│  📄 Script: bin/2_create_latex_rosters.py                           │
│                                                                     │
│  Command:                                                           │
│  $ python3 bin/2_create_latex_rosters.py csv                       │
│                                                                     │
│  (Reads CSVs, creates LaTeX, compiles to PDF)                      │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
╔═══════════════════════════════════════════════════════════════════╗
║  📁 OUTPUT: seasons/2025-26/output/                               ║
║     ├── rosters_latex/                                            ║
║     │   ├── 12U_Black.tex                                         ║
║     │   └── ...                                                   ║
║     └── rosters_pdf/  ⭐ PRINT THESE                              ║
║         ├── 12U_Black.pdf                                         ║
║         └── ...                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  VERIFICATION: Count Players                                        │
│  🔢 Script: bin/count_players.py                                    │
│                                                                     │
│  Command:                                                           │
│  $ python3 bin/count_players.py seasons/2025-26/output/csv         │
│                                                                     │
│  (Quality check + billing data)                                    │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
╔═══════════════════════════════════════════════════════════════════╗
║  📁 OUTPUT: seasons/2025-26/output/reports/                       ║
║     └── player_count.csv                                          ║
║         (Team names + player counts for billing)                  ║
╚═══════════════════════════════════════════════════════════════════╝

Week 3-4: Photo Schedule & Logistics
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: Create Photo Schedule                                     │
│  📅 Manual Task                                                     │
│                                                                     │
│  1. Copy: config/photo_schedule_template.csv                       │
│  2. Fill in team names and photo times                             │
│  3. Save as: seasons/2025-26/input/photo_schedule.csv              │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4: Generate Envelope Labels                                  │
│  ✉️  Script: bin/3_create_envelopes.py (TODO)                      │
│                                                                     │
│  Currently: Manual process using envelops/ directory               │
│  Future: Automated script will read photo_schedule.csv             │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
╔═══════════════════════════════════════════════════════════════════╗
║  📁 OUTPUT: seasons/2025-26/output/                               ║
║     ├── envelopes_latex/                                          ║
║     │   └── Team_Envelopes.tex                                    ║
║     └── envelopes_pdf/  ⭐ PRINT & CUT THESE                      ║
║         └── Team_Envelopes.pdf                                    ║
╚═══════════════════════════════════════════════════════════════════╝

Photo Week: Print & Distribute
┌─────────────────────────────────────────────────────────────────────┐
│  📋 CHECKLIST                                                       │
│  ☐ Print roster sheets (from rosters_pdf/)                         │
│  ☐ Print envelope labels (from envelopes_pdf/)                     │
│  ☐ Cut envelope labels                                             │
│  ☐ Stuff envelopes with schedules                                  │
│  ☐ Distribute envelopes to coaches                                 │
│  ☐ Bring extra blank roster sheets                                 │
│                                                                     │
│  📸 PHOTO DAY! 🏒                                                   │
└─────────────────────────────────────────────────────────────────────┘

Post-Photo: Memory Mates Creation
╔═══════════════════════════════════════════════════════════════════╗
║  📥 INPUT: seasons/2025-26/photos/                                ║
║     └── [Team Name]/                                              ║
║         ├── Team Photo.jpg                                        ║
║         ├── player1.jpg                                           ║
║         └── player2.jpg                                           ║
╚═══════════════════════════════════════════════════════════════════╝
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 6: Create Memory Mate Data (per team)                        │
│  🖼️  Script: bin/create_mm_csv_data.py                             │
│                                                                     │
│  Command (run for each team):                                      │
│  $ python3 bin/create_mm_csv_data.py "12U Black" \                 │
│      seasons/2025-26/output/csv/12U_Black.csv \                    │
│      seasons/2025-26/photos/12U_Black/                             │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
╔═══════════════════════════════════════════════════════════════════╗
║  📁 OUTPUT: seasons/2025-26/output/reports/                       ║
║     ├── 12U_Black_mm.csv                                          ║
║     ├── 12U_Red_mm.csv                                            ║
║     └── ... (one per team)                                        ║
║                                                                   ║
║  Use these files in Photoshop data merge to automate              ║
║  Memory Mate creation!                                            ║
╚═══════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────┐
│  ✅ COMPLETE: Deliver final products to organization               │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════
                         FILE ORGANIZATION
═══════════════════════════════════════════════════════════════════════

seasons/2025-26/
├── input/                          ⬅️  YOU PUT FILES HERE
│   ├── rosters.xlsx                 (from organization)
│   └── photo_schedule.csv           (you create)
│
└── output/                         ➡️  GENERATED FILES HERE
    ├── csv/                          (roster data)
    │   ├── 12U_Black.csv
    │   └── ...
    │
    ├── rosters_latex/                (LaTeX source)
    │   ├── 12U_Black.tex
    │   └── ...
    │
    ├── rosters_pdf/                  ⭐ PRINT THESE
    │   ├── 12U_Black.pdf
    │   └── ...
    │
    ├── envelopes_latex/              (envelope source)
    │   └── Team_Envelopes.tex
    │
    ├── envelopes_pdf/                ⭐ PRINT THESE
    │   └── Team_Envelopes.pdf
    │
    └── reports/                      (verification & billing)
        ├── player_count.csv          (for billing)
        └── *_mm.csv                  (for Photoshop)


═══════════════════════════════════════════════════════════════════════
                         SCRIPT REFERENCE
═══════════════════════════════════════════════════════════════════════

Core Workflow (in order):
1️⃣  bin/1_export_csv_from_excel.py    Excel → CSV files
2️⃣  bin/2_create_latex_rosters.py     CSV → Photo roster PDFs
3️⃣  bin/3_create_envelopes.py         Schedule → Envelope labels

Utilities (use as needed):
🔢 bin/count_players.py               Verify counts & billing
🖼️  bin/create_mm_csv_data.py         Photoshop data prep


═══════════════════════════════════════════════════════════════════════
                         QUICK COMMANDS
═══════════════════════════════════════════════════════════════════════

# Full workflow (Steps 1-2)
python3 bin/1_export_csv_from_excel.py seasons/2025-26/input/rosters.xlsx
python3 bin/2_create_latex_rosters.py csv

# Verification
python3 bin/count_players.py seasons/2025-26/output/csv

# View outputs
open seasons/2025-26/output/rosters_pdf/
open seasons/2025-26/output/reports/player_count.csv

# Memory Mate (per team)
python3 bin/create_mm_csv_data.py "12U Black" \
    seasons/2025-26/output/csv/12U_Black.csv \
    seasons/2025-26/photos/12U_Black/


═══════════════════════════════════════════════════════════════════════
For detailed instructions, see:
• QUICKREF.md  - Quick reference guide
• WORKFLOW.md  - Complete step-by-step process
• README.md    - Project overview
═══════════════════════════════════════════════════════════════════════
```
