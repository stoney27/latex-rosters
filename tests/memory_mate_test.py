import os
import sys
import pytest
import csv

from src.create_mm_csv_data import photos_full_path
from src.create_mm_csv_data import find_team_photo
from src.create_mm_csv_data import get_check_args
from src.create_mm_csv_data import check_photos
from src.create_mm_csv_data import write_csv_file
from src.create_mm_csv_data import main


# Create test csv data file
def create_test_csv_data(tmpdir, filename):
    # Create a temporary file
    csv_file = os.path.join(tmpdir, filename)

    file = open(csv_file, 'w', newline='')

    with file:
        # Create some test data with a temporary file
        order = ['Firstname', 'Lastname', 
                    'Sweater', 'Team']
        csv_writer = csv.DictWriter(file, fieldnames=order)
        csv_writer.writeheader()

        # Create some test data
        csv_writer.writerow({'Firstname': 'John', 'Lastname': 'Smith','Sweater': '45', 'Team': '12U AAA'})
        csv_writer.writerow({'Firstname': 'Jerry', 'Lastname': 'Flynn','Sweater': '89', 'Team': '12U AAA'})
        csv_writer.writerow({'Firstname': 'Ian', 'Lastname': 'Stone','Sweater': '12', 'Team': '12U AAA'})

    return csv_file

# Test photos_full_path function
def test_photos_full_path(tmpdir):
    # Create some files in the temporary directory
    open(os.path.join(tmpdir, 'file1.jpg'), 'w').close()
    open(os.path.join(tmpdir, 'file2.jpg'), 'w').close()

    # Test with the temporary directory
    expected_output = [os.path.join(
        tmpdir, 'file1.jpg'), os.path.join(tmpdir, 'file2.jpg')]
    assert photos_full_path(tmpdir) == expected_output

# Test find_team_photo function
def test_find_team_photo():
    # Create some test data
    photo_list = [
        '/tmp/John Smith#45.jpg',
        '/tmp/Jerry Flynn#89.jpg',
        '/tmp/Team Photo - 12U AAA.jpg',
    ]
    photo_list2 = [
        '/tmp/John Smith#45.jpg',
        '/tmp/Jerry Flynn#89.jpg',
        '/tmp/Ian Stone#12.jpg',
    ]

    # Call the function under test
    assert find_team_photo(photo_list) == '/tmp/Team Photo - 12U AAA.jpg'
    assert find_team_photo(photo_list2) == None

# Test get_check_args function
def test_get_check_args(tmpdir):

    # set the sys.argv list
    # Create a temporary file
    csv_file = os.path.join(tmpdir, 'test.csv')

    sys.argv = ['create_mm_csv_data.py', csv_file, '-p /tmp', '-t "Team Name"']

    # Create some test data with a temporary file
    open(csv_file, 'w').close()
    filename = csv_file
    path = '/tmp'
    team_name = '"Team Name"'

    # Call the function under test
    assert get_check_args() == (filename, path, team_name)

    # Call with just two args
    sys.argv = ['create_mm_csv_data.py', csv_file]
    # get current working directory
    cwd = os.getcwd()
    assert get_check_args() == (filename, cwd, None)

    # Call with just one arg
    sys.argv = ['create_mm_csv_data.py']
    with pytest.raises(SystemExit) as e:
        get_check_args()
    assert e.type == SystemExit
    assert e.value.code == 2

    # Call with no filename but other args
    sys.argv = ['create_mm_csv_data.py', '-p /tmp', '-t "Team Name"']
    with pytest.raises(SystemExit) as e:
        get_check_args()
    assert e.type == SystemExit
    assert e.value.code == 2

