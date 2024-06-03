import sys

import pytest

from wit_project import constants
from wit_project import main


def test_main_init(tmp_path):
    constants.WORKING_FOLDER = tmp_path
    sys.argv = ['_', 'init']
    main.main()
    assert (tmp_path / '.wit' / 'staging_area').exists()
    assert (tmp_path / '.wit' / 'images').exists()




