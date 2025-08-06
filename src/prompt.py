def ask_yes_no(prompt_text: str) -> bool:
    reply = input(f"{prompt_text} [y/N]: ").lower().strip()
    return reply == "y"
