import logging
from pathlib import Path
import sys
import warnings

from wit_project import wit_add
from wit_project import wit_branch
from wit_project import wit_checkout
from wit_project import wit_commit
from wit_project import wit_init
from wit_project import wit_status


logger = logging.getLogger(__name__)


def main() -> None:
    if sys.argv[1] == 'init':
        wit_init.init()
        
    if sys.argv[1] == 'add':
        try:
            wit_add.add(Path(sys.argv[2]))
        except IndexError:
            warnings.warn('Path to add should be applied.')
        
    if sys.argv[1] == 'commit':
        try:
            wit_commit.commit(sys.argv[2])  
        except IndexError:
            warnings.warn('Commit message should be applied.')
            
    if sys.argv[1] == 'status':
        wit_status.status()
        
    if sys.argv[1] == 'checkout':
        try:
            wit_checkout.checkout(sys.argv[2])
        except IndexError:
            warnings.warn('Branch or commit id should be applied.')
        
    if sys.argv[1] == 'branch':
        try:
            wit_branch.branch(sys.argv[2])
        except IndexError:
            warnings.warn('Branch name should be applied.')
        


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
        


