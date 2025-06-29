import os
import sys
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bin.create_latex_rosters import get_csv_dir_and_template
from bin.create_latex_rosters import get_project_root

def remove_bin_tests(path):
    return path.replace('/bin/tests', '')

# @pytest.fixture
# def setup_directories(monkeypatch):
#     project_root = os.path.dirname(os.path.abspath(__file__))
#     project_root = remove_bin_tests(project_root)

#     data_dir = os.path.join(project_root, 'test-data')
#     templates_dir = os.path.join(project_root, 'test-templates')

#     # Create mock directories
#     os.makedirs(data_dir, exist_ok=True)
#     os.makedirs(templates_dir, exist_ok=True)

#     # Create a mock template file
#     with open(os.path.join(templates_dir, 'RosterTemplate.tex'), 'w') as f:
#         f.write('Template content')

#     yield data_dir, templates_dir

#     # Cleanup
#     os.rmdir(data_dir)
#     os.remove(os.path.join(templates_dir, 'RosterTemplate.tex'))
#     os.rmdir(templates_dir)

def test_default_template(setup_directories):
    data_dir, templates_dir = setup_directories
    args = ['script_name', 'csv_directory']
    expected_csv_dir = os.path.join(data_dir, 'csv_directory')
    expected_template_file = os.path.join(templates_dir, 'RosterTemplate.tex')

    csv_dir, template_file = get_csv_dir_and_template(args)

    assert os.path.abspath(csv_dir) == os.path.abspath(expected_csv_dir)
    assert template_file == expected_template_file

def test_custom_template(setup_directories):
    data_dir, templates_dir = setup_directories
    custom_template = 'RosterTemplate.tex'
    with open(os.path.join(templates_dir, custom_template), 'w') as f:
        f.write('Custom template content')

    args = ['script_name', 'csv_directory', custom_template]
    expected_csv_dir = os.path.join(data_dir, 'csv_directory')
    expected_template_file = os.path.join(templates_dir, custom_template)

    csv_dir, template_file = get_csv_dir_and_template(args)

    assert os.path.abspath(csv_dir) == os.path.abspath(expected_csv_dir)
    assert template_file == expected_template_file

def test_missing_arguments():
    args = ['script_name']
    with pytest.raises(ValueError):
        get_csv_dir_and_template(args)
        
def test_get_project_root():
    project_root = get_project_root()
    project_root = remove_bin_tests(project_root)
    assert os.path.basename(project_root) == '/Users/srs/src/latex-rosters'