from pathlib import Path
import sys

import pytest

from wit_project import constants
from wit_project import main
from wit_project import wit_general_functions


    
def test_add_nothing_or_add_from_no_wit_folder_available():
    sys.argv = ['_', 'add']
    main.main()
    staging_folder = constants.WORKING_FOLDER / '.wit'/ "staging_area"
    assert not list(wit_general_functions.get_all_files_in_dir(staging_folder))
    
    file_path = constants.WORKING_FOLDER.parent / 'not_gonna_work.txt'
    (file_path).write_text('hi')
    sys.argv = ['_', 'add', file_path]
    main.main()
    file_names = [file.name for file in wit_general_functions.get_all_files_in_dir(staging_folder)]
    assert 'not_gonna_work' not in file_names
    
    
def test_add_dir_and_files():
    dir_path = constants.WORKING_FOLDER / 'level_1' / 'level_2'
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / 'text_add.txt').write_text('hi')
    
    sys.argv = ['_', 'add', (dir_path / 'text_add.txt')]
    main.main()
    
    staging_folder = constants.WORKING_FOLDER / '.wit' / "staging_area"
    assert (staging_folder / 'level_1' / 'level_2' / 'text_add.txt').exists()
    
    
