import os
import sys
import pytest
import tempfile
import shutil

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import from the numbered script
import importlib.util
spec = importlib.util.spec_from_file_location("create_latex_rosters", 
    os.path.join(os.path.dirname(__file__), '..', '2_create_latex_rosters.py'))
create_latex_rosters = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create_latex_rosters)

get_csv_dir_and_template = create_latex_rosters.get_csv_dir_and_template
get_project_root = create_latex_rosters.get_project_root
get_season_year = create_latex_rosters.get_season_year


@pytest.fixture
def setup_test_environment(tmpdir):
    """Create a temporary test environment with season structure"""
    # Create temporary season directory
    test_root = tmpdir.mkdir("latex-rosters")
    test_root.mkdir("bin")  # So get_project_root works
    test_root.mkdir("templates")
    
    # Create seasons structure
    season = "2024-25"
    season_dir = test_root.mkdir("seasons").mkdir(season)
    output_dir = season_dir.mkdir("output")
    csv_dir = output_dir.mkdir("csv")
    
    # Create template
    template_file = test_root.join("templates", "RosterTemplate.tex")
    template_file.write("Test template content: CSV_FILE")
    
    yield str(test_root), str(csv_dir), str(template_file), season
    
    # Cleanup happens automatically with tmpdir


def test_get_project_root():
    """Test that get_project_root finds the correct root directory"""
    project_root = get_project_root()
    assert os.path.exists(os.path.join(project_root, 'bin'))
    assert os.path.basename(project_root) == 'latex-rosters'


def test_get_season_year():
    """Test season year detection"""
    season = get_season_year()
    # Should return format like "2025-26"
    assert '-' in season
    parts = season.split('-')
    assert len(parts) == 2
    assert len(parts[0]) == 4  # Full year
    assert len(parts[1]) == 2  # Two-digit year


def test_csv_dir_and_template_basic(setup_test_environment, monkeypatch):
    """Test basic CSV directory and template detection"""
    test_root, csv_dir, template_file, season = setup_test_environment
    
    # Monkeypatch get_project_root to return our test root
    monkeypatch.setattr(create_latex_rosters, 'get_project_root', lambda: test_root)
    monkeypatch.setattr(create_latex_rosters, 'get_season_year', lambda: season)
    
    args = ['script_name', 'csv']
    result_csv_dir, result_template, result_season = get_csv_dir_and_template(args)
    
    # Verify the paths are constructed correctly
    assert 'csv' in result_csv_dir
    assert 'seasons' in result_csv_dir
    assert result_template == template_file
    assert result_season == season


def test_custom_template(setup_test_environment, monkeypatch):
    """Test with custom template file"""
    test_root, csv_dir, template_file, season = setup_test_environment
    
    # Create custom template
    custom_template_file = os.path.join(test_root, 'templates', 'CustomTemplate.tex')
    with open(custom_template_file, 'w') as f:
        f.write('Custom template content')
    
    monkeypatch.setattr(create_latex_rosters, 'get_project_root', lambda: test_root)
    monkeypatch.setattr(create_latex_rosters, 'get_season_year', lambda: season)
    
    args = ['script_name', 'csv', 'CustomTemplate.tex']
    result_csv_dir, result_template, result_season = get_csv_dir_and_template(args)
    
    assert result_template == custom_template_file


def test_missing_arguments():
    """Test that missing arguments raises ValueError"""
    args = ['script_name']
    with pytest.raises(ValueError, match='Please provide'):
        get_csv_dir_and_template(args)


def test_season_override(setup_test_environment, monkeypatch):
    """Test manual season override"""
    test_root, csv_dir, template_file, season = setup_test_environment
    
    # Create another season directory
    test_season = "2026-27"
    season_dir = os.path.join(test_root, 'seasons', test_season)
    os.makedirs(os.path.join(season_dir, 'output', 'csv'), exist_ok=True)
    
    monkeypatch.setattr(create_latex_rosters, 'get_project_root', lambda: test_root)
    
    args = ['script_name', 'csv', test_season]
    result_csv_dir, result_template, result_season = get_csv_dir_and_template(args)
    
    assert test_season in result_csv_dir
    assert result_season == test_season


def test_check_dependencies_pdflatex_missing():
    """Test dependency check when pdflatex is missing"""
    fake_path = '/fake/path/to/pdflatex'
    template_file = __file__  # Use this file as a valid template
    
    with pytest.raises(FileNotFoundError, match='pdflatex not found'):
        create_latex_rosters.check_dependencies(fake_path, template_file)


def test_check_dependencies_template_missing():
    """Test dependency check when template is missing"""
    # Use /bin/sh as a valid executable path
    pdflatex_path = '/bin/sh'
    fake_template = '/fake/path/to/template.tex'
    
    with pytest.raises(FileNotFoundError, match='Template file.*not found'):
        create_latex_rosters.check_dependencies(pdflatex_path, fake_template)


def test_create_latex_directory(tmpdir, monkeypatch):
    """Test LaTeX directory creation"""
    test_root = tmpdir.mkdir("project")
    test_root.mkdir("bin")  # For get_project_root
    season = "2024-25"
    
    monkeypatch.setattr(create_latex_rosters, 'get_project_root', lambda: str(test_root))
    
    latex_dir = create_latex_rosters.create_latex_directory(season)
    
    assert os.path.exists(latex_dir)
    assert 'rosters_latex' in latex_dir
    assert season in latex_dir


