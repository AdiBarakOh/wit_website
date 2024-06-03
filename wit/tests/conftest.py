import sys

import pytest

from wit_project import constants
from wit_project import main
from wit_project import wit_init



@pytest.fixture(autouse=True, scope='session')
def create_wit_working_folder(tmp_path_factory):
    constants.WORKING_FOLDER = tmp_path_factory.mktemp("temp_dir")
    return constants.WORKING_FOLDER


@pytest.fixture(autouse=True, scope='session')
def wit_folder_creation(create_wit_working_folder):
    return wit_init.init()


@pytest.fixture(scope='session')
def wit_file_creation(wit_folder_creation):
    (constants.WORKING_FOLDER / 'text.txt').write_text('hi')
    

@pytest.fixture(scope='session')
def wit_add_file(wit_file_creation):
    sys.argv = ['_', 'add']
    sys.argv.append(constants.WORKING_FOLDER / 'text.txt')
    main.main()
    

@pytest.fixture(scope='session')    
def wit_commit_txt_file(wit_add_file):
    sys.argv = ['_', 'commit', 'commit_message']
    main.main()
    
    
    