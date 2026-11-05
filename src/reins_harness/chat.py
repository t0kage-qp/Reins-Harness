from pathlib import Path

from reins_harness.agent import run_agent
from reins_harness.prompts import SYSTEM_PROMPT

def main() -> None:
    base = Path(__file__).parent
    system_prompt = (base / "system_prompt.md").read_text(encoding="utf-8")
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        user_input = input("> ")
        if user_input.strip() in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": user_input})
        print(run_agent(messages))

if __name__ == "__main__":
    main()