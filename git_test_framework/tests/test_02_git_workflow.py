from git_test_framework.git_utils import *

REPO_URL = "git@github.com:cosminalbescu/test.git"
CLONE_PATH = os.path.join("tmp", "git_workflow_repo")


def test_git_workflow():
    """
    End-to-end test that simulates a real Git workflow:
    1. Clone repo
    2. Create branch
    3. Add file
    4. Commit
    5. Push
    6. Merge into main
    7. Pull for verification
    """
    # Step 1: Delete old repo and clone fresh copy
    delete_existing_repo(CLONE_PATH)
    clone_repo(REPO_URL, CLONE_PATH)

    # Step 2: Create and switch to a new branch
    create_branch(CLONE_PATH, "feature-workflow")

    # Step 3: Add a new file
    add_file(CLONE_PATH, "workflow_test.txt", "Testing Git workflow")

    # Step 4: Commit changes
    commit_changes(CLONE_PATH, "Adding workflow test file")

    # Step 5: Push branch to remote
    push_branch(CLONE_PATH, "origin", "feature-workflow")

    # Step 6: Merge into main
    checkout_branch(CLONE_PATH, "main")
    merge_branch(CLONE_PATH, "feature-workflow")
    push_branch(CLONE_PATH, "origin", "main")

    # Step 7: Pull latest changes from main
    pull_branch(CLONE_PATH, "origin", "main")

    # Step 8: Verify if the merged file exists
    merged_file = os.path.join(CLONE_PATH, "workflow_test.txt")
    assert os.path.exists(merged_file), "workflow_test.txt not found after merge!"
