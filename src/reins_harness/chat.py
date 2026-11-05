import os
from openai import OpenAI
from pathlib import Path

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

    resp = client.chat.completions.create(
        model=os.environ["MODEL_DEFAULT"],
        messages=messages,
    )
    reply = resp.choices[0].message.content

    messages.append({"role": "assistant","content":reply})
    print(reply)