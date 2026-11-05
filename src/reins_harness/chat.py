import json
import os
from openai import OpenAI
from pathlib import Path
from reins_harness.tools import TOOLS, run_tool

MAX_STEPS = 10


BASE = Path(__file__).parent
system_prompt = (BASE / "system_prompt.md").read_text(encoding="utf-8")

messages=[
    {"role": "system", "content": system_prompt}
]

client = OpenAI(
    base_url=os.environ["BASE_URL"],
    api_key=os.environ["API_KEY"],
    # Name your app here: the API's firewall rejects the SDK's default User-Agent.
    default_headers={"User-Agent": "reins-harness/1.0"},
)

while True:
    user_input = input("> ")
    if user_input.strip() in ("exit","quit"):
        break
    messages.append({"role": "user", "content":user_input})

    for step in range(MAX_STEPS):
        resp = client.chat.completions.create(
            model=os.environ["MODEL_DEFAULT"],
            messages=messages,
            tools=TOOLS,
        )
        msg = resp.choices[0].message

        if not msg.tool_calls:
            break

        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            print(f"[tool call] {call.function.name}({args})")
            result = run_tool(call.function.name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result,
            })

    else:
        print("[stopped] MAX_STEPS complete")

    print(msg.content)
    messages.append({"role": "assistant", "content": msg.content})