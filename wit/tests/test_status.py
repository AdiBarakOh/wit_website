import sys

import pytest

from wit_project import constants
from wit_project import main
from wit_project import wit_add
from wit_project import wit_commit
from wit_project import wit_init
from wit_project import wit_status


@pytest.fixture(scope='session')
def create_changes_not_staged_for_commit(tmp_path_factory):
    # Diffrent folder for avoiding status changed by other tests.
    constants.WORKING_FOLDER = tmp_path_factory.mktemp("temp_dir_status")
    wit_init.init()
    (constants.WORKING_FOLDER / 'text.txt').write_text('hi')
    file_path = constants.WORKING_FOLDER / 'text.txt'
    wit_add.add(file_path)
    wit_commit.commit('For status')
    (constants.WORKING_FOLDER / 'text.txt').write_text('bye')
    
 
@pytest.fixture(scope='session')   
def create_changes_to_be_commited_and_untracked(create_changes_not_staged_for_commit):
    file_path = constants.WORKING_FOLDER / 'text_2.txt'
    file_path.write_text('hi')
    wit_add.add(constants.WORKING_FOLDER / 'text.txt')

    
def test_status_not_staged_for_commit(create_changes_not_staged_for_commit):
    sys.argv = ['_', 'status']
    main.main()
    assert wit_status.status()[2][0].name == 'text.txt'
    assert (constants.WORKING_FOLDER / 'text.txt') not in wit_status.status()[3]
    
    
def test_status_to_be_commited_and_untracked(create_changes_to_be_commited_and_untracked):
    sys.argv = ['_', 'status']
    main.main()
    assert wit_status.status()[2] == []
    assert wit_status.status()[1][0].name == 'text.txt'
    assert constants.WORKING_FOLDER / 'text_2.txt' in wit_status.status()[3]
    
    
    
    