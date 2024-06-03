import os
import logging
from pathlib import Path

from wit_project import constants
from wit_project import wit_general_functions


logger = logging.getLogger(__name__)


def commit(message: str) -> None:
    """Add files and folders from .wit\\staging_area to commmid_id folder in .wit\\images and create logs."""
    
    wit_folder: bool | Path = wit_general_functions.check_wit_folder(constants.WORKING_FOLDER)
    if not wit_folder:
        logger.error('No .wit folder in the directory. commit function was not completed.')
        return
    
    commit_id: str = wit_general_functions.create_commit_id()
    images_folder_path: Path = wit_folder / 'images'
    commit_folder_path: Path = images_folder_path /commit_id
    reference_file_path: Path = wit_folder / 'references.txt'
    os.makedirs(commit_folder_path)
    if not commit_folder_path.exists():
        logger.critical(f"Failed to create commit folder: {commit_folder_path}")
    
    head_id: str | None = wit_general_functions.get_commit_head(reference_file_path)
    activated_branch_name: str = wit_general_functions.get_activated_branch_name(wit_folder)
    branch_head: str | None = wit_general_functions.get_branch_reference(reference_file_path, activated_branch_name)
    wit_general_functions.create_commit_txt(parent_id=head_id, images_folder_path=images_folder_path, commit_id=commit_id, message=message)
    
    master_id: str | None = wit_general_functions.get_branch_reference(reference_file_path, 'master')
    if master_id == head_id and activated_branch_name == 'master':
        wit_general_functions.add_commit_references(wit_folder=wit_folder,commit_id=commit_id, new_master_id=commit_id) 
    else:
        wit_general_functions.add_commit_references(wit_folder=wit_folder, commit_id=commit_id, new_master_id=master_id)
    if branch_head == head_id:
        wit_general_functions.add_branch_references(reference_file_path, activated_branch_name)
    staging_folder_path: Path = wit_folder / 'staging_area'
    wit_general_functions.copy_folder(src_folder=staging_folder_path, dest_folder=commit_folder_path)
    
    
