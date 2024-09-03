import sys
import os
import subprocess

commit1 = sys.argv[1]
commit2 = sys.argv[2]

git_diff_command = f"git diff {commit1} {commit2}"

# Use the current working directory as the repository path
cwd = os.getcwd()

# Execute the git diff command and get the output
diff_output = subprocess.check_output(git_diff_command, shell=True, cwd=cwd).decode("utf-8")

print(diff_output)