import subprocess
from typing import Tuple


def run_git_command(command: list, repo_path: str = None) -> Tuple[int, str, str]:
    """
    Runs a Git command using subprocess and returns the exit code, stdout, and stderr.

    Args:
        command (list): The Git command to execute as a list (e.g., ['commit', '-m', 'message']).
        repo_path (str, optional): Path to the Git repository. If None, runs in the current directory.

    Returns:
        Tuple[int, str, str]: A tuple containing (exit_code, stdout, stderr).
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


def initialize_repo(repo_path: str) -> Tuple[int, str, str]:
    """Initializes a new Git repository in the given path."""
    return run_git_command(['init'], repo_path)


def clone_repo(repo_url: str, destination_path: str) -> Tuple[int, str, str]:
    """Clones a Git repository from a remote URL to a local path."""
    return run_git_command(['clone', repo_url, destination_path])


def create_commit(repo_path: str, message: str) -> Tuple[int, str, str]:
    """
    Creates a new commit in the repository (assumes that there are staged changes).
    """
    return run_git_command(['commit', '-m', message], repo_path)


def push_changes(repo_path: str, remote: str = 'origin', branch: str = 'main') -> Tuple[int, str, str]:
    """Pushes committed changes to the remote repository."""
    return run_git_command(['push', remote, branch], repo_path)


def pull_changes(repo_path: str, remote: str = 'origin', branch: str = 'main') -> Tuple[int, str, str]:
    """Pulls the latest changes from the remote repository."""
    return run_git_command(['pull', remote, branch], repo_path)