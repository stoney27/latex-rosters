# !/usr/bin/env python3.9
# Tests for export_csv_from_excel
#
import pytest
import export_csv_from_excel

def test_clean_row():
    # Test empty first name
    headers = ['Firstname', 'Lastname', 'Sweater', 'Team']
    row = ['Ian', 'Stonefield', '$@#00', 'Bantam AAA']
    assert export_csv_from_excel.clean_row(row, headers) == ['Ian', 'Stonefield', '00', 'Bantam AAA']