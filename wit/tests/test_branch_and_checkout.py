import sys

import pytest

from wit_project import constants
from wit_project import main
from wit_project import wit_add
from wit_project import wit_commit
from wit_project import wit_general_functions



def test_branch_adi(wit_commit_txt_file):
    sys.argv = ['_', 'branch', 'adi']
    main.main()
    ref_file_path = constants.WORKING_FOLDER / '.wit'/ 'references.txt'
    assert wit_general_functions.get_branch_reference(ref_file_path, 'adi')
    
    
def test_checkout_adi():
    sys.argv = ['_', 'checkout', 'adi']
    main.main()
    assert 'adi' == wit_general_functions.get_activated_branch_name(constants.WORKING_FOLDER / '.wit')
    
    ref_file_path = constants.WORKING_FOLDER / '.wit'/ 'references.txt'
    assert (
        wit_general_functions.get_branch_reference(ref_file_path, 'adi') == 
        wit_general_functions.get_commit_head(ref_file_path)
    )
    
    
def test_checkout_fail_for_not_staged_for_commit():
    (constants.WORKING_FOLDER / 'text_checkout.txt').write_text('hi')
    file_path = constants.WORKING_FOLDER / 'text_checkout.txt'
    wit_add.add(file_path)
    wit_commit.commit('For status')
    (constants.WORKING_FOLDER / 'text_checkout.txt').write_text('bye')
    
    sys.argv = ['_', 'checkout', 'adi']
    
    assert main.main() is None
       
    
    


    
    
    