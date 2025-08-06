import subprocess
from pathlib import Path


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def git_diff(repo_path):
    return run("git diff", repo_path)


def git_add(repo_path, file_path):
    rel = str(Path(file_path).relative_to(repo_path))
    run(f"git add '{rel}'", repo_path)


def git_commit(repo_path, message):
    run(f"git commit -m \"{message}\"", repo_path)


def git_push(repo_path, branch="main"):
    run(f"git push origin {branch}", repo_path)
