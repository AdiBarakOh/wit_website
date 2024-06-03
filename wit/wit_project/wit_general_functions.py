from collections import namedtuple
import datetime
import filecmp
import logging
import os
from pathlib import Path
import random
import shutil
import string
from typing import Iterator, NamedTuple


logger = logging.getLogger(__name__)


HEXDIGIT_CHARACTERS: list[str] = list(string.ascii_lowercase)[:6] + [str(number) for number in range(0, 10)]


def copy_files_to_relative_folders(
        src_dir: Path,
        relative_src_folder: Path,
        relative_dest_folder: Path,
        copy_wit_files=True,
) -> None:
    
    if src_dir.is_file():
        relative_folders_path: Path | str = get_relative_folders(src_dir, relative_src_folder)
        if relative_folders_path == src_dir.parent:
            finished_path: Path = relative_dest_folder   
        else:
            finished_path = relative_dest_folder / relative_folders_path
            finished_path.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy(src_dir, finished_path)
        except shutil.SameFileError:
            pass 
    else:
        for file in get_all_files_in_dir(directory=src_dir):
            relative_folders_path = get_relative_folders(file, relative_src_folder)
            if relative_folders_path == file.parent:
                finished_path = relative_dest_folder   
            else:
                finished_path = relative_dest_folder / relative_folders_path
            if copy_wit_files or not check_if_wit_file(file):
                os.makedirs(finished_path, exist_ok=True)
                try:
                    shutil.copy(file, finished_path)
                except shutil.SameFileError:
                    pass     
                
                
def get_relative_folders(file_path: Path, start_relative_path: Path) -> Path:
    """Get a realative path of a given directory from the start_relative_path."""
    
    folders: list[str] = []
    if file_path.is_file():
        file_path = file_path.parent
    while file_path != start_relative_path and file_path != file_path.parent:
        folders.append(file_path.stem)
        file_path = file_path.parent 
    folders.reverse()
    if folders:
        return Path(os.path.join(*folders))
    return start_relative_path


def copy_folder(src_folder: Path, dest_folder: Path) -> None:
        dest_folder.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)
    
        
    
def compare_files_and_dir(dir_1: Path, dir_2: Path) -> NamedTuple:
    """Compare files and their relative path in directories,
    and return whether they are the same, diffrent or not available in the second directory."""
    
    same_files: list[Path] = []
    diffrent_save_of_files: list[Path] = []
    in_dir_1_not_in_dir_2: list[Path] = []
    for file_1 in get_all_files_in_dir(dir_1):
        for file_2 in get_all_files_in_dir(dir_2):
            path_is_relative: bool = compare_relative_path(file_1, dir_1, file_2, dir_2)
            file_is_same: bool = filecmp.cmp(file_1, file_2)
            name_is_same: bool = file_1.name == file_2.name
            if path_is_relative and file_is_same and name_is_same:
                same_files.append(file_1)
            elif path_is_relative and name_is_same:
                diffrent_save_of_files.append(file_1)
        if file_1 not in same_files and file_1 not in diffrent_save_of_files:
            in_dir_1_not_in_dir_2.append(file_1)
    Compare = namedtuple('Compare', ['same_files', 'diffrent_save_of_files', 'in_dir_1_not_in_dir_2'])
    compare = Compare(same_files, diffrent_save_of_files, in_dir_1_not_in_dir_2)
    return compare


def get_all_files_in_dir(directory: Path) -> Iterator[Path]:
    """Return all files' path in a given directory."""
    
    for (dirpath, _, filenames) in os.walk(directory):
        for file in filenames:
            yield(Path(os.path.join(dirpath, file)))
    
    
def compare_relative_path(path_1: Path, relative_start_1: Path, path_2: Path, relative_start_2: Path) -> bool:
    """Compare relative folders of paths or files from given folders."""
    
    relative_path_1 = get_relative_folders(path_1, relative_start_1)
    relative_path_2 = get_relative_folders(path_2, relative_start_2)
    relative_path_is_start = relative_path_1 == relative_start_1 and relative_path_2 == relative_start_2
    return relative_path_1 == relative_path_2 or relative_path_is_start


def check_wit_folder(start_folder: Path) -> None | Path:
    """Check whether a .wit or folder exsists in a given directory."""
    
    file_path = start_folder
    if not file_path.exists():
        return None
    while file_path != file_path.parent:
        wit_path = file_path / '.wit'
        if wit_path.exists():
            return wit_path
        else:
            file_path = file_path.parent
    if (file_path / '.wit').exists():
        return file_path / '.wit'
    return None


def check_if_wit_file(file_path: Path) -> bool:
    """Check whether a file is under .wit or .mypy_cache folder directory."""
    while file_path.parent != file_path:
        if file_path.stem == '.wit' or file_path.stem == ".mypy_cache":
            return True
        file_path = file_path.parent
    return False


def create_commit_txt(parent_id: None | str, images_folder_path: Path, commit_id: str, message: str) -> None:
    file_path: Path = images_folder_path / (f"{commit_id}.txt")
    parent = parent_id
    date: str = f"{datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")}"
    text: str = (
        f"{parent=}\n"
        f"{date=}\n"
        f"{message=}\n"
    )
    file_path.write_text(text)
        
    
def create_commit_id() -> str:
    return "".join(random.choices(HEXDIGIT_CHARACTERS, k=40))


def add_commit_references(wit_folder: Path, commit_id: str, new_master_id: None | str) -> None:
    file_path = wit_folder / 'references.txt'
    if new_master_id is None:
        new_master_id = commit_id
    with open(file_path, 'a') as file:
        file.write(f"master={new_master_id}\nHEAD={commit_id}\n")
    
        
def get_commit_head(reference_file_path: Path) -> str | None:
    if reference_file_path.exists():
        refs = reference_file_path.read_text().splitlines()
        refs.reverse()
        for ref in refs:
            if ref.startswith('HEAD='):
                return ref.split('=')[1]
        
        logger.critical(f"No HEAD was found in refrence file: {reference_file_path}")
    return None


def is_commit_id(references_file: Path, user_commit_input: str) -> bool: 
    images_folder = references_file.parent / 'images'
    possible_commit_id = images_folder / (user_commit_input + '.txt')
    if possible_commit_id.exists():
        return True
    return False

def create_activated_branch_txt(wit_folder: Path, branch_name: str) -> None:
    activated_txt_path = wit_folder / 'activated.txt'
    with open(activated_txt_path, 'w') as file:
        file.write(branch_name)
        
        
def add_branch_references(references_file: Path, branch_name: str) -> None:
    commit_head = get_commit_head(references_file)
    with open(references_file, 'a') as file:
        file.write(f"{branch_name}={commit_head}\n")
        
        
def get_activated_branch_name(wit_folder: Path) -> str:
    activated_txt_path = wit_folder / 'activated.txt'
    return activated_txt_path.read_text()


def get_branch_reference(references_file: Path, branch_name: str) -> str | None:
    if references_file.exists():
        refrences_by_commits = references_file.read_text().splitlines()
        refrences_by_commits.reverse()
        for ref in refrences_by_commits:
            if ref.startswith(f"{branch_name}="):
                return ref.split('=')[1]
        
        logger.error(f'Failed to find branch: {branch_name} in {references_file}')
    return None
    

