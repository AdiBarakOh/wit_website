import logging
import os

from wit_project import constants
from wit_project import wit_general_functions


logger = logging.getLogger(__name__)


def init(test=False) -> None:
    """Create .wit folders in current working directory."""
    
    os.makedirs((constants.WORKING_FOLDER / '.wit' / 'images'), exist_ok=True)
    os.makedirs((constants.WORKING_FOLDER / '.wit' / 'staging_area'), exist_ok=True)
    wit_folder = constants.WORKING_FOLDER / '.wit'
    wit_general_functions.create_activated_branch_txt(wit_folder, 'master')
    
    if not wit_folder.exists():
        logger.critical('Creation of .wit folder failed.')
    
