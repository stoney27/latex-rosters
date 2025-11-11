#!/usr/bin/env python3
"""
Simple test runner to validate the updated test files
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("Testing Import of 1_export_csv_from_excel.py")
print("=" * 70)

try:
    import importlib.util
    script_path = os.path.join(os.path.dirname(__file__), '1_export_csv_from_excel.py')
    spec = importlib.util.spec_from_file_location("export_csv_from_excel", script_path)
    export_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(export_module)
    print("✓ Successfully imported 1_export_csv_from_excel.py")
    print(f"  - clean_name function: {hasattr(export_module, 'clean_name')}")
    print(f"  - clean_row function: {hasattr(export_module, 'clean_row')}")
    print(f"  - export_by_team function: {hasattr(export_module, 'export_by_team')}")
    print(f"  - export_by_workbook function: {hasattr(export_module, 'export_by_workbook')}")
except Exception as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)

print()
print("=" * 70)
print("Testing Import of 2_create_latex_rosters.py")
print("=" * 70)

try:
    script_path = os.path.join(os.path.dirname(__file__), '2_create_latex_rosters.py')
    spec = importlib.util.spec_from_file_location("create_latex_rosters", script_path)
    roster_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(roster_module)
    print("✓ Successfully imported 2_create_latex_rosters.py")
    print(f"  - get_project_root function: {hasattr(roster_module, 'get_project_root')}")
    print(f"  - get_season_year function: {hasattr(roster_module, 'get_season_year')}")
    print(f"  - get_csv_dir_and_template function: {hasattr(roster_module, 'get_csv_dir_and_template')}")
except Exception as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)

print()
print("=" * 70)
print("Testing Basic Functions")
print("=" * 70)

try:
    # Test get_project_root
    root = roster_module.get_project_root()
    print(f"✓ get_project_root() returned: {root}")
    print(f"  - bin directory exists: {os.path.exists(os.path.join(root, 'bin'))}")
    
    # Test get_season_year
    season = roster_module.get_season_year()
    print(f"✓ get_season_year() returned: {season}")
    
    # Test clean_name
    result = export_module.clean_name('JOHN')
    print(f"✓ clean_name('JOHN') returned: {result}")
    
except Exception as e:
    print(f"✗ Function test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print("All basic import and function tests passed! ✓")
print("=" * 70)
print()
print("To run full test suite, use:")
print("  pytest bin/tests/ -v")