def test_check_photos(tmpdir):

    csv_file = create_test_csv_data(tmpdir, 'test.csv')
    print(f"csv_file: {csv_file}")

    data = csv.DictReader(open(csv_file))
    
    player_data = list(data)

    # Create a list of photo files including playernames in the filename
    photo_list = []
    photo_list.append(os.path.join(tmpdir, 'John Smith#45.jpg'))
    photo_list.append(os.path.join(tmpdir, 'Jerry Flynn#89.jpg'))

    # Call the function under test
    assert check_photos(player_data,photo_list) == False

    # Create a list of photo files including playernames in the filename
    photo_list = []
    photo_list.append(os.path.join(tmpdir, 'John Smith#45.jpg'))
    photo_list.append(os.path.join(tmpdir, 'Jerry Flynn#89.jpg'))
    photo_list.append(os.path.join(tmpdir, 'Ian Stone#12.jpg'))

    # Call the function under test
    assert check_photos(player_data,photo_list) == True

# Test write_csv_file function
def test_write_csv_file(tmpdir):

    # setup data
    csv_file = create_test_csv_data(tmpdir, 'test.csv')
    data = csv.DictReader(open(csv_file, 'r'))
    field_names = data.fieldnames

    player_data = list(data)

    # Create a temporary file
    csv_file = os.path.join(tmpdir, 'newData.csv')

    team_photo = "/tmp/Team Photo - 12U AAA.jpg"

    photo_list = [
        '/tmp/John Smith#45.jpg',
        '/tmp/Jerry Flynn#89.jpg',
        '/tmp/Ian Stone#12.jpg',
    ]
    # Call the function under test
    write_csv_file(csv_file, player_data, photo_list, team_photo, None)

    # Read the file and check the data
    data = csv.DictReader(open(csv_file))
    field_names = data.fieldnames
    assert field_names == ['Lastname', 'Firstname', 'Sweater', 'Team', 'Photo', 'TeamPhoto']
    test_player_data = list(data)
    assert test_player_data[0]['Firstname'] == 'John'
    assert test_player_data[0]['Lastname'] == 'Smith'
    assert test_player_data[0]['Sweater'] == '45'
    assert test_player_data[0]['Team'] == '12U AAA'
    assert test_player_data[0]['Photo'] == '/tmp/John Smith#45.jpg'
    assert test_player_data[0]['TeamPhoto'] == '/tmp/Team Photo - 12U AAA.jpg'
    assert test_player_data[2]['Lastname'] == 'Stone'
    assert test_player_data[2]['Firstname'] == 'Ian'
    assert test_player_data[2]['Sweater'] == '12'
    assert test_player_data[2]['Team'] == '12U AAA'
    assert test_player_data[2]['Photo'] == '/tmp/Ian Stone#12.jpg'
    assert test_player_data[2]['TeamPhoto'] == '/tmp/Team Photo - 12U AAA.jpg'

    # Call write_csv_file with team name
    write_csv_file(csv_file, player_data, photo_list, team_photo, "16U AAA")

    # Read the file and check the data
    data = csv.DictReader(open(csv_file))
    field_names = data.fieldnames
    assert field_names == ['Lastname', 'Firstname', 'Sweater', 'Team', 'Photo', 'TeamPhoto']
    test_player_data = list(data)
    assert test_player_data[0]['Firstname'] == 'John'
    assert test_player_data[0]['Team'] == '16U AAA'


