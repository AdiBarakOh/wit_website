import logging
from pathlib import Path
from typing import TypeAlias
import warnings

from wit_project import constants
from wit_project import wit_general_functions
from wit_project import wit_status


logger = logging.getLogger(__name__)
status_result_type: TypeAlias = tuple[str | None, list[Path], list[Path], list[Path]] | None


def checkout(commit_id_or_branch: str) -> bool:
    """Copy files from relevent commit id or branch commit folder to the original folder where .wit folder exsists."""
    
    wit_folder: bool | Path = wit_general_functions.check_wit_folder(constants.WORKING_FOLDER)
    if not wit_folder:
        logger.error('No .wit folder in the directory. checkout function was not completed.')
        return False
    references_file: Path = wit_folder / 'references.txt'
    
    if wit_general_functions.is_commit_id(references_file, commit_id_or_branch):
        commit_id = commit_id_or_branch
    else:
        commit_id = wit_general_functions.get_branch_reference(references_file, commit_id_or_branch)
        wit_general_functions.create_activated_branch_txt(wit_folder, commit_id_or_branch)
        
    if commit_id is None:
        logger.error(f'Failed to find commit id or branch: {commit_id_or_branch}')
        return False
    
    assert commit_id is not None  
     
    status_result: status_result_type = wit_status.status()
    assert status_result is not None
    
    changes_to_be_committed: list = status_result[1]
    changes_not_staged_for_commit: list = status_result[2]
    if changes_to_be_committed or changes_not_staged_for_commit:
        warnings.warn("failed checkout: there are still changes to be committed or changes not staged for commit.")
        return False
    
    commit_folder: Path = wit_folder / 'images' / commit_id
    wit_parent_folder: Path = wit_folder.parent
    wit_general_functions.copy_files_to_relative_folders(commit_folder, commit_folder, wit_parent_folder)
    
    staging_folder: Path = wit_folder / 'staging_area'
    master_id: str = wit_general_functions.get_branch_reference(references_file, 'master')
    if master_id is None:
        logger.critical(f'checkout failed: No master branch was found in {references_file}')
        return False
    
    assert master_id is not None
    wit_general_functions.add_commit_references(wit_folder, commit_id, master_id)
    wit_general_functions.copy_folder(commit_folder, staging_folder)
    return True
    
