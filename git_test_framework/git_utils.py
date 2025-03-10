import subprocess
import shutil
import os
from typing import Tuple


def run_git_command(command: list, repo_path: str = None) -> tuple:
    """
    Executes a Git command using subprocess.

    Args:
        command (list): Git command as a list (e.g., ['commit', '-m', 'message']).
        repo_path (str, optional): Path to repository. Defaults to None.

    Returns:
        Tuple[int, str, str]: (exit_code, stdout, stderr)
    """
    full_command = ['git'] + command
    try:
        result = subprocess.run(
            full_command,
            cwd=repo_path if repo_path else None,
            text=True,
            capture_output=True,
            check=False
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, '', str(e)


def delete_existing_repo(path: str):
    """Deletes the given directory if it exists."""
    if os.path.exists(path):
        shutil.rmtree(path)


def clone_repo(repo_url: str, clone_path: str):
    """Clones the given Git repository to the specified path."""
    exit_code, stdout, stderr = run_git_command(["clone", repo_url, clone_path])
    assert exit_code == 0, f"Git clone failed: {stderr}"


def create_branch(repo_path: str, branch_name: str):
    """Creates and switches to a new branch."""
    exit_code, stdout, stderr = run_git_command(["checkout", "-b", branch_name], repo_path)
    assert exit_code == 0, f"Creating branch failed: {stderr}"


def checkout_branch(repo_path: str, branch_name: str):
    """Checks out the specified branch."""
    exit_code, stdout, stderr = run_git_command(["checkout", branch_name], repo_path)
    assert exit_code == 0, f"Checkout failed: {stderr}"


def add_file(repo_path: str, file_name: str, content: str):
    """Creates and stages a file."""
    file_path = os.path.join(repo_path, file_name)
    with open(file_path, "w") as f:
        f.write(content)
    exit_code, stdout, stderr = run_git_command(["add", file_name], repo_path)
    assert exit_code == 0, f"Git add failed: {stderr}"


def commit_changes(repo_path: str, message: str):
    """Commits staged changes with the specified message."""
    exit_code, stdout, stderr = run_git_command(["commit", "-m", message], repo_path)
    assert exit_code == 0, f"Git commit failed: {stderr}"


def push_branch(repo_path: str, remote: str, branch_name: str):
    """Pushes the branch to the remote repository."""
    exit_code, stdout, stderr = run_git_command(["push", remote, branch_name], repo_path)
    assert exit_code == 0, f"Git push failed: {stderr}"


def merge_branch(repo_path: str, branch_name: str):
    """Merges a branch into the currently active branch."""
    exit_code, stdout, stderr = run_git_command(["merge", branch_name], repo_path)
    assert exit_code == 0, f"Git merge failed: {stderr}"


def pull_branch(repo_path: str, remote: str, branch_name: str):
    """Pulls the latest changes from a remote branch."""
    exit_code, stdout, stderr = run_git_command(["pull", remote, branch_name], repo_path)
    assert exit_code == 0, f"Git pull failed: {stderr}"


def delete_branch_remote(repo_path: str, remote: str, branch_name: str):
    """Deletes the specified remote branch."""
    exit_code, stdout, stderr = run_git_command(["push", remote, "--delete", branch_name], repo_path)
    assert exit_code == 0, f"Deleting remote branch failed: {stderr}"
