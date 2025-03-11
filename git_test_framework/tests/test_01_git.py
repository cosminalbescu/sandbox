from git_test_framework.git_utils import *

REPO_URL = "git@github.com:cosminalbescu/test.git"
CLONE_PATH = os.path.join("tmp", "git_push_repo")


def test_delete_existing_repo():
    """Test to ensure local clone directory is deleted properly."""
    delete_existing_repo(CLONE_PATH)
    assert not os.path.exists(CLONE_PATH), "Directory was not deleted."


def test_git_clone():
    """Test that cloning from GitHub is successful."""
    delete_existing_repo(CLONE_PATH)
    clone_repo(REPO_URL, CLONE_PATH)
    assert os.path.exists(CLONE_PATH), "Clone directory was not created."


def test_git_create_branch():
    """Test that a new branch can be created and checked out."""
    create_branch(CLONE_PATH, "test-branch")


def test_git_add_file():
    """Test adding a file to staging."""
    add_file(CLONE_PATH, "push_test.txt", "Test push!")
    exit_code, stdout, _ = run_git_command(["status"], CLONE_PATH)
    assert "push_test.txt" in stdout, "File is not staged."


def test_git_commit():
    """Test committing staged files."""
    commit_changes(CLONE_PATH, "Test push commit")


def test_git_push():
    """Test pushing the new branch to remote."""
    push_branch(CLONE_PATH, "origin", "test-branch")


def test_git_merge():
    """Test merging the test branch back into main and pushing."""
    checkout_branch(CLONE_PATH, "main")
    merge_branch(CLONE_PATH, "test-branch")
    push_branch(CLONE_PATH, "origin", "main")


def test_git_pull():
    """Test pulling changes from the remote repository after merge."""
    pull_branch(CLONE_PATH, "origin", "main")
    file_path = os.path.join(CLONE_PATH, "push_test.txt")
    assert os.path.exists(file_path), "File push_test.txt not found after pull."


def test_git_cleanup():
    """Test cleanup by removing test files, branches and tmp directory."""

    # Reset the local repository by deleting and re-cloning a fresh copy.
    delete_existing_repo(CLONE_PATH)
    clone_repo(REPO_URL, CLONE_PATH)

    # Remove specific test files that were created in previous tests.
    files_to_delete = ["push_test.txt"]
    for file in files_to_delete:
        file_path = os.path.join(CLONE_PATH, file)
        if os.path.exists(file_path):
            os.remove(file_path)

    # Mark deleted files in Git, create a commit with the changes, and push them to the remote repository.
    run_git_command(["add"] + files_to_delete, CLONE_PATH)
    commit_changes(CLONE_PATH, "Cleanup test files")
    push_branch(CLONE_PATH, "origin", "main")

    # Delete remote branches
    delete_branch_remote(CLONE_PATH, "origin", "test-branch")

    # Delete tmp directory entirely
    delete_existing_repo("tmp")
