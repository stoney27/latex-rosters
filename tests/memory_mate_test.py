import os
from src.create_mm_csv_data import photos_full_path
from src.create_mm_csv_data import find_team_photo

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