def test_main(mocker, tmpdir):
    # Set up test variables and mocked functions
    csv_file = create_test_csv_data(tmpdir, 'test.csv')
    
    sys.argv = ['create_mm_csv_data.py', csv_file, '-p /tmp', '-t "12U AAA"']

    path = "test_path"
    team_name = "12U AAA"
    team_photo = "/tmp/Team Photo - 12U AAA.jpg"

    photos_list = [
        '/tmp/John Smith#45.jpg',
        '/tmp/Jerry Flynn#89.jpg',
        '/tmp/Ian Stone#12.jpg',
        '/tmp/Team Photo - 12U AAA.jpg'
    ]

    # Define mocked functions
    mocker.patch('src.create_mm_csv_data.get_check_args', return_value=(csv_file, path, team_name))
    mocker.patch('src.create_mm_csv_data.photos_full_path', return_value=photos_list)
    mocker.patch('src.create_mm_csv_data.find_team_photo', return_value=team_photo)
    mocker.patch('src.create_mm_csv_data.check_photos', return_value=True)

    # Call main function
    main()

    expected_player_data = [{'Lastname': 'Smith', 'Firstname': 'John', 'Sweater': '45', 'Team': '12U AAA', 'Photo': '/tmp/John Smith#45.jpg', 'TeamPhoto': '/tmp/Team Photo - 12U AAA.jpg'}, 
                            {'Lastname': 'Flynn', 'Firstname': 'Jerry', 'Sweater': '89','Team': '12U AAA', 'Photo': '/tmp/Jerry Flynn#89.jpg', 'TeamPhoto': '/tmp/Team Photo - 12U AAA.jpg'},
                            {'Lastname': 'Stone', 'Firstname': 'Ian', 'Sweater': '12', 'Team': '12U AAA', 'Photo': '/tmp/Ian Stone#12.jpg', 'TeamPhoto': '/tmp/Team Photo - 12U AAA.jpg'}]
    # Check that new file is created
    newfile = os.path.splitext(os.path.basename(csv_file))[0] + "_mm.csv"
    csv_file_path = os.path.dirname(csv_file)
    new_csv_file = os.path.join(csv_file_path, newfile)
    assert os.path.exists(new_csv_file)

    # Check that new file contains expected data
    with open(new_csv_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows == expected_player_data

    # Clean up
    os.remove(new_csv_file)
    os.remove(csv_file)

    # Test with no team photo
    mocker.patch('src.create_mm_csv_data.find_team_photo', return_value=None) 
    
    with pytest.raises(SystemExit) as e:
        main()
    assert e.type == SystemExit
    assert e.value.code == 1


    # Test with different team name
    csv_file2 = create_test_csv_data(tmpdir, 'test2.csv')
    team_name = "16U Black"
    sys.argv = ['create_mm_csv_data.py', csv_file2, '-p /tmp', '-t ' + team_name]

    path = "test_path"
    team_photo = "/tmp/Team Photo.jpg"

    photos_list = [
        '/tmp/John Smith#45.jpg',
        '/tmp/Jerry Flynn#89.jpg',
        '/tmp/Ian Stone#12.jpg',
        '/tmp/Team Photo.jpg'
    ]

    # Define mocked functions
    mocker.patch('src.create_mm_csv_data.get_check_args',
                return_value=(csv_file2, path, team_name))
    mocker.patch('src.create_mm_csv_data.photos_full_path',
                return_value=photos_list)
    mocker.patch('src.create_mm_csv_data.find_team_photo',
                return_value=team_photo)
    mocker.patch('src.create_mm_csv_data.check_photos', return_value=True)

    # Call main function
    main()

    newfile = os.path.splitext(os.path.basename(csv_file2))[0] + "_mm.csv"
    csv_file_path2 = os.path.dirname(csv_file2)
    new_csv_file = os.path.join(csv_file_path2, newfile)
    assert os.path.exists(new_csv_file)

    print(f"new_csv_file: {new_csv_file}")

    expected_player_data2 = [{'Lastname': 'Smith', 'Firstname': 'John', 'Sweater': '45', 'Team': '16U Black', 
                                'Photo': '/tmp/John Smith#45.jpg', 'TeamPhoto': '/tmp/Team Photo.jpg'},
                            {'Lastname': 'Flynn', 'Firstname': 'Jerry', 'Sweater': '89', 'Team': '16U Black',
                                'Photo': '/tmp/Jerry Flynn#89.jpg', 'TeamPhoto': '/tmp/Team Photo.jpg'},
                            {'Lastname': 'Stone', 'Firstname': 'Ian', 'Sweater': '12', 'Team': '16U Black', 
                                'Photo': '/tmp/Ian Stone#12.jpg', 'TeamPhoto': '/tmp/Team Photo.jpg'}]
    
    # Check that new file contains expected data
    with open(new_csv_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows == expected_player_data2

    # Clean up test file
    os.remove(new_csv_file)
    os.remove(csv_file2)
