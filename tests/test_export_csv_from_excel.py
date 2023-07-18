# !/usr/bin/env python3.9
# Tests for export_csv_from_excel
#
import pytest
import export_csv_from_excel
import csv
import os
import pandas as pd

# Create workbook test data
def create_test_workbook():
    team1 = [
        ['Ian', 'Stonefield', '1', 'Bantam AAA'],
        ['Scott', 'Stonefield', '10', 'Bantam AAA'],
        ['Dylan', 'Stonefield', '20', 'Bantam AAA'],
        ['Evan', 'Stonefield', '30', 'Bantam AAA'],
        ]
    
    team2 = [
        ['Aidan', 'Stonefield', '40', '16U AAA'],
        ['Avery', 'Stonefield', '50', '16U AAA'],
        ['Kieran', 'Stonefield', '60', '16U AAA'],
        ['Mason', 'Stonefield', '70', '16U AAA'],
        ]

    headers = ['Firstname', 'Lastname', 'Sweater', 'Team']
    # Write out rows to a excel file for testing
    df1 = pd.DataFrame(team1, columns=headers)
    df2 = pd.DataFrame(team2, columns=headers)
    
    writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Bantam AAA', index=False)
    df2.to_excel(writer, sheet_name='16U AAA', index=False)
    writer.close()

# Create a test file
def create_team_test_data():
    # test the player count funcionality by passing in a list of rows
    rows = [
        ['Ian', 'Stonefield', '1', 'Bantam AAA'],
        ['Scott', 'Stonefield', '10', 'Bantam AAA'],
        ['Dylan', 'Stonefield', '20', 'Bantam AAA'],
        ['Evan', 'Stonefield', '30', 'Bantam AAA'],
        ['Aidan', 'Stonefield', '40', 'Bantam AAA'],
        ['Avery', 'Stonefield', '50', 'Bantam AAA'],
        ['Kieran', 'Stonefield', '60', 'Bantam AAA'],
        ['Mason', 'Stonefield', '70', 'Bantam AAA'],
        ['Carter', 'Stonefield', '80', 'Squirt A'],
        ['Riley', 'Stonefield', '9', 'Squirt A'],
        ['Nathan', 'Stonefield', '11', 'Squirt A'],
        ['Ethan', 'Stonefield', '12', 'Squirt A'],
        ['Kaden', 'Stonefield', '13', 'Squirt A'],
        ['Cameron', 'Stonefield', '50', 'Squirt A'],
    ]

    headers = ['Firstname', 'Lastname', 'Sweater', 'Team']
    
    # Write out rows to a excel file for testing
    df = pd.DataFrame(rows, columns=headers)
    
    writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Test Team', index=False)
    writer.close()

# Cleanup the test files
def cleanup_test_data():
    # Remove the test file
    if os.path.exists('test.xlsx'):
        os.remove('test.xlsx')
    if os.path.exists('test.csv'):
        os.remove('test.csv')
    if os.path.exists('csv/Bantam_AAA.csv'):
        os.remove('csv/Bantam_AAA.csv')
    if os.path.exists('csv/16U_AAA.csv'):
        os.remove('csv/16U_AAA.csv')
    if os.path.exists('csv/Squirt_A.csv'):
        os.remove('csv/Squirt_A.csv')

# Test the clean_row function
def test_clean_row():
    # Test empty first name
    headers = ['Firstname', 'Lastname', 'Sweater', 'Team']
    row = ['Ian', 'Stoney', '$@#00', 'Bantam AAA']
    assert export_csv_from_excel.clean_row(row, headers) == ['Ian', 'Stoney', '00', 'Bantam AAA']
    
    row = ['BEN', 'stoney', '10', 'Squirt AAA']
    assert export_csv_from_excel.clean_row(row, headers) == ['Ben', 'Stoney', '10', 'Squirt AAA']
    
# test the player count funcionality by passing in a list of rows
def test_player_count():
    create_team_test_data()
    
    export_csv_from_excel.export_by_team('test.xlsx')
    
    assert export_csv_from_excel.player_count == 14
    
    cleanup_test_data()
    
# Test the export_by_workbook function
def test_by_workbook():
    create_test_workbook()
    
    export_csv_from_excel.export_by_workbook('test.xlsx')
    
    assert os.path.exists('csv/Bantam_AAA.csv')
    assert os.path.exists('csv/16U_AAA.csv')
    
    # Read the csv file and check the contents
    with open('csv/Bantam_AAA.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        row_count = 0
        for row in reader:
            row_count += 1
        assert row_count == 5

    cleanup_test_data()
    
# Test the export_by_team function
def test_by_team():
    create_team_test_data()
    
    export_csv_from_excel.export_by_team('test.xlsx')
    
    assert os.path.exists('csv/Squirt_A.csv')
    
    # Read the csv file and check the contents
    with open('csv/Squirt_A.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        row_count = 0
        for row in reader:
            row_count += 1
        assert row_count == 7

    cleanup_test_data()