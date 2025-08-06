import time
from pathlib import Path
from src.watcher import start_watching
from src import git_handler
from src.analyzer import generate_commit_message
from src.prompt import ask_yes_no

# path to your dotfiles repo
REPO_PATH = Path("/home/ayush/Ayush/dotfiles").expanduser()
AUTO_PUSH = False  # set True for auto-push mode

changed_files = set()


def on_change(file_path):
    # Only care about files inside the repo
    changed_files.add(file_path)
    print(f"Detected change: {file_path}")


def main():
    print("Watching for changes...")
    observer = start_watching(str(REPO_PATH), on_change)

    try:
        while True:
            if changed_files:
                time.sleep(2)  # simple debounce
                files = list(changed_files)
                changed_files.clear()

                # Stage files
                for f in files:
                    try:
                        git_handler.git_add(str(REPO_PATH), f)
                    except Exception as e:
                        print(f"Failed to stage {f}: {e}")

                # Show diff:
                diff = git_handler.git_diff(str(REPO_PATH))
                print("---- git diff ----")
                print(diff or "(no diff)")
                print("------------------")

                msg = generate_commit_message(diff)
                print(f"Proposed commit msg: {msg}")

                if AUTO_PUSH or ask_yes_no("Commit & push?"):
                    try:
                        git_handler.git_commit(str(REPO_PATH), msg)
                        git_handler.git_push(str(REPO_PATH), branch="main")
                        print("Pushed.")
                    except Exception as e:
                        print(f"Git error: {e}")
                else:
                    print("Skipped.")

            time.sleep(1)

    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
