from pathlib import Path
import flask
from flask import render_template
from flask import request
from flask import Response
from flask import url_for

from wit_project import wit_add  # wit_project in .venv
from wit_project import wit_branch
from wit_project import wit_checkout
from wit_project import wit_commit
from wit_project import wit_init
from wit_project import wit_status
from wit_project import wit_general_functions


create_app = flask.Flask(__name__)


@create_app.route('/', methods=['GET', 'POST'])
def index() -> Response | str:
    """Provide files' status and an option to commit."""
    wit_init.init()
    file_to_add = None
    commit_ok = None
    
    if request.method == 'POST':
        file_to_add = request.form.get('path_to_file')
        commit_message = request.form.get('commit_message')
        commit_ok = commit_files(commit_message)
    
    status = wit_status.status()
    if not file_to_add:
        return render_template(
        'index.html',
        latest_commit_head=status.latest_commit_head,
        changes_to_be_committed=status.changes_to_be_committed,
        changes_not_staged_for_commit=status.changes_not_staged_for_commit,
        untracked_files=status.untracked_files,
        commit_success=commit_ok,
        )
    
    return check_add(file_to_add)


@create_app.route('/add/<file_name>', methods=['GET', 'POST'])
def check_add(file_name: str) -> Response:
    """Check if wit_add was made"""
    file_path = Path(file_name.strip('"'))
    wit_add.add(file_path)
    if test_add(file_path):
        add_ok_template = render_template("add_ok.html", file_name=file_name)    
        return Response(add_ok_template, status=200)
    add_failed_template = render_template("add_failed.html", file_name=file_name)
    return Response(add_failed_template, status=400)


@create_app.route('/add', methods=['GET', 'POST'])
def add_file() -> Response | str:
    """Add user's input of file."""
    if request.method == 'POST':
        file_name = request.form.get('file_name')
        return check_add(file_name)
    return render_template("add_file.html")


@create_app.route('/branches', methods=['GET', 'POST'])
def branches() -> str:
    """show branches and create new when requested."""
    activated_branch = None
    
    branches = get_all_branches()  
    activated_branch = wit_general_functions.get_activated_branch_name(Path.cwd() / '.wit')
    
    if request.method == 'POST':
        new_branch = request.form.get('new_branch')
        if new_branch != '':
            wit_branch.branch(new_branch)
    return render_template("branches.html", branches=branches, activated_branch=activated_branch)


@create_app.route('/checkout', methods=['GET', 'POST'])
def checkout_branch() -> str:
    
    all_branches = get_all_branches()
    redirect_url = url_for('index')
    checkout_ok = None
    files_in_branch_head_commit = None
    branch_name = request.args.get('branch_name')
    
    if branch_name:
        checkout_ok = wit_checkout.checkout(branch_name)
        commit_head = wit_general_functions.get_commit_head(Path.cwd() / '.wit'/ 'references.txt')
        if commit_head:
            files_in_branch_head_commit = wit_general_functions.get_all_files_in_dir(Path.cwd() / '.wit'/ "images" / commit_head)
    
    return render_template(
        "checkout.html",
        files_in_branch_head_commit=files_in_branch_head_commit,
        branch_name=branch_name,
        checkout_ok=checkout_ok,
        redirect_url=redirect_url,
        all_branches=all_branches
    )


def commit_files(commit_message: str | None) -> bool:
    if commit_message:
        wit_commit.commit(commit_message)
        return test_commit()
    return False


def test_commit() -> bool:
    commit_head = wit_general_functions.get_commit_head(Path.cwd() / '.wit'/ 'references.txt')
    commit_folder = Path.cwd() / '.wit'/ "images" / commit_head
    staging_folder: Path = Path.cwd() / '.wit' / "staging_area"
    if commit_head and commit_folder:
       diffrent_save = wit_general_functions.compare_files_and_dir(staging_folder, commit_folder).diffrent_save_of_files
       not_available = wit_general_functions.compare_files_and_dir(staging_folder, commit_folder).in_dir_1_not_in_dir_2
       return len(diffrent_save) + len(not_available) == 0
    return False
        
        
def get_all_branches() -> set[str] | None:
    references_file = Path.cwd() / '.wit' / 'references.txt'
    if references_file.exists():
        refrences_by_commits = references_file.read_text().splitlines()
        all_branches: set[str] = set()
        for ref in refrences_by_commits:
            branch_ref = ref.split('=')[0]
            if ref.startswith(branch_ref) and branch_ref != 'HEAD':
                all_branches.add(branch_ref)
        return all_branches
    return None


def test_add(file_added: Path) -> bool:
    staging_folder: Path = Path.cwd() / '.wit' / "staging_area"
    return file_added in wit_general_functions.compare_files_and_dir(Path.cwd(), staging_folder).same_files
    

if __name__ == '__main__':
    create_app.run(host='localhost', port=5000, debug=True)
    
    
    
