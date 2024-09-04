# AI Code Review repository

Check out the blog post and follow along: https://taskautomation.dev/blog/code-review


## Post commit hook which runs the python script.

```bash

#!/bin/sh
echo "executing post-commit"

commit1=$(git rev-parse HEAD^)
commit2=$(git rev-parse HEAD)

powershell.exe -Command ". .venv\\Scripts\\Activate.ps1"

python "post-commit.py" "$commit1" "$commit2"

exit 0

```

## Python script which runs the git diff command and then runs the AI code review.

```python	

import sys
import os
import subprocess
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from rich.console import Console
from rich.markdown import Markdown

console = Console()

commit1 = sys.argv[1]
commit2 = sys.argv[2]

git_diff_command = f"git diff {commit1} {commit2}"

# Use the current working directory as the repository path
cwd = os.getcwd()

# Execute the git diff command and get the output
diff_output = subprocess.check_output(git_diff_command, shell=True, cwd=cwd).decode("utf-8")

prompt = """
You are an expert developer and git super user. You do code reviews based on the git diff output between two commits. Complete the following tasks, and be extremely critical and precise in your review:
* [Description] Describe the code change.
* [Obvious errors] Look for obvious errors in the code.
* [Improvements] Suggest improvements where relevant.
* [Friendly advice] Give some friendly advice or heads up where relevant.
* [Stop when done] Stop when you are done with the review.

This is the git diff output between two commits: \n\n {diff}

AI OUTPUT:

"""

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


output_parser = StrOutputParser()
PROMPT = PromptTemplate(template=prompt, input_variables=["diff"])
chain = PROMPT | llm | output_parser

print("Running diffs...")
results = chain.invoke({"diff": diff_output})

md = Markdown(results)
console.print(md)

```