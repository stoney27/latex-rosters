#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for count_players.py utility
"""
import pytest
import sys
import os
import csv
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the count_players module
import count_players


@pytest.fixture
def setup_test_csv_files(tmpdir):
    """Create temporary CSV files for testing"""
    test_dir = tmpdir.mkdir("test_csv")
    
    # Create sample team CSV files
    teams = {
        '12U_Black.csv': [
            ['Firstname', 'Lastname', 'Sweater', 'Team'],
            ['John', 'Doe', '10', '12U Black'],
            ['Jane', 'Smith', '11', '12U Black'],
            ['Bob', 'Johnson', '12', '12U Black'],
        ],
        '12U_Red.csv': [
            ['Firstname', 'Lastname', 'Sweater', 'Team'],
            ['Alice', 'Williams', '20', '12U Red'],
            ['Charlie', 'Brown', '21', '12U Red'],
            ['David', 'Davis', '22', '12U Red'],
            ['Eve', 'Miller', '23', '12U Red'],
            ['Frank', 'Wilson', '24', '12U Red'],
        ],
        '14U_AAA.csv': [
            ['Firstname', 'Lastname', 'Sweater', 'Team'],
            ['George', 'Moore', '30', '14U AAA'],
            ['Helen', 'Taylor', '31', '14U AAA'],
        ],
    }
    
    for filename, rows in teams.items():
        filepath = test_dir.join(filename)
        with open(str(filepath), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    
    yield str(test_dir)


@pytest.fixture
def setup_season_structure(tmpdir):
    """Create temporary season directory structure"""
    season_dir = tmpdir.mkdir("seasons").mkdir("2024-25")
    output_dir = season_dir.mkdir("output")
    csv_dir = output_dir.mkdir("csv")
    
    # Create sample CSV files
    teams = {
        '10U_Black.csv': 8,  # 8 players
        '10U_Red.csv': 10,   # 10 players
        '12U_AAA.csv': 15,   # 15 players
    }
    
    for filename, player_count in teams.items():
        filepath = csv_dir.join(filename)
        with open(str(filepath), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Firstname', 'Lastname', 'Sweater', 'Team'])
            for i in range(player_count):
                writer.writerow([f'Player{i}', f'Last{i}', str(i), 'Team'])
    
    yield str(csv_dir), str(season_dir)


def test_count_lines_in_csv(setup_test_csv_files):
    """Test counting lines in a CSV file"""
    test_dir = setup_test_csv_files
    
    # Test file with 3 players (4 lines including header)
    file_path = os.path.join(test_dir, '12U_Black.csv')
    count = count_players.count_lines_in_csv(file_path)
    assert count == 3
    
    # Test file with 5 players
    file_path = os.path.join(test_dir, '12U_Red.csv')
    count = count_players.count_lines_in_csv(file_path)
    assert count == 5
    
    # Test file with 2 players
    file_path = os.path.join(test_dir, '14U_AAA.csv')
    count = count_players.count_lines_in_csv(file_path)
    assert count == 2


def test_format_filename():
    """Test filename formatting"""
    # Test basic CSV removal
    assert count_players.format_filename('12U_Black.csv') == '12U Black'
    
    # Test multiple underscores
    assert count_players.format_filename('14U_Red_American.csv') == '14U Red American'
    
    # Test with no underscores
    assert count_players.format_filename('AAA.csv') == 'AAA'
    
    # Test Girls teams
    assert count_players.format_filename('Girls_10U_Black.csv') == 'Girls 10U Black'


def test_main_with_basic_directory(setup_test_csv_files, tmpdir):
    """Test main function with a basic directory (no season structure)"""
    test_dir = setup_test_csv_files
    
    # Change to temp directory to avoid polluting project
    original_dir = os.getcwd()
    temp_work_dir = str(tmpdir.mkdir("work"))
    os.chdir(temp_work_dir)
    
    try:
        count_players.main(test_dir)
        
        # Check that output file was created
        output_file = os.path.join(temp_work_dir, 'player_count.csv')
        assert os.path.exists(output_file)
        
        # Read and verify the output
        with open(output_file, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Check header
            assert rows[0] == ['Team Name', 'Number of Players']
            
            # Check data rows (order may vary, so create a dict)
            data = {row[0]: int(row[1]) for row in rows[1:]}
            assert data['12U Black'] == 3
            assert data['12U Red'] == 5
            assert data['14U AAA'] == 2
            
    finally:
        os.chdir(original_dir)


def test_main_with_season_structure(setup_season_structure):
    """Test main function with season directory structure"""
    csv_dir, season_dir = setup_season_structure
    
    count_players.main(csv_dir)
    
    # Check that output file was created in reports directory
    output_file = os.path.join(season_dir, 'output', 'reports', 'player_count.csv')
    assert os.path.exists(output_file)
    
    # Read and verify the output
    with open(output_file, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Check header
        assert rows[0] == ['Team Name', 'Number of Players']
        
        # Check data (order may vary)
        data = {row[0]: int(row[1]) for row in rows[1:]}
        assert data['10U Black'] == 8
        assert data['10U Red'] == 10
        assert data['12U AAA'] == 15
        
        # Verify total
        total = sum(data.values())
        assert total == 33


def test_main_with_nonexistent_directory(capsys):
    """Test main function with non-existent directory"""
    count_players.main('/path/that/does/not/exist')
    
    captured = capsys.readouterr()
    assert 'does not exist' in captured.out


def test_main_with_empty_directory(tmpdir):
    """Test main function with empty directory"""
    empty_dir = tmpdir.mkdir("empty")
    
    # Change to temp directory
    original_dir = os.getcwd()
    os.chdir(str(tmpdir))
    
    try:
        count_players.main(str(empty_dir))
        
        # Should create output file with just header
        output_file = 'player_count.csv'
        assert os.path.exists(output_file)
        
        with open(output_file, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 1  # Just header
            assert rows[0] == ['Team Name', 'Number of Players']
    finally:
        os.chdir(original_dir)


def test_main_with_non_csv_files(tmpdir):
    """Test that non-CSV files are ignored"""
    test_dir = tmpdir.mkdir("mixed_files")
    
    # Create CSV file
    csv_file = test_dir.join("team.csv")
    with open(str(csv_file), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Firstname', 'Lastname', 'Sweater', 'Team'])
        writer.writerow(['John', 'Doe', '10', 'Team'])
    
    # Create non-CSV files
    test_dir.join("readme.txt").write("Some text")
    test_dir.join("data.xlsx").write("Excel data")
    
    # Change to temp directory
    original_dir = os.getcwd()
    os.chdir(str(tmpdir))
    
    try:
        count_players.main(str(test_dir))
        
        # Should only process the CSV file
        output_file = 'player_count.csv'
        with open(output_file, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
            # Should have header + 1 data row
            assert len(rows) == 2
    finally:
        os.chdir(original_dir)


def test_integration_full_workflow(tmpdir):
    """Integration test simulating full workflow"""
    # Create season structure
    project_root = tmpdir.mkdir("project")
    season = "2025-26"
    season_dir = project_root.mkdir("seasons").mkdir(season)
    output_dir = season_dir.mkdir("output")
    csv_dir = output_dir.mkdir("csv")
    
    # Create multiple team files
    teams_data = {
        '9U_Black': 7,
        '9U_Red': 8,
        '10U_Black': 12,
        '10U_Red': 11,
        '10U_White': 9,
        '12U_AAA': 16,
        'Girls_10U_Black': 10,
        'Girls_12U_Red': 13,
    }
    
    for team_name, player_count in teams_data.items():
        filepath = csv_dir.join(f"{team_name}.csv")
        with open(str(filepath), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Firstname', 'Lastname', 'Sweater', 'Team'])
            for i in range(player_count):
                writer.writerow([f'Player{i}', f'Last{i}', str(i+1), team_name])
    
    # Run the count_players function
    count_players.main(str(csv_dir))
    
    # Verify output
    reports_dir = output_dir.join("reports")
    assert reports_dir.check()
    
    output_file = reports_dir.join("player_count.csv")
    assert output_file.check()
    
    # Read and verify all teams are counted
    with open(str(output_file), 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Should have header + 8 teams
        assert len(rows) == 9
        
        data = {row[0]: int(row[1]) for row in rows[1:]}
        
        # Verify each team
        assert data['9U Black'] == 7
        assert data['10U Black'] == 12
        assert data['Girls 10U Black'] == 10
        assert data['Girls 12U Red'] == 13
        
        # Verify total
        total = sum(data.values())
        assert total == sum(teams_data.values())
        assert total == 86
