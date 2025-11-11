#!/usr/bin/env python3
"""
Quick test to verify the fixes work
"""
import sys
import os

# Change to project root
os.chdir('/Users/srs/src/latex-rosters')

print("Running quick test validation...")
print("=" * 60)

# Run pytest with explicit output
import subprocess
result = subprocess.run(
    ['python3', '-m', 'pytest', 'bin/tests/test_export_csv_from_excel.py', '-v', '--tb=short'],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("STDERR:")
    print(result.stderr)

sys.exit(result.returncode)
