#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for create_mm_csv_data.py - Memory Mate CSV generation
"""
import pytest
import sys
import os
import csv
import tempfile
import shutil
import importlib.util

# Import the script
script_path = os.path.join(os.path.dirname(__file__), '..', 'create_mm_csv_data.py')
spec = importlib.util.spec_from_file_location("create_mm_csv_data", script_path)
mm_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mm_module)


@pytest.fixture
def setup_photo_directory(tmpdir):
    """Create temporary directory with photo files"""
    photo_dir = tmpdir.mkdir("photos")
    
    # Create player photo files
    photo_files = [
        'Smith_John.jpg',
        'Doe_Jane.jpg',
        'Johnson_Bob.jpg',
        'Williams_Alice.jpg',
        'Team Photo.jpg',  # Team photo
    ]
    
    for photo_file in photo_files:
        photo_dir.join(photo_file).write("fake image data")
    
    yield str(photo_dir)


@pytest.fixture
def setup_roster_csv(tmpdir):
    """Create temporary roster CSV file"""
    csv_file = tmpdir.join("12U_Black.csv")
    
    roster_data = [
        ['Firstname', 'Lastname', 'Sweater', 'Team'],
        ['John', 'Smith', '10', '12U Black'],
        ['Jane', 'Doe', '11', '12U Black'],
        ['Bob', 'Johnson', '12', '12U Black'],
        ['Alice', 'Williams', '13', '12U Black'],
    ]
    
    with open(str(csv_file), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(roster_data)
    
    yield str(csv_file)


@pytest.fixture
def setup_season_structure(tmpdir):
    """Create full season directory structure with roster and photos"""
    # Create season structure
    season_dir = tmpdir.mkdir("seasons").mkdir("2025-26")
    output_dir = season_dir.mkdir("output")
    csv_dir = output_dir.mkdir("csv")
    reports_dir = output_dir.mkdir("reports")
    photos_dir = season_dir.mkdir("photos").mkdir("12U_Black")
    
    # Create roster CSV
    roster_file = csv_dir.join("12U_Black.csv")
    roster_data = [
        ['Firstname', 'Lastname', 'Sweater', 'Team'],
        ['John', 'Smith', '10', '12U Black'],
        ['Jane', 'Doe', '11', '12U Black'],
        ['Bob', 'Johnson', '12', '12U Black'],
    ]
    
    with open(str(roster_file), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(roster_data)
    
    # Create photo files
    photo_files = [
        'Smith_John.jpg',
        'Doe_Jane.jpg',
        'Johnson_Bob.jpg',
        'Team Photo.jpg',
    ]
    
    for photo_file in photo_files:
        photos_dir.join(photo_file).write("image data")
    
    yield str(roster_file), str(photos_dir), str(reports_dir)


def test_photos_full_path(setup_photo_directory):
    """Test getting full paths for all photos in directory"""
    photo_dir = setup_photo_directory
    
    full_paths = mm_module.photos_full_path(photo_dir)
    
    # Should return 5 files
    assert len(full_paths) == 5
    
    # All paths should be absolute
    for path in full_paths:
        assert os.path.isabs(path)
        assert photo_dir in path
    
    # Check that specific files are included
    filenames = [os.path.basename(p) for p in full_paths]
    assert 'Team Photo.jpg' in filenames
    assert 'Smith_John.jpg' in filenames


def test_find_team_photo(setup_photo_directory):
    """Test finding the team photo from a list"""
    photo_dir = setup_photo_directory
    full_paths = mm_module.photos_full_path(photo_dir)
    
    team_photo = mm_module.find_team_photo(full_paths)
    
    assert team_photo is not None
    assert 'Team Photo' in team_photo
    assert team_photo.endswith('.jpg')


def test_find_team_photo_missing():
    """Test when team photo is not in the list"""
    photo_list = [
        '/path/to/player1.jpg',
        '/path/to/player2.jpg',
    ]
    
    team_photo = mm_module.find_team_photo(photo_list)
    assert team_photo is None


def test_find_team_photo_case_sensitive():
    """Test team photo detection with different cases"""
    # Should find "Team Photo" (case sensitive)
    photo_list = [
        '/path/to/Team Photo.jpg',
        '/path/to/player.jpg',
    ]
    team_photo = mm_module.find_team_photo(photo_list)
    assert team_photo is not None
    
    # Should also find if "Team Photo" is part of filename
    photo_list = [
        '/path/to/2024_Team Photo_Final.jpg',
        '/path/to/player.jpg',
    ]
    team_photo = mm_module.find_team_photo(photo_list)
    assert team_photo is not None


def test_create_mm_csv_path_with_season(tmpdir):
    """Test MM CSV path creation with season structure"""
    # Create a season structure in tmpdir
    season_dir = tmpdir.mkdir("seasons").mkdir("2025-26")
    output_dir = season_dir.mkdir("output")
    csv_dir = output_dir.mkdir("csv")
    
    roster_file = os.path.join(str(csv_dir), "12U_Black.csv")
    photo_dir = str(tmpdir.mkdir("photos"))
    
    result = mm_module.create_mm_csv_path(photo_dir, roster_file)
    
    # Should place in reports directory
    assert 'seasons' in result
    assert '2025-26' in result
    assert 'reports' in result
    assert result.endswith('12U_Black_mm.csv')


def test_create_mm_csv_path_without_season(tmpdir):
    """Test MM CSV path creation without season structure"""
    photo_dir = str(tmpdir.mkdir("photos"))
    roster_file = "/some/other/path/roster.csv"
    
    result = mm_module.create_mm_csv_path(photo_dir, roster_file)
    
    # Should fallback to photo directory
    assert photo_dir in result
    assert result.endswith('roster_mm.csv')


def test_create_mm_csv_path_creates_directory(tmpdir):
    """Test that create_mm_csv_path creates the reports directory"""
    # Create season structure without reports dir
    season_dir = tmpdir.mkdir("seasons").mkdir("2024-25")
    output_dir = season_dir.mkdir("output")
    csv_dir = output_dir.mkdir("csv")
    
    roster_file = os.path.join(str(csv_dir), "Team.csv")
    photo_dir = str(tmpdir.mkdir("photos"))
    
    result = mm_module.create_mm_csv_path(photo_dir, roster_file)
    
    # Reports directory should now exist
    reports_dir = os.path.join(str(output_dir), "reports")
    assert os.path.exists(reports_dir)
    assert result.startswith(reports_dir)


def test_integration_full_mm_csv_creation(setup_season_structure):
    """Integration test for complete MM CSV creation"""
    roster_file, photos_dir, reports_dir = setup_season_structure
    team_name = "12U Black"
    
    # Get full photo paths
    photo_list = mm_module.photos_full_path(photos_dir)
    
    # Find team photo
    team_photo = mm_module.find_team_photo(photo_list)
    assert team_photo is not None
    
    # Remove team photo from list
    photo_list.remove(team_photo)
    
    # Create output path
    output_file = mm_module.create_mm_csv_path(photos_dir, roster_file)
    
    # Read roster and create MM CSV (simulating the main script logic)
    with open(roster_file, 'r') as infile:
        reader = csv.DictReader(infile)
        
        with open(output_file, 'w', newline='') as outfile:
            fieldnames = ['Lastname', 'Firstname', 'Sweater', 'Teamname', 'Photo', 'Team']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                row['Teamname'] = team_name
                row['Team'] = team_photo
                
                # Find player photo
                row['Photo'] = None
                for photo in photo_list:
                    if row['Lastname'] in photo and row['Firstname'] in photo:
                        row['Photo'] = photo
                        break
                
                if row['Photo'] is None:
                    row['Photo'] = 'blank'
                
                writer.writerow(row)
    
    # Verify output file exists
    assert os.path.exists(output_file)
    
    # Verify output content
    with open(output_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        # Should have 3 players
        assert len(rows) == 3
        
        # Check first player
        assert rows[0]['Firstname'] == 'John'
        assert rows[0]['Lastname'] == 'Smith'
        assert rows[0]['Sweater'] == '10'
        assert rows[0]['Teamname'] == team_name
        assert 'Smith_John' in rows[0]['Photo']
        assert 'Team Photo' in rows[0]['Team']


def test_filename_variations():
    """Test MM CSV path with various filename formats"""
    test_cases = [
        ("Team.csv", "Team_mm.csv"),
        ("12U_Black.csv", "12U_Black_mm.csv"),
        ("Girls_14U_Red.csv", "Girls_14U_Red_mm.csv"),
        ("/long/path/to/roster.csv", "roster_mm.csv"),
    ]
    
    photo_dir = "/tmp/photos"
    
    for input_file, expected_filename in test_cases:
        result = mm_module.create_mm_csv_path(photo_dir, input_file)
        assert result.endswith(expected_filename)


def test_photo_matching_edge_cases(tmpdir):
    """Test photo matching with edge cases"""
    photo_dir = tmpdir.mkdir("photos")
    
    # Create photos with similar names
    photo_files = [
        'Smith_John.jpg',
        'Smith_Johnny.jpg',  # Similar name
        'Johnson_John.jpg',  # Same first name
        'Smithson_John.jpg',  # Similar last name
        'Team Photo.jpg',
    ]
    
    for photo in photo_files:
        photo_dir.join(photo).write("data")
    
    full_paths = mm_module.photos_full_path(str(photo_dir))
    
    # Simulate matching for "John Smith"
    lastname = "Smith"
    firstname = "John"
    
    matched_photo = None
    for photo in full_paths:
        if lastname in photo and firstname in photo:
            matched_photo = photo
            break
    
    # Should match Smith_John.jpg (first match)
    assert matched_photo is not None
    assert 'Smith_John' in matched_photo


def test_empty_photo_directory(tmpdir):
    """Test handling of empty photo directory"""
    empty_dir = tmpdir.mkdir("empty_photos")
    
    full_paths = mm_module.photos_full_path(str(empty_dir))
    assert full_paths == []
    
    team_photo = mm_module.find_team_photo(full_paths)
    assert team_photo is None


def test_photos_with_spaces_in_names(tmpdir):
    """Test handling photos with spaces in filenames"""
    photo_dir = tmpdir.mkdir("photos")
    
    # Create photos with spaces
    photo_files = [
        'Smith John.jpg',
        'Doe Jane Marie.jpg',
        'Team Photo 2024.jpg',
    ]
    
    for photo in photo_files:
        photo_dir.join(photo).write("data")
    
    full_paths = mm_module.photos_full_path(str(photo_dir))
    assert len(full_paths) == 3
    
    # Should still find team photo
    team_photo = mm_module.find_team_photo(full_paths)
    assert team_photo is not None
    assert 'Team Photo' in team_photo
