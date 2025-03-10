# **Git Test Framework** 🚀

This framework automates testing for basic Git functionality, including:
- **Cloning a repository** (`git clone`)
- **Creating and pushing a commit** (`git push`)
- **Creating and merging a branch** (`git merge`)
- **Pulling changes after a merge** (`git pull`)
- **Cleaning up test files, branches, and local repositories** (`git rm`, `git branch -D`)

## 📌 **Prerequisites**

Before running the tests, ensure you have:
- **Python 3 installed** (`python3 --version`)
- **pytest installed** (`pip install pytest`)
- **SSH authentication set up for GitHub** (if using SSH URLs)

## 🚀 **Running the Full Test Suite (In Correct Order)**

To execute **all** Git tests in the correct order, run:

```bash
python3 -m pytest tests/
```

Test execution order:
1. **test_01_git.py** (Unit tests for Git functionality)
2. **test_02_git_workflow.py** (Workflow test: clone → commit → push → merge → pull)
3. **test_03_git_cleanup.py** (Deletes test files and branches)

For detailed output, add `-v`:

```bash
python3 -m pytest tests/ -v
```

---

## 🚀 **Running Individual Test Suites**
The framework is modular. You can run specific tests:

### 🔹 **Running Unit Tests (Basic Git Operations)**
To test **individual Git commands** (clone, commit, push, merge), run:

```bash
python3 -m pytest tests/test_01_git.py
```

---

### 🔹 **Running the Full Git Workflow (Without Cleanup)**
To test a **complete Git workflow** (clone → branch → commit → push → merge → pull), without cleaning up:

```bash
python3 -m pytest tests/test_02_git_workflow.py
```

This will:
- Clone the repository
- Create a feature branch
- Add and commit a test file
- Push and merge into `main`
- Pull changes for verification
- **Does NOT delete files or branches!**

---

### 🔹 **Running Cleanup Separately**
To **remove test files**, **delete test branches**, and **clean local repositories**, run:

```bash
python3 -m pytest tests/test_03_git_cleanup.py
```

This will:
- Delete test files from `main`
- Commit and push the cleanup
- Delete temporary test branches
- Remove all cloned test directories

---

## 🚀 **Running All Tests Except Cleanup**
If you want to test **everything** except cleanup, use:

```bash
python3 -m pytest tests/ -k "not test_git_cleanup"
```

---

## 🔄 **Clearing Pytest Cache (If Needed)**
If you experience issues with test results persisting unexpectedly, clear the `pytest` cache before running tests:

```bash
python3 -m pytest --cache-clear tests/
```

---

## 🔍 **Running a Specific Test Case**
To execute a single test case from any test file, specify the function name:

```bash
python3 -m pytest tests/test_01_git.py::test_git_clone
```

This allows running a single test without executing the entire suite.

---

## 📂 **Project Structure**
```
git_test_framework/
│── tests/
│   ├── test_01_git.py            # Unit tests for Git functionality
│   ├── test_02_git_workflow.py   # Full Git workflow test (without cleanup)
│   ├── test_03_git_cleanup.py    # Cleanup test (removes test artifacts)
│── git_utils.py               # Helper functions for running Git commands
│── README.md                  # Documentation
```

---

## ❗ **Notes**
- Ensure your GitHub repository is accessible (via SSH or HTTPS).
- **Workflow tests create a feature branch** and merge it into `main`.
- **Run the cleanup test separately** to delete test files and branches.
- If a test fails, you can debug by running tests individually.

---

### ✅ **Happy Testing! 🚀**  
This modular structure allows **flexible testing**, making it **CI/CD friendly**, easy to debug, and highly maintainable. 🎯

