import os


def load_system_prompt() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_dir = os.path.join(script_dir, "prompt")

    parts = []
    if os.path.isdir(prompt_dir):
        for filename in sorted(os.listdir(prompt_dir)):
            file_path = os.path.join(prompt_dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    parts.append(f.read())

    return "\n".join(parts)


SYSTEM_PROMPT = load_system_prompt()