def test_create_pdf_directory(tmpdir, monkeypatch):
    """Test PDF directory creation"""
    test_root = tmpdir.mkdir("project")
    test_root.mkdir("bin")
    season = "2024-25"
    
    monkeypatch.setattr(create_latex_rosters, 'get_project_root', lambda: str(test_root))
    
    pdf_dir = create_latex_rosters.create_pdf_directory(season)
    
    assert os.path.exists(pdf_dir)
    assert 'rosters_pdf' in pdf_dir
    assert season in pdf_dir


def test_create_latex_file_from_template(tmpdir):
    """Test LaTeX file generation from template"""
    # Create template file
    template_file = tmpdir.join("template.tex")
    template_content = r"""
\documentclass{article}
\begin{document}
\csvreader{CSV_FILE}{columns}{\item \name}
\end{document}
"""
    template_file.write(template_content)
    
    # Create CSV file
    csv_file = tmpdir.join("team.csv")
    csv_file.write("name,number\nJohn,10\nJane,11")
    
    # Output file
    output_file = tmpdir.join("team.tex")
    
    # Generate LaTeX file
    create_latex_rosters.create_latex_file_from_template(
        str(template_file),
        str(csv_file),
        str(output_file)
    )
    
    # Verify output
    assert output_file.check()
    content = output_file.read()
    assert str(csv_file) in content
    assert 'CSV_FILE' not in content


def test_process_csv_files(tmpdir):
    """Test processing multiple CSV files"""
    # Create CSV directory with files
    csv_dir = tmpdir.mkdir("csv")
    csv_dir.join("team1.csv").write("name,number\nJohn,10")
    csv_dir.join("team2.csv").write("name,number\nJane,11")
    csv_dir.join("readme.txt").write("ignore this")  # Non-CSV file
    
    # Create template
    template_file = tmpdir.join("template.tex")
    template_file.write(r"\csvreader{CSV_FILE}")
    
    # Create LaTeX output directory
    latex_dir = tmpdir.mkdir("latex")
    
    # Process files
    create_latex_rosters.process_csv_files(
        str(csv_dir),
        str(template_file),
        str(latex_dir)
    )
    
    # Verify output
    assert latex_dir.join("team1.tex").check()
    assert latex_dir.join("team2.tex").check()
    assert not latex_dir.join("readme.tex").check()  # Should not process .txt


def test_cleanup_auxiliary_tex_files(tmpdir):
    """Test cleanup of auxiliary LaTeX files"""
    pdf_dir = tmpdir.mkdir("pdf")
    
    # Create various files
    pdf_dir.join("team.pdf").write("pdf content")
    pdf_dir.join("team.log").write("log content")
    pdf_dir.join("team.aux").write("aux content")
    pdf_dir.join("team.tex").write("tex content")
    
    # Run cleanup
    create_latex_rosters.cleanup_auxiliary_tex_files(str(pdf_dir))
    
    # Check results
    assert pdf_dir.join("team.pdf").check()  # Should keep
    assert pdf_dir.join("team.tex").check()  # Should keep
    assert not pdf_dir.join("team.log").check()  # Should remove
    assert not pdf_dir.join("team.aux").check()  # Should remove


def test_integration_latex_generation_workflow(tmpdir, monkeypatch):
    """Integration test for complete LaTeX generation workflow"""
    # Setup project structure
    project_root = tmpdir.mkdir("project")
    project_root.mkdir("bin")
    templates_dir = project_root.mkdir("templates")
    
    season = "2025-26"
    season_dir = project_root.mkdir("seasons").mkdir(season)
    output_dir = season_dir.mkdir("output")
    csv_dir = output_dir.mkdir("csv")
    
    # Create template
    template_file = templates_dir.join("RosterTemplate.tex")
    template_content = r"""
\documentclass{article}
\usepackage{csvsimple}
\begin{document}
\csvreader[head to column names]{CSV_FILE}{}{\name: \number}
\end{document}
"""
    template_file.write(template_content)
    
    # Create CSV files
    teams = {
        '12U_Black': [['Firstname', 'Lastname', 'Sweater'], ['John', 'Doe', '10']],
        '12U_Red': [['Firstname', 'Lastname', 'Sweater'], ['Jane', 'Smith', '11']],
    }
    
    for team_name, rows in teams.items():
        team_file = csv_dir.join(f"{team_name}.csv")
        import csv as csv_module
        with open(str(team_file), 'w', newline='') as f:
            writer = csv_module.writer(f)
            writer.writerows(rows)
    
    # Monkeypatch functions
    monkeypatch.setattr(create_latex_rosters, 'get_project_root', lambda: str(project_root))
    monkeypatch.setattr(create_latex_rosters, 'get_season_year', lambda: season)
    
    # Get directories and template
    args = ['script_name', 'csv']
    result_csv_dir, result_template, result_season = get_csv_dir_and_template(args)
    
    # Create output directories
    latex_dir = create_latex_rosters.create_latex_directory(season)
    pdf_dir = create_latex_rosters.create_pdf_directory(season)
    
    # Process CSV files
    create_latex_rosters.process_csv_files(str(csv_dir), str(template_file), latex_dir)
    
    # Verify LaTeX files created
    assert os.path.exists(os.path.join(latex_dir, '12U_Black.tex'))
    assert os.path.exists(os.path.join(latex_dir, '12U_Red.tex'))
    
    # Verify content
    with open(os.path.join(latex_dir, '12U_Black.tex'), 'r') as f:
        content = f.read()
        assert '12U_Black.csv' in content
        assert 'CSV_FILE' not in content