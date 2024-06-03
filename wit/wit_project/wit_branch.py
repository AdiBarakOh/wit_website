import logging
from pathlib import Path

from wit_project import constants
from wit_project import wit_general_functions


logger = logging.getLogger(__name__)


def branch(branch_name: str) -> None:
    wit_folder: bool | Path = wit_general_functions.check_wit_folder(constants.WORKING_FOLDER)
    if not wit_folder:
        logger.error('No .wit folder in the directory. branch function was not completed.')
        return
    references_file: Path = wit_folder / 'references.txt'
    wit_general_functions.add_branch_references(references_file, branch_name)
    
    
