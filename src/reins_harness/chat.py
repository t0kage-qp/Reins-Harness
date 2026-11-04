import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["BASE_URL"],
    api_key=os.environ["API_KEY"],
    # Name your app here: the API's firewall rejects the SDK's default User-Agent.
    default_headers={"User-Agent": "reins-harness/1.0"},
)

completion = client.chat.completions.create(
    model=os.environ["MODEL_DEFAULT"],
    messages=[{"role": "user", "content": "Hi what is your name?"}],
)

print(completion.choices[0].message.content)