from git_test_framework.git_utils import *

REPO_URL = "git@github.com:cosminalbescu/test.git"
CLONE_PATH = os.path.join("tmp", "git_workflow_repo")


def test_git_cleanup():
    """
    Cleanup test:
    1. Delete test files from repo, commit and push
    2. Delete the temporary branches from GitHub
    3. Delete the tmp directory
    """

    # Step 1: Delete and re-clone fresh copy of repository
    delete_existing_repo(CLONE_PATH)
    clone_repo(REPO_URL, CLONE_PATH)

    # Step 2: Remove test files from repo
    files_to_delete = ["workflow_test.txt"]
    deleted_files = []

    for file_name in files_to_delete:
        file_path = os.path.join(CLONE_PATH, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            deleted_files.append(file_name)

    # Step 3: Mark deleted files in Git, create a commit with the changes, and push them to the remote repository.
    if deleted_files:
        run_git_command(["add"] + deleted_files, CLONE_PATH)
        commit_changes(CLONE_PATH, "Cleanup test files")
        push_branch(CLONE_PATH, "origin", "main")

    # Step 4: Delete remote branches
    branches_to_delete = ["feature-workflow"]
    for branch in branches_to_delete:
        delete_branch_remote(CLONE_PATH, "origin", branch)

    # Step 5: Delete tmp directory entirely
    delete_existing_repo("tmp")
