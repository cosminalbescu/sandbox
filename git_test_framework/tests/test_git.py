import os
import shutil
import pytest
from git_test_framework.git_utils import run_git_command


def test_git_clone():
    """
    Tests if we can clone the GitHub repo
    """
    repo_url = "git@github.com:cosminalbescu/test.git"
    clone_path = "cloned_repo"

    # Delete `cloned_repo` if it exists
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)

    exit_code, stdout, stderr = run_git_command(["clone", repo_url, clone_path])
    assert exit_code == 0, f"`git clone` ERROR: {stderr}"


def test_git_push():
    repo_url = "git@github.com:cosminalbescu/test.git"
    repo_path = os.path.abspath("git_push_repo")

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    exit_code, stdout, stderr = run_git_command(["clone", repo_url, repo_path])
    assert exit_code == 0, f"`git clone` ERROR: {stderr}"

    test_file = os.path.join(repo_path, "push_test.txt")
    with open(test_file, "w") as f:
        f.write("Test push!")

    assert os.path.exists(test_file), "push_test.txt has not been created!"

    exit_code, stdout, stderr = run_git_command(["add", "."], repo_path)
    assert exit_code == 0, f"`git add` ERROR: {stderr}"

    exit_code, stdout, stderr = run_git_command(["status"], repo_path)
    assert "push_test.txt" in stdout, "push_test.txt does not exist in staging!"

    exit_code, stdout, stderr = run_git_command(["commit", "-m", "Test push commit"], repo_path)
    assert exit_code == 0, f"`git commit` ERROR: {stderr}"

    exit_code, stdout, stderr = run_git_command(["checkout", "-b", "test-branch"], repo_path)
    assert exit_code == 0, f"`git checkout` ERROR: {stderr}"

    exit_code, stdout, stderr = run_git_command(["push", "origin", "test-branch"], repo_path)
    assert exit_code == 0, f"`git push` ERROR: {stderr}"


def test_git_merge():
    import time

    repo_url = "git@github.com:cosminalbescu/test.git"
    repo_path = os.path.abspath("git_merge_repo")

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    exit_code, stdout, stderr = run_git_command(["clone", repo_url, repo_path])
    assert exit_code == 0, f"clone ERROR: {stderr}"

    exit_code, stdout, stderr = run_git_command(["checkout", "-b", "feature-merge-test"], repo_path)
    assert exit_code == 0, f"New branch creation ERROR: {stderr}"

    # Unique filename and without .gitignore conflicts
    # unique_filename = f"merge_test_{int(time.time())}.txt"
    unique_filename = "qa_test_merge.txt"
    new_file = os.path.join(repo_path, unique_filename)
    with open(new_file, "w") as f:
        f.write("Testing git merge functionality!")

    assert os.path.exists(new_file), f"{unique_filename} does not exist after creation!"

    # Adds the newly created file
    exit_code, stdout, stderr = run_git_command(["add", unique_filename], repo_path)
    assert exit_code == 0, f"Eroare la `git add`: {stderr}"

    # Verifies the file in staging
    exit_code, stdout, stderr = run_git_command(["status"], repo_path)
    assert unique_filename in stdout, f"{unique_filename} does not exist in staging:\n{stdout}\n{stderr}"

    # Commit
    exit_code, stdout, stderr = run_git_command(["commit", "-m", f"Add {unique_filename}"], repo_path)
    assert exit_code == 0, f"commit ERROR: {stderr}"

    # Checkout main & merge
    exit_code, stdout, stderr = run_git_command(["checkout", "main"], repo_path)
    assert exit_code == 0, f"checkout main ERROR: {stderr}"

    exit_code, stdout, stderr = run_git_command(["merge", "feature-merge-test"], repo_path)
    assert exit_code == 0, f"merge ERROR: {stderr}"

    # Push on main
    exit_code, stdout, stderr = run_git_command(["push", "origin", "main"], repo_path)
    assert exit_code == 0, f"push after merge ERROR: {stderr}"


def test_git_pull_after_merge():
    repo_url = "git@github.com:cosminalbescu/test.git"
    repo_path = os.path.abspath("git_pull_repo")

    # Cleanup if the repo exists
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    # Clone the repo again
    exit_code, stdout, stderr = run_git_command(["clone", repo_url, repo_path])
    assert exit_code == 0, f"clone ERROR: {stderr}"

    # Do a 'git pull' for safety
    exit_code, stdout, stderr = run_git_command(["pull", "origin", "main"], repo_path)
    assert exit_code == 0, f"pull ERROR: {stderr}"

    # Check if the file exists after merge
    merged_file = os.path.join(repo_path, "qa_test_merge.txt")
    assert os.path.exists(merged_file), "qa_test_merge.txt does not exist after pull!"

    with open(merged_file, "r") as f:
        content = f.read()
    assert "Testing git merge functionality!" in content, "Contents of qa_test_merge.txt is not correct!"


def test_git_cleanup():
    """
    Test care:
    1. Delete test files from repo, commit and push
    2. Delete the temporary branches from GitHub
    3. Delete local folders used by previous tests
    """
    repo_url = "git@github.com:cosminalbescu/test.git"
    repo_path = os.path.abspath("git_cleanup_repo")

    # Cleanup if the repo exists
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    # Clone the repo again
    exit_code, stdout, stderr = run_git_command(["clone", repo_url, repo_path])
    assert exit_code == 0, f"Clone ERROR: {stderr}"

    # === Delete the files from the repo ===
    files_to_delete = ["qa_test_merge.txt", "push_test.txt"]
    deleted_files = []

    for file_name in files_to_delete:
        file_path = os.path.join(repo_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            deleted_files.append(file_name)

    if deleted_files:
        exit_code, stdout, stderr = run_git_command(["add"] + deleted_files, repo_path)
        assert exit_code == 0, f"`git add` ERROR: {stderr}"

        exit_code, stdout, stderr = run_git_command(["commit", "-m", "Cleanup test files"], repo_path)
        assert exit_code == 0, f"Commit ERROR: {stderr}"

        exit_code, stdout, stderr = run_git_command(["push", "origin", "main"], repo_path)
        assert exit_code == 0, f"Push ERROR: {stderr}"
    else:
        print("Noting got deleted!")

    # === Delete temporary branches from GitHub ===
    branches_to_delete = ["test-branch", "feature-merge-test"]

    for branch in branches_to_delete:
        exit_code, stdout, stderr = run_git_command(["push", "origin", "--delete", branch], repo_path)
        if exit_code == 0:
            print(f"Branch {branch} has been successfully deleted!")
        else:
            print(f"Branch {branch} could NOT be deleted or did not exist!:\n{stderr}")

    # === Delete local folders used in tests ===
    local_folders = ["git_push_repo", "git_merge_repo", "git_pull_repo", "git_cleanup_repo"]

    for folder in local_folders:
        folder_path = os.path.abspath(folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"Folder {folder} was deleted.")

    print("Complete cleanup!")

