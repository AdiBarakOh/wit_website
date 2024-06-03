import logging
from pathlib import Path
import warnings

from wit_project import constants
from wit_project import wit_general_functions

logger = logging.getLogger(__name__)


def add(file_path: Path) -> None:
    """Add files to .wit\\staging_area if folder available in directory."""
    
    wit_folder: bool | Path = wit_general_functions.check_wit_folder(constants.WORKING_FOLDER)
    if not wit_folder:
        logger.error('No .wit folder in the directory. add function was not completed.')
        return
    if not wit_general_functions.check_wit_folder(file_path):
        warnings.warn('The path provided has no .wit folder in directory tree.')
        return
    
    wit_parent_folder: Path = wit_folder.parent
    wit_general_functions.copy_files_to_relative_folders(
        src_dir=file_path,
        relative_src_folder=wit_parent_folder,
        relative_dest_folder= wit_folder / "staging_area",
        copy_wit_files=False,
    )
    




