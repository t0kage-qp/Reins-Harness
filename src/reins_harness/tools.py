from pathlib import Path

def read_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as e:
        return f"Error: {e}"

TOOLS = [{
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read a text file and return its contents.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file"},
            },
            "required": ["path"],
        },
    },
}]

REGISTRY = {"read_file": read_file}

def run_tool(name: str, args: dict) -> str:
    fn = REGISTRY.get(name)
    if fn is None:
        return f"Error: unknown tool {name}"
    return fn(**args)