def generate_commit_message(diff_text):
    """
    Very basic rule based commit message generator.
    You can swap this later with LLM.
    """
    lines = diff_text.splitlines()
    additions = sum(1 for l in lines if l.startswith("+") and not l.startswith("+++"))
    deletions = sum(1 for l in lines if l.startswith("-") and not l.startswith("---"))

    return f"Update dotfiles (+{additions} / -{deletions})"
