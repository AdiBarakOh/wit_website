from collections import namedtuple
import logging
from pathlib import Path

from wit_project import constants
from wit_project import wit_general_functions


logger = logging.getLogger(__name__)


def status() -> tuple[str | None, list[Path], list[Path], list[Path]] | None:
    """Print status of files to be commited or not in current working directory."""
    
    wit_folder: bool | Path = wit_general_functions.check_wit_folder(constants.WORKING_FOLDER)
    if not wit_folder:
        logger.error('No .wit folder in the directory. status function was not completed.')
        return
    latest_commit_head: str | None = wit_general_functions.get_commit_head(wit_folder / 'references.txt')
    if latest_commit_head is None:
        latest_commit_head = 'No commits Yet'
    
    staging_folder_path: Path = wit_folder / 'staging_area'
    commit_folder_path: Path = wit_folder / 'images' / latest_commit_head
    _, files_in_commit_not_updated, only_in_staging = wit_general_functions.compare_files_and_dir(staging_folder_path, commit_folder_path)
    changes_to_be_committed = files_in_commit_not_updated + only_in_staging
    
    wit_parent_folder = wit_folder.parent
    _, changes_not_staged_for_commit, _ = wit_general_functions.compare_files_and_dir(wit_parent_folder, staging_folder_path)
    _, _, files_only_in_wit_folder = wit_general_functions.compare_files_and_dir(wit_parent_folder, staging_folder_path)
    untracked_files: list[Path] = [file for file in files_only_in_wit_folder if not wit_general_functions.check_if_wit_file(file)]

    print(f"{latest_commit_head=}")
    print(f"{changes_to_be_committed=}")
    print(f"{changes_to_be_committed=}")
    print(f"{changes_not_staged_for_commit=}")
    print(f"{untracked_files=}")
    Status = namedtuple('Status', ['latest_commit_head', 'changes_to_be_committed', 'changes_not_staged_for_commit', 'untracked_files'])
    status = Status(
        latest_commit_head,
        changes_to_be_committed,
        changes_not_staged_for_commit,
        untracked_files,
    )
    return status
