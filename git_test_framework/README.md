# Git Test Framework

This framework automates testing for basic Git functionality, including:
- **Cloning a repository** (`git clone`)
- **Creating and pushing a commit** (`git push`)
- **Creating and merging a branch** (`git merge`)
- **Pulling changes after a merge** (`git pull`)
- **Cleaning up test files, branches, and local repositories**

## 📌 Prerequisites

Before running the tests, ensure you have:
- **Python 3 installed** (`python3 --version`)
- **pytest installed** (`pip install pytest`)
- **SSH authentication set up for GitHub** (if using SSH URLs)

## 🚀 Running the Full Test Suite

To execute all the Git tests, run:

```bash
python3 -m pytest tests/
```

This will:
1. Clone the repository.
2. Push a test commit to a new branch.
3. Merge changes into `main`.
4. Pull changes and verify the merge.
5. Cleanup test artifacts.

## 🚀 Running All Tests Except Cleanup

To execute all tests **except** the cleanup test, run:

```bash
python3 -m pytest tests/ -k "not test_git_cleanup"
```

This allows you to verify all Git operations without cleaning up test artifacts immediately.

## 🧹 Running Only the Cleanup Test

To remove test files, delete test branches from GitHub, and clean local repositories, run:

```bash
python3 -m pytest tests/ -k "test_git_cleanup"
```

## 📂 Project Structure

```
git_test_framework/
│── tests/
│   ├── test_git.py           # Test cases for Git functionality
│── git_utils.py               # Helper functions for running Git commands
│── README.md                  # Documentation
```

## ❗ Notes
- Ensure your GitHub repository is accessible (either via SSH or HTTPS).
- Test branches are automatically created and merged into `main`.
- **Run the cleanup test if you want to reset your repository after testing.**

Happy testing! 🚀

