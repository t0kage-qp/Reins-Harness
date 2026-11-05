import json
import os
from openai import OpenAI

from reins_harness.tools import TOOLS, run_tool

MAX_STEPS = 10

client = OpenAI(
    base_url=os.environ["BASE_URL"],
    api_key=os.environ["API_KEY"],
    default_headers={"User-Agent": "reins-harness/1.0"},
)

def run_agent(messages: list) -> str:
    """Run the agent loop on messages (mutated in place) and return the final reply."""
    for _ in range(MAX_STEPS):
        resp = client.chat.completions.create(
            model=os.environ["MODEL_DEFAULT"],
            messages=messages,
            tools=TOOLS,
        )
        msg = resp.choices[0].message

        if not msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content})
            return msg.content

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

    return "[stopped] MAX_STEPS complete"