from pathlib import Path
import sys

import pytest

from wit_project import constants
from wit_project import main
from wit_project import wit_add
from wit_project import wit_general_functions
from wit_project import wit_init


@pytest.fixture(scope='session')
def create_clean_commit(tmp_path_factory):
    # Diffrent folder for avoiding status changed by other tests.
    constants.WORKING_FOLDER = tmp_path_factory.mktemp("temp_dir_commit")
    wit_init.init()
    (constants.WORKING_FOLDER / 'text.txt').write_text('hi')
    file_path = constants.WORKING_FOLDER / 'text.txt'
    wit_add.add(file_path)


def test_commit_fail(create_clean_commit):
    
    sys.argv = ['_', 'commit']
    main.main()
    commit_head = wit_general_functions.get_commit_head(constants.WORKING_FOLDER / '.wit'/ 'references.txt')
    
    assert commit_head is None
    assert (constants.WORKING_FOLDER / '.wit'/ "staging_area" / 'text.txt').exists()
    
    
def test_commit(create_clean_commit):
    sys.argv = ['_', 'commit', 'commit_message']
    main.main()
    commit_head = wit_general_functions.get_commit_head(constants.WORKING_FOLDER / '.wit'/ 'references.txt')
    commit_folder = constants.WORKING_FOLDER / '.wit'/ "images" / commit_head
    
    assert (commit_folder / 'text.txt').exists()
    assert len(list(wit_general_functions.get_all_files_in_dir(commit_folder))) == 1
    assert "parent=None" in (commit_folder.parent / (commit_head + '.txt')).read_text()
    assert (constants.WORKING_FOLDER / '.wit' / 'activated.txt').read_text() == 'master'
    
    
    
    
    
    
    
    
    