from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Static
from textual import work
from reins_harness.agent import run_agent
from reins_harness.prompts import SYSTEM_PROMPT


class ReinsApp(App):
    CSS = """
    VerticalScroll { padding: 1 2; }
    Input { dock: bottom; }
    """

    def __init__(self):
        super().__init__()
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat")
        yield Input(placeholder="Type a message...")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return
        event.input.value = ""
        self.add_message(f"> {text}")
        self.messages.append({"role": "user", "content": text})
        self.ask_agent()

    def add_message(self, text: str) -> None:
        chat = self.query_one("#chat", VerticalScroll)
        chat.mount(Static(text))
        chat.scroll_end()

    @work(thread=True)
    def ask_agent(self) -> None:
        reply = run_agent(self.messages)
        self.call_from_thread(self.add_message, reply)


def main():
    ReinsApp().run()


if __name__ == "__main__":
    main